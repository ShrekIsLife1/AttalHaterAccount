import { Router, Request, Response } from "express";
import { getPrisma } from "../prisma.js";
// No auth import needed — catalog is public per F-02 contract

export const productsRouter = Router();

const prisma = getPrisma();

/**
 * GET /api/products
 * F-02 / AC-05 — Return all active products with stock availability.
 * Access: authenticated users (CUSTOMER or OPERATOR).
 */
productsRouter.get("/", async (_req: Request, res: Response) => {
  try {
    const products = await prisma.product.findMany({
      where: { isActive: true },
      orderBy: { name: "asc" },
      select: {
        id: true,
        name: true,
        description: true,
        priceMinor: true,
        stockQuantity: true,
        isActive: true
      }
    });

    res.status(200).json(products);
  } catch (err) {
    console.error("[GET /api/products] Database error:", err);
    res.status(500).json({ error: "Internal server error" });
  }
});
