import { describe, it, expect, beforeAll, afterAll, beforeEach } from "vitest";
import request from "supertest";
import { app } from "../../src/app.js";
import { getPrisma } from "../../src/prisma.js";
import { runSeed } from "../../prisma/seed.js";

const prisma = getPrisma();

describe("Order Placement API (F-03 / AC-06..AC-10 / TEST-07, TEST-08, TEST-10, TEST-11, TEST-12)", () => {
  let customerCookie: string;
  let operatorCookie: string;
  let activeProduct1: any;
  let activeProduct2: any;
  let inactiveProduct: any;
  let zeroStockProduct: any;

  beforeAll(async () => {
    await prisma.$connect();
    await runSeed();

    // Login customer1
    const custRes = await request(app)
      .post("/api/auth/login")
      .send({ email: "customer1@example.com", password: process.env.SEED_PASSWORD || "password123" });
    const custCookies = custRes.headers["set-cookie"];
    customerCookie = Array.isArray(custCookies)
      ? custCookies.find((c: string) => c.startsWith("sid=")) || custCookies[0]
      : custCookies;

    // Login operator1
    const opRes = await request(app)
      .post("/api/auth/login")
      .send({ email: "operator1@example.com", password: process.env.SEED_PASSWORD || "password123" });
    const opCookies = opRes.headers["set-cookie"];
    operatorCookie = Array.isArray(opCookies)
      ? opCookies.find((c: string) => c.startsWith("sid=")) || opCookies[0]
      : opCookies;
  });

  beforeEach(async () => {
    // Reset seed before each test to ensure deterministic stock counts
    await runSeed();

    // Retrieve product IDs
    activeProduct1 = await prisma.product.findFirst({
      where: { isActive: true, stockQuantity: { gt: 5 } }
    });
    activeProduct2 = await prisma.product.findFirst({
      where: { isActive: true, id: { not: activeProduct1.id } }
    });
    inactiveProduct = await prisma.product.findFirst({
      where: { isActive: false }
    });
    zeroStockProduct = await prisma.product.findFirst({
      where: { stockQuantity: 0 }
    });
  });

  afterAll(async () => {
    await prisma.$disconnect();
  });

  describe("TEST-07: Valid multi-item order placement & atomic stock decrement (AC-06)", () => {
    it("creates an order in PLACED status, snapshots prices, and atomically decrements inventory", async () => {
      const initialStock1 = activeProduct1.stockQuantity;
      const initialStock2 = activeProduct2.stockQuantity;

      const orderPayload = {
        items: [
          { productId: activeProduct1.id, quantity: 2 },
          { productId: activeProduct2.id, quantity: 1 }
        ]
      };

      const res = await request(app)
        .post("/api/orders")
        .set("Cookie", customerCookie)
        .send(orderPayload);

      expect(res.status).toBe(201);
      expect(res.body).toHaveProperty("order");
      const order = res.body.order;

      expect(order.status).toBe("PLACED");
      const expectedTotal =
        activeProduct1.priceMinor * 2 + activeProduct2.priceMinor * 1;
      expect(order.totalMinor).toBe(expectedTotal);

      // Verify line items and price snapshots
      expect(order.items).toHaveLength(2);
      const line1 = order.items.find(
        (i: any) => i.productId === activeProduct1.id
      );
      expect(line1.quantity).toBe(2);
      expect(line1.unitPriceAtOrder).toBe(activeProduct1.priceMinor);

      // Verify atomic inventory decrement in PostgreSQL
      const updatedP1 = await prisma.product.findUnique({
        where: { id: activeProduct1.id }
      });
      const updatedP2 = await prisma.product.findUnique({
        where: { id: activeProduct2.id }
      });

      expect(updatedP1?.stockQuantity).toBe(initialStock1 - 2);
      expect(updatedP2?.stockQuantity).toBe(initialStock2 - 1);
    });
  });

  describe("TEST-08: Authoritative server pricing (AC-07 / BR-03)", () => {
    it("ignores client-sent total, price, unitPrice, or customerId and recalculates from DB", async () => {
      const forgedPayload = {
        items: [{ productId: activeProduct1.id, quantity: 2 }],
        totalMinor: 100, // Client tries to pay 1 THB
        price: 50,
        customerId: 999999,
        status: "COMPLETED"
      };

      const res = await request(app)
        .post("/api/orders")
        .set("Cookie", customerCookie)
        .send(forgedPayload);

      expect(res.status).toBe(201);
      const order = res.body.order;

      const authoritativeTotal = activeProduct1.priceMinor * 2;
      expect(order.totalMinor).toBe(authoritativeTotal);
      expect(order.totalMinor).not.toBe(100);
      expect(order.status).toBe("PLACED");
    });
  });

  describe("TEST-10: Order line constraint validation (AC-08 / BR-06)", () => {
    it("rejects empty items array with HTTP 400", async () => {
      const res = await request(app)
        .post("/api/orders")
        .set("Cookie", customerCookie)
        .send({ items: [] });

      expect(res.status).toBe(400);
      expect(res.body).toHaveProperty("error");
    });

    it("rejects invalid quantities (0, negative, > 10) with HTTP 400", async () => {
      const resZero = await request(app)
        .post("/api/orders")
        .set("Cookie", customerCookie)
        .send({ items: [{ productId: activeProduct1.id, quantity: 0 }] });
      expect(resZero.status).toBe(400);

      const resNeg = await request(app)
        .post("/api/orders")
        .set("Cookie", customerCookie)
        .send({ items: [{ productId: activeProduct1.id, quantity: -1 }] });
      expect(resNeg.status).toBe(400);

      const resOver = await request(app)
        .post("/api/orders")
        .set("Cookie", customerCookie)
        .send({ items: [{ productId: activeProduct1.id, quantity: 15 }] });
      expect(resOver.status).toBe(400);
    });

    it("rejects duplicate product lines in a single order payload with HTTP 400", async () => {
      const res = await request(app)
        .post("/api/orders")
        .set("Cookie", customerCookie)
        .send({
          items: [
            { productId: activeProduct1.id, quantity: 1 },
            { productId: activeProduct1.id, quantity: 2 }
          ]
        });

      expect(res.status).toBe(400);
    });
  });

  describe("TEST-11: Rejection on inactive product or stockout with atomic rollback (AC-09)", () => {
    it("rejects order containing an inactive product and creates zero order records", async () => {
      const ordersCountBefore = await prisma.order.count();

      const res = await request(app)
        .post("/api/orders")
        .set("Cookie", customerCookie)
        .send({
          items: [{ productId: inactiveProduct.id, quantity: 1 }]
        });

      expect(res.status).toBe(400);
      const ordersCountAfter = await prisma.order.count();
      expect(ordersCountAfter).toBe(ordersCountBefore);
    });

    it("rejects order when requested quantity exceeds available stock and leaves stock unchanged", async () => {
      const initialStock = activeProduct1.stockQuantity;

      const res = await request(app)
        .post("/api/orders")
        .set("Cookie", customerCookie)
        .send({
          items: [{ productId: activeProduct1.id, quantity: initialStock + 10 }]
        });

      expect(res.status).toBe(400);

      // Verify stock was not partially decremented
      const productAfter = await prisma.product.findUnique({
        where: { id: activeProduct1.id }
      });
      expect(productAfter?.stockQuantity).toBe(initialStock);
    });
  });

  describe("TEST-12: Price snapshot immutability across catalog price updates (AC-10)", () => {
    it("preserves historical unitPriceAtOrder even after product catalog price changes in DB", async () => {
      // 1. Place order
      const res = await request(app)
        .post("/api/orders")
        .set("Cookie", customerCookie)
        .send({
          items: [{ productId: activeProduct1.id, quantity: 1 }]
        });

      expect(res.status).toBe(201);
      const orderId = res.body.order.id;
      const originalPrice = activeProduct1.priceMinor;

      // 2. Mutate product price in database directly
      await prisma.product.update({
        where: { id: activeProduct1.id },
        data: { priceMinor: originalPrice + 50000 }
      });

      // 3. Fetch past order detail
      const fetchRes = await request(app)
        .get(`/api/orders/${orderId}`)
        .set("Cookie", customerCookie);

      expect(fetchRes.status).toBe(200);
      expect(fetchRes.body.order.items[0].unitPriceAtOrder).toBe(originalPrice);
      expect(fetchRes.body.order.totalMinor).toBe(originalPrice);
    });
  });

  describe("Role & Authentication Restrictions (BR-08 / NFR-01)", () => {
    it("returns HTTP 401 when unauthenticated", async () => {
      const res = await request(app)
        .post("/api/orders")
        .send({ items: [{ productId: activeProduct1.id, quantity: 1 }] });

      expect(res.status).toBe(401);
    });

    it("returns HTTP 403 when an OPERATOR attempts to place an order", async () => {
      const res = await request(app)
        .post("/api/orders")
        .set("Cookie", operatorCookie)
        .send({ items: [{ productId: activeProduct1.id, quantity: 1 }] });

      expect(res.status).toBe(403);
    });
  });
});
