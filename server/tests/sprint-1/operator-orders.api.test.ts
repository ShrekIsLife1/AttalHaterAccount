import { describe, it, expect, beforeAll, afterAll, beforeEach } from "vitest";
import request from "supertest";
import { app } from "../../src/app.js";
import { getPrisma } from "../../src/prisma.js";
import { runSeed } from "../../prisma/seed.js";

const prisma = getPrisma();

describe("Operator Order Queue & Single-Step Acceptance (F-05 / AC-13..AC-16 / TEST-16, TEST-17, TEST-19, TEST-20)", () => {
  let customerCookie: string;
  let operator1Cookie: string;
  let operator2Cookie: string;
  let operator1User: any;
  let customerUser: any;
  let product1: any;

  beforeAll(async () => {
    await prisma.$connect();
    await runSeed();

    const seedPassword = process.env.SEED_PASSWORD || "password123";

    // Login customer1
    const custRes = await request(app)
      .post("/api/auth/login")
      .send({ email: "customer1@example.com", password: seedPassword });
    const custCookies = custRes.headers["set-cookie"];
    customerCookie = Array.isArray(custCookies)
      ? custCookies.find((c: string) => c.startsWith("sid=")) || custCookies[0]
      : custCookies;
    customerUser = custRes.body.user;

    // Login operator1
    const op1Res = await request(app)
      .post("/api/auth/login")
      .send({ email: "operator1@example.com", password: seedPassword });
    const op1Cookies = op1Res.headers["set-cookie"];
    operator1Cookie = Array.isArray(op1Cookies)
      ? op1Cookies.find((c: string) => c.startsWith("sid=")) || op1Cookies[0]
      : op1Cookies;
    operator1User = op1Res.body.user;

    // Login operator2
    const op2Res = await request(app)
      .post("/api/auth/login")
      .send({ email: "operator2@example.com", password: seedPassword });
    const op2Cookies = op2Res.headers["set-cookie"];
    operator2Cookie = Array.isArray(op2Cookies)
      ? op2Cookies.find((c: string) => c.startsWith("sid=")) || op2Cookies[0]
      : op2Cookies;
  });

  beforeEach(async () => {
    await runSeed();
    product1 = await prisma.product.findFirst({ where: { isActive: true, stockQuantity: { gt: 5 } } });
  });

  afterAll(async () => {
    await prisma.$disconnect();
  });

  describe("TEST-16: RBAC Protection on Operator Endpoints (AC-13 / BR-08)", () => {
    it("returns HTTP 401 Unauthorized when unauthenticated for GET and PATCH", async () => {
      const getRes = await request(app).get("/api/operator/orders");
      expect(getRes.status).toBe(401);

      const patchRes = await request(app).patch("/api/operator/orders/1/accept");
      expect(patchRes.status).toBe(401);
    });

    it("returns HTTP 403 Forbidden when a CUSTOMER attempts to access GET /api/operator/orders", async () => {
      const res = await request(app)
        .get("/api/operator/orders")
        .set("Cookie", customerCookie);

      expect(res.status).toBe(403);
      expect(res.body).toHaveProperty("error");
    });

    it("returns HTTP 403 Forbidden when a CUSTOMER attempts to call PATCH /api/operator/orders/:id/accept", async () => {
      const res = await request(app)
        .patch("/api/operator/orders/1/accept")
        .set("Cookie", customerCookie);

      expect(res.status).toBe(403);
      expect(res.body).toHaveProperty("error");
    });

    it("allows authenticated OPERATOR to access GET /api/operator/orders", async () => {
      const res = await request(app)
        .get("/api/operator/orders")
        .set("Cookie", operator1Cookie);

      expect(res.status).toBe(200);
      expect(Array.isArray(res.body)).toBe(true);
    });
  });

  describe("TEST-17: Operator Orders Queue Listing (AC-14 / FR-09)", () => {
    it("returns only PLACED orders, ordered chronologically (oldest first: createdAt ASC)", async () => {
      // Create 3 orders with slight time difference
      const order1 = await prisma.order.create({
        data: {
          customerId: customerUser.id,
          status: "PLACED",
          totalMinor: 5000,
          createdAt: new Date(Date.now() - 30000), // 30s ago
          items: {
            create: [{ productId: product1.id, quantity: 1, unitPriceAtOrder: 5000 }]
          }
        }
      });

      const order2 = await prisma.order.create({
        data: {
          customerId: customerUser.id,
          status: "PLACED",
          totalMinor: 10000,
          createdAt: new Date(Date.now() - 20000), // 20s ago
          items: {
            create: [{ productId: product1.id, quantity: 2, unitPriceAtOrder: 5000 }]
          }
        }
      });

      // Also create an order that is already ACCEPTED (must NOT appear in the incoming queue)
      const acceptedOrder = await prisma.order.create({
        data: {
          customerId: customerUser.id,
          status: "ACCEPTED",
          totalMinor: 15000,
          createdAt: new Date(Date.now() - 40000), // 40s ago
          acceptedAt: new Date(Date.now() - 10000),
          acceptedByOperatorId: operator1User.id,
          items: {
            create: [{ productId: product1.id, quantity: 3, unitPriceAtOrder: 5000 }]
          }
        }
      });

      const res = await request(app)
        .get("/api/operator/orders")
        .set("Cookie", operator1Cookie);

      expect(res.status).toBe(200);
      expect(Array.isArray(res.body)).toBe(true);

      const returnedIds = res.body.map((o: any) => o.id);
      expect(returnedIds).toContain(order1.id);
      expect(returnedIds).toContain(order2.id);
      expect(returnedIds).not.toContain(acceptedOrder.id);

      // Verify chronological sorting (order1 before order2)
      const index1 = returnedIds.indexOf(order1.id);
      const index2 = returnedIds.indexOf(order2.id);
      expect(index1).toBeLessThan(index2);

      // Verify payload structure includes customer details and items
      const returnedOrder1 = res.body.find((o: any) => o.id === order1.id);
      expect(returnedOrder1.status).toBe("PLACED");
      expect(returnedOrder1.customer).toBeDefined();
      expect(returnedOrder1.customer.email).toBe(customerUser.email);
      expect(returnedOrder1.items).toHaveLength(1);
      expect(returnedOrder1.items[0].unitPriceAtOrder).toBe(5000);
    });
  });

  describe("TEST-19: Single-Step Acceptance Transition (AC-15 / BR-04 / FR-10)", () => {
    it("transitions order status from PLACED to ACCEPTED, records acceptedAt and acceptedByOperatorId", async () => {
      const order = await prisma.order.create({
        data: {
          customerId: customerUser.id,
          status: "PLACED",
          totalMinor: 75000,
          items: {
            create: [{ productId: product1.id, quantity: 1, unitPriceAtOrder: 75000 }]
          }
        }
      });

      const beforeTime = new Date();

      const res = await request(app)
        .patch(`/api/operator/orders/${order.id}/accept`)
        .set("Cookie", operator1Cookie);

      expect(res.status).toBe(200);
      expect(res.body).toHaveProperty("order");
      const updated = res.body.order;

      expect(updated.id).toBe(order.id);
      expect(updated.status).toBe("ACCEPTED");
      expect(updated.acceptedByOperatorId).toBe(operator1User.id);
      expect(updated.acceptedAt).toBeDefined();

      const acceptedTime = new Date(updated.acceptedAt);
      expect(acceptedTime.getTime()).toBeGreaterThanOrEqual(beforeTime.getTime() - 1000);

      // Verify database persistence
      const dbOrder = await prisma.order.findUnique({ where: { id: order.id } });
      expect(dbOrder!.status).toBe("ACCEPTED");
      expect(dbOrder!.acceptedByOperatorId).toBe(operator1User.id);
      expect(dbOrder!.acceptedAt).not.toBeNull();
    });
  });

  describe("TEST-20: State Machine Conflict Guard & 404 on Invalid Acceptance (AC-16 / BR-04)", () => {
    it("returns HTTP 409 Conflict when attempting to accept an already ACCEPTED order", async () => {
      // 1. Create already accepted order
      const order = await prisma.order.create({
        data: {
          customerId: customerUser.id,
          status: "ACCEPTED",
          totalMinor: 75000,
          acceptedAt: new Date(Date.now() - 5000),
          acceptedByOperatorId: operator1User.id,
          items: {
            create: [{ productId: product1.id, quantity: 1, unitPriceAtOrder: 75000 }]
          }
        }
      });

      const originalAcceptedAt = order.acceptedAt!.toISOString();

      // 2. Operator 2 attempts to accept the already accepted order
      const res = await request(app)
        .patch(`/api/operator/orders/${order.id}/accept`)
        .set("Cookie", operator2Cookie);

      expect(res.status).toBe(409);
      expect(res.body).toHaveProperty("error");
      expect(res.body.error).toMatch(/cannot be accepted|already accepted/i);

      // Verify database remains untouched (still operator 1 and original timestamp)
      const dbOrder = await prisma.order.findUnique({ where: { id: order.id } });
      expect(dbOrder!.status).toBe("ACCEPTED");
      expect(dbOrder!.acceptedByOperatorId).toBe(operator1User.id);
      expect(dbOrder!.acceptedAt!.toISOString()).toBe(originalAcceptedAt);
    });

    it("returns HTTP 404 Not Found when order ID does not exist", async () => {
      const res = await request(app)
        .patch("/api/operator/orders/999999/accept")
        .set("Cookie", operator1Cookie);

      expect(res.status).toBe(404);
      expect(res.body).toHaveProperty("error");
      expect(res.body.error).toMatch(/Order not found/i);
    });

    it("returns HTTP 400 Bad Request when order ID is not a valid number", async () => {
      const res = await request(app)
        .patch("/api/operator/orders/invalid-id/accept")
        .set("Cookie", operator1Cookie);

      expect(res.status).toBe(400);
      expect(res.body).toHaveProperty("error");
    });
  });
});
