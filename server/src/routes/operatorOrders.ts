import { Router, Request, Response } from "express";
import { getPrisma } from "../prisma.js";
import { requireAuth, requireRole } from "../middleware/auth.js";

export const operatorOrdersRouter = Router();
const prisma = getPrisma();

// All operator order routes require authenticated session with OPERATOR role
operatorOrdersRouter.use(requireAuth, requireRole("OPERATOR"));

/**
 * GET /api/operator/orders
 * Returns incoming orders awaiting review (status = PLACED), sorted chronologically (createdAt ASC).
 * AC-14 / FR-09 / TEST-17
 */
operatorOrdersRouter.get("/", async (_req: Request, res: Response) => {
  try {
    const orders = await prisma.order.findMany({
      where: { status: "PLACED" },
      orderBy: { createdAt: "asc" },
      include: {
        customer: {
          select: {
            id: true,
            email: true,
            name: true,
          },
        },
        items: {
          include: {
            product: true,
          },
        },
      },
    });

    return res.status(200).json(orders);
  } catch (err: any) {
    return res.status(500).json({ error: "Failed to retrieve incoming orders: " + (err?.message || "Internal error") });
  }
});

/**
 * PATCH /api/operator/orders/:id/accept
 * Transitions order status from PLACED to ACCEPTED, recording acceptedAt and acceptedByOperatorId.
 * Rejects with 409 Conflict if order is already ACCEPTED or in any non-PLACED state.
 * AC-15, AC-16 / BR-04 / FR-10 / TEST-19, TEST-20
 */
operatorOrdersRouter.patch("/:id/accept", async (req: Request, res: Response) => {
  try {
    const id = Number(req.params.id);
    if (isNaN(id)) {
      return res.status(400).json({ error: "Invalid order ID" });
    }

    const order = await prisma.order.findUnique({
      where: { id },
      include: {
        customer: {
          select: {
            id: true,
            email: true,
            name: true,
          },
        },
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

    // State machine guard: only PLACED orders can be transitioned to ACCEPTED
    if (order.status !== "PLACED") {
      return res.status(409).json({
        error: `Order cannot be accepted from current status (${order.status}). Order is already accepted or finalized.`,
      });
    }

    // Atomic update of status, timestamp, and operator identity
    const updated = await prisma.order.update({
      where: { id },
      data: {
        status: "ACCEPTED",
        acceptedAt: new Date(),
        acceptedByOperatorId: req.user!.id,
      },
      include: {
        customer: {
          select: {
            id: true,
            email: true,
            name: true,
          },
        },
        items: {
          include: {
            product: true,
          },
        },
      },
    });

    return res.status(200).json({ order: updated });
  } catch (err: any) {
    return res.status(500).json({ error: "Failed to accept order: " + (err?.message || "Internal error") });
  }
});
