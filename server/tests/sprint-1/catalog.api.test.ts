import { describe, it, expect, beforeAll, afterAll } from "vitest";
import request from "supertest";
import { app } from "../../src/app.js";
import { getPrisma } from "../../src/prisma.js";
import { runSeed } from "../../prisma/seed.js";

const prisma = getPrisma();

describe("Product Catalog API (F-02 / AC-05 / TEST-05)", () => {
  beforeAll(async () => {
    await prisma.$connect();
    await runSeed();
  });

  afterAll(async () => {
    await prisma.$disconnect();
  });

  describe("TEST-05: GET /api/products — active catalog with stock availability (AC-05)", () => {
    it("returns HTTP 200 with an array of active products", async () => {
      const res = await request(app).get("/api/products");

      expect(res.status).toBe(200);
      expect(Array.isArray(res.body)).toBe(true);
      expect(res.body.length).toBeGreaterThan(0);
    });

    it("returns integer priceMinor and stockQuantity for each product", async () => {
      const res = await request(app).get("/api/products");

      expect(res.status).toBe(200);
      for (const product of res.body) {
        expect(typeof product.priceMinor).toBe("number");
        expect(Number.isInteger(product.priceMinor)).toBe(true);
        expect(product.priceMinor).toBeGreaterThan(0);

        expect(typeof product.stockQuantity).toBe("number");
        expect(Number.isInteger(product.stockQuantity)).toBe(true);
        expect(product.stockQuantity).toBeGreaterThanOrEqual(0);
      }
    });

    it("returns expected product fields (id, name, description, priceMinor, stockQuantity, isActive)", async () => {
      const res = await request(app).get("/api/products");

      expect(res.status).toBe(200);
      const product = res.body[0];
      expect(product).toHaveProperty("id");
      expect(product).toHaveProperty("name");
      expect(product).toHaveProperty("priceMinor");
      expect(product).toHaveProperty("stockQuantity");
      expect(product).toHaveProperty("isActive");
    });

    it("only returns active products (isActive=true); inactive products are omitted", async () => {
      // Insert an inactive product directly
      const inactive = await prisma.product.create({
        data: {
          name: "INACTIVE_TEST_PRODUCT",
          description: "Should not appear in catalog",
          priceMinor: 99999,
          stockQuantity: 100,
          isActive: false
        }
      });

      const res = await request(app).get("/api/products");

      expect(res.status).toBe(200);
      const ids = res.body.map((p: { id: number }) => p.id);
      expect(ids).not.toContain(inactive.id);

      // All returned items are active
      for (const product of res.body) {
        expect(product.isActive).toBe(true);
      }

      // Cleanup
      await prisma.product.delete({ where: { id: inactive.id } });
    });

    it("includes out-of-stock products (stockQuantity=0) in the response", async () => {
      // Insert a zero-stock product
      const outOfStock = await prisma.product.create({
        data: {
          name: "OUT_OF_STOCK_TEST_PRODUCT",
          description: "Active but no stock",
          priceMinor: 50000,
          stockQuantity: 0,
          isActive: true
        }
      });

      const res = await request(app).get("/api/products");

      expect(res.status).toBe(200);
      const found = res.body.find((p: { id: number }) => p.id === outOfStock.id);
      expect(found).toBeDefined();
      expect(found.stockQuantity).toBe(0);
      expect(found.isActive).toBe(true);

      // Cleanup
      await prisma.product.delete({ where: { id: outOfStock.id } });
    });

    it("returns HTTP 200 with empty array when no active products exist", async () => {
      // Temporarily deactivate all products
      await prisma.product.updateMany({ data: { isActive: false } });

      const res = await request(app).get("/api/products");

      expect(res.status).toBe(200);
      expect(Array.isArray(res.body)).toBe(true);
      expect(res.body).toHaveLength(0);

      // Restore active products from seed
      await runSeed();
    });
  });
});
