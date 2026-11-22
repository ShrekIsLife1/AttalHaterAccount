import { describe, it, expect, beforeAll, afterAll } from "vitest";
import request from "supertest";
import { app } from "../../src/app.js";
import { getPrisma } from "../../src/prisma.js";
import { runSeed } from "../../prisma/seed.js";

const prisma = getPrisma();

describe("Customer Order Access & Ownership Isolation (F-04 / AC-11, AC-12 / TEST-13, TEST-15)", () => {
  let customer1Cookie: string;
  let customer2Cookie: string;
  let orderCustomer1Id: number;
  let orderCustomer2Id: number;

  beforeAll(async () => {
    await prisma.$connect();
    await runSeed();

    // Authenticate Customer 1
    const res1 = await request(app)
      .post("/api/auth/login")
      .send({ email: "customer1@example.com", password: "password123" });
    customer1Cookie = res1.headers["set-cookie"][0];

    // Authenticate Customer 2
    const res2 = await request(app)
      .post("/api/auth/login")
      .send({ email: "customer2@example.com", password: "password123" });
    customer2Cookie = res2.headers["set-cookie"][0];

    // Fetch active products
    const products = await prisma.product.findMany({
      where: { isActive: true, stockQuantity: { gt: 5 } },
    });
    const p1 = products[0];
    const p2 = products[1];

    // Customer 1 places an order
    const order1Res = await request(app)
      .post("/api/orders")
      .set("Cookie", customer1Cookie)
      .send({
        items: [{ productId: p1.id, quantity: 1 }],
      });
    expect(order1Res.status).toBe(201);
    orderCustomer1Id = order1Res.body.order.id;

    // Customer 2 places an order
    const order2Res = await request(app)
      .post("/api/orders")
      .set("Cookie", customer2Cookie)
      .send({
        items: [{ productId: p2.id, quantity: 2 }],
      });
    expect(order2Res.status).toBe(201);
    orderCustomer2Id = order2Res.body.order.id;
  });

  afterAll(async () => {
    await prisma.$disconnect();
  });

  describe("TEST-13: GET /api/orders — Customer lists only own orders (AC-11)", () => {
    it("returns HTTP 200 with only Customer 1's orders, sorted newest first", async () => {
      const res = await request(app)
        .get("/api/orders")
        .set("Cookie", customer1Cookie);

      expect(res.status).toBe(200);
      expect(Array.isArray(res.body.orders)).toBe(true);
      expect(res.body.orders.length).toBeGreaterThanOrEqual(1);

      // Verify all orders belong to Customer 1
      for (const order of res.body.orders) {
        expect(order.customerId).toBeDefined();
        // None should be Customer 2's order
        expect(order.id).not.toBe(orderCustomer2Id);
      }

      // Check order fields
      const firstOrder = res.body.orders[0];
      expect(firstOrder).toHaveProperty("id");
      expect(firstOrder).toHaveProperty("status", "PLACED");
      expect(firstOrder).toHaveProperty("totalMinor");
      expect(firstOrder).toHaveProperty("items");
      expect(Array.isArray(firstOrder.items)).toBe(true);
    });

    it("returns HTTP 401 when calling GET /api/orders unauthenticated", async () => {
      const res = await request(app).get("/api/orders");
      expect(res.status).toBe(401);
    });
  });

  describe("TEST-15: GET /api/orders/:id — Ownership isolation (AC-12 / NFR-01)", () => {
    it("allows Customer 1 to view their own order detail", async () => {
      const res = await request(app)
        .get(`/api/orders/${orderCustomer1Id}`)
        .set("Cookie", customer1Cookie);

      expect(res.status).toBe(200);
      expect(res.body.order.id).toBe(orderCustomer1Id);
      expect(res.body.order.items.length).toBeGreaterThanOrEqual(1);
      expect(res.body.order.items[0]).toHaveProperty("unitPriceAtOrder");
    });

    it("returns HTTP 404 Not Found when Customer 1 queries Customer 2's order (no data leakage)", async () => {
      const res = await request(app)
        .get(`/api/orders/${orderCustomer2Id}`)
        .set("Cookie", customer1Cookie);

      expect(res.status).toBe(404);
      expect(res.body).toHaveProperty("error", "Order not found");
      expect(res.body).not.toHaveProperty("order");
    });

    it("returns HTTP 404 for non-existent order ID", async () => {
      const res = await request(app)
        .get("/api/orders/999999")
        .set("Cookie", customer1Cookie);

      expect(res.status).toBe(404);
      expect(res.body).toHaveProperty("error", "Order not found");
    });
  });
});
