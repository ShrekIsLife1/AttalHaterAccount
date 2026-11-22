import { Router, Request, Response } from "express";
import { getPrisma } from "../prisma.js";
import { requireAuth, requireRole } from "../middleware/auth.js";
import { calculateOrderPricing, OrderValidationError, OrderItemInput } from "../domain/pricing.js";

export const ordersRouter = Router();
const prisma = getPrisma();

/**
 * POST /api/orders
 * Customer places an order. Server re-evaluates prices, enforces business rules,
 * atomically reserves stock and persists the order.
 */
ordersRouter.post(
  "/",
  requireAuth,
  requireRole("CUSTOMER"),
  async (req: Request, res: Response) => {
    try {
      const { items } = req.body;

      if (!items || !Array.isArray(items) || items.length === 0) {
        return res.status(400).json({ error: "Order must contain at least one item" });
      }

      // Execute in atomic database transaction
      const result = await prisma.$transaction(async (tx) => {
        // Collect requested product IDs
        const productIds = items
          .filter((i) => i && typeof i.productId === "number")
          .map((i) => i.productId);

        const dbProducts = await tx.product.findMany({
          where: { id: { in: productIds } },
        });

        const productsMap = new Map<number, {
          id: number;
          name: string;
          priceMinor: number;
          stockQuantity: number;
          isActive: boolean;
        }>();

        for (const p of dbProducts) {
          productsMap.set(p.id, {
            id: p.id,
            name: p.name,
            priceMinor: p.priceMinor,
            stockQuantity: p.stockQuantity,
            isActive: p.isActive,
          });
        }

        // Validate domain rules and compute authoritative pricing
        const calculated = calculateOrderPricing(items as OrderItemInput[], productsMap);

        // Atomically decrement stock
        for (const line of calculated.lines) {
          await tx.product.update({
            where: { id: line.productId },
            data: {
              stockQuantity: {
                decrement: line.quantity,
              },
            },
          });
        }

        // Persist order with immutable price snapshots
        const order = await tx.order.create({
          data: {
            customerId: req.user!.id,
            status: "PLACED",
            totalMinor: calculated.totalMinor,
            items: {
              create: calculated.lines.map((l) => ({
                productId: l.productId,
                quantity: l.quantity,
                unitPriceAtOrder: l.unitPriceAtOrder,
              })),
            },
          },
          include: {
            items: {
              include: {
                product: true,
              },
            },
          },
        });

        return order;
      });

      return res.status(201).json({ order: result });
    } catch (err: any) {
      if (err instanceof OrderValidationError) {
        return res.status(400).json({ error: err.message });
      }
      return res.status(500).json({ error: "Failed to place order: " + (err?.message || "Internal error") });
    }
  }
);

/**
 * GET /api/orders/:id
 * Retrieve order details by ID with line items.
 */
ordersRouter.get("/:id", requireAuth, async (req: Request, res: Response) => {
  try {
    const id = Number(req.params.id);
    if (isNaN(id)) {
      return res.status(400).json({ error: "Invalid order ID" });
    }

    const order = await prisma.order.findUnique({
      where: { id },
      include: {
        items: {
          include: {
            product: true,
          },
        },
      },
    });

    if (!order) {
      return res.status(404).json({ error: "Order not found" });
    }

    // RBAC: CUSTOMER can only view their own order; OPERATOR can view any order
    if (req.user!.role === "CUSTOMER" && order.customerId !== req.user!.id) {
      return res.status(403).json({ error: "Forbidden: You cannot view another customer's order" });
    }

    return res.status(200).json({ order });
  } catch (err: any) {
    return res.status(500).json({ error: "Failed to retrieve order: " + (err?.message || "Internal error") });
  }
});
