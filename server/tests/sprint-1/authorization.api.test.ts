import { describe, it, expect, beforeAll, afterAll } from "vitest";
import request from "supertest";
import { app } from "../../src/app.js";
import { getPrisma } from "../../src/prisma.js";
import { runSeed } from "../../prisma/seed.js";

const prisma = getPrisma();

describe("Issue #13: Cross-Cutting Authorization Hardening & Permission Matrix (AC-03, AC-12, AC-13, AC-17 / NFR-01, BR-05, BR-07, BR-08)", () => {
  let customer1Cookie: string;
  let customer2Cookie: string;
  let operatorCookie: string;
  let customer1Id: number;
  let customer2Id: number;
  let operatorId: number;
  let orderCustomer1Id: number;
  let orderCustomer2Id: number;
  let testProductId: number;

  beforeAll(async () => {
    await prisma.$connect();
    await runSeed();

    // Authenticate Customer 1
    const res1 = await request(app)
      .post("/api/auth/login")
      .send({ email: "customer1@example.com", password: "password123" });
    customer1Cookie = res1.headers["set-cookie"][0];
    customer1Id = res1.body.user.id;

    // Authenticate Customer 2
    const res2 = await request(app)
      .post("/api/auth/login")
      .send({ email: "customer2@example.com", password: "password123" });
    customer2Cookie = res2.headers["set-cookie"][0];
    customer2Id = res2.body.user.id;

    // Authenticate Operator 1
    const resOp = await request(app)
      .post("/api/auth/login")
      .send({ email: "operator1@example.com", password: "password123" });
    operatorCookie = resOp.headers["set-cookie"][0];
    operatorId = resOp.body.user.id;

    // Locate active product
    const p = await prisma.product.findFirst({
      where: { isActive: true, stockQuantity: { gte: 10 } },
    });
    testProductId = p!.id;

    // Create order for Customer 1
    const o1 = await request(app)
      .post("/api/orders")
      .set("Cookie", customer1Cookie)
      .send({ items: [{ productId: testProductId, quantity: 1 }] });
    orderCustomer1Id = o1.body.order.id;

    // Create order for Customer 2
    const o2 = await request(app)
      .post("/api/orders")
      .set("Cookie", customer2Cookie)
      .send({ items: [{ productId: testProductId, quantity: 1 }] });
    orderCustomer2Id = o2.body.order.id;
  });

  afterAll(async () => {
    await prisma.$disconnect();
  });

  // 1. Unauthenticated checks across all protected endpoints (401)
  describe("1. Unauthenticated Access Protection (HTTP 401)", () => {
    it("rejects GET /api/auth/me without session cookie", async () => {
      const res = await request(app).get("/api/auth/me");
      expect(res.status).toBe(401);
      expect(res.body).toHaveProperty("error");
    });

    it("rejects POST /api/orders without session cookie", async () => {
      const res = await request(app)
        .post("/api/orders")
        .send({ items: [{ productId: testProductId, quantity: 1 }] });
      expect(res.status).toBe(401);
    });

    it("rejects GET /api/orders without session cookie", async () => {
      const res = await request(app).get("/api/orders");
      expect(res.status).toBe(401);
    });

    it("rejects GET /api/orders/:id without session cookie", async () => {
      const res = await request(app).get(`/api/orders/${orderCustomer1Id}`);
      expect(res.status).toBe(401);
    });

    it("rejects GET /api/operator/orders without session cookie", async () => {
      const res = await request(app).get("/api/operator/orders");
      expect(res.status).toBe(401);
    });

    it("rejects PATCH /api/operator/orders/:id/accept without session cookie", async () => {
      const res = await request(app).patch(`/api/operator/orders/${orderCustomer1Id}/accept`);
      expect(res.status).toBe(401);
    });

    it("rejects request with forged / invalid cookie token", async () => {
      const res = await request(app)
        .get("/api/auth/me")
        .set("Cookie", "sid=deadbeefcafebabe0000000000000000");
      expect(res.status).toBe(401);
    });
  });

  // 2. Role-Based Access Control (403 vs 200)
  describe("2. Role-Based Access Control Segregation (HTTP 403)", () => {
    it("Customer calling operator queue GET /api/operator/orders returns 403 Forbidden", async () => {
      const res = await request(app)
        .get("/api/operator/orders")
        .set("Cookie", customer1Cookie);
      expect(res.status).toBe(403);
      expect(res.body).toHaveProperty("error");
    });

    it("Customer calling operator accept PATCH /api/operator/orders/:id/accept returns 403 Forbidden", async () => {
      const res = await request(app)
        .patch(`/api/operator/orders/${orderCustomer1Id}/accept`)
        .set("Cookie", customer1Cookie);
      expect(res.status).toBe(403);
    });

    it("Operator attempting customer order creation POST /api/orders returns 403 Forbidden", async () => {
      const res = await request(app)
        .post("/api/orders")
        .set("Cookie", operatorCookie)
        .send({ items: [{ productId: testProductId, quantity: 1 }] });
      expect(res.status).toBe(403);
      expect(res.body).toHaveProperty("error");
    });

    it("Operator attempting customer order list GET /api/orders returns 403 Forbidden", async () => {
      const res = await request(app)
        .get("/api/orders")
        .set("Cookie", operatorCookie);
      expect(res.status).toBe(403);
    });

    it("Operator is allowed to view any customer order detail GET /api/orders/:id (HTTP 200)", async () => {
      const res = await request(app)
        .get(`/api/orders/${orderCustomer1Id}`)
        .set("Cookie", operatorCookie);
      expect(res.status).toBe(200);
      expect(res.body.order.id).toBe(orderCustomer1Id);
    });
  });

  // 3. Customer Ownership Isolation (404 Not Found & Zero Data Leakage)
  describe("3. Customer Order Ownership Isolation (AC-12 / NFR-01 / BR-05)", () => {
    it("Customer A requesting Customer B's order returns 404 Not Found without leaking metadata", async () => {
      const res = await request(app)
        .get(`/api/orders/${orderCustomer2Id}`)
        .set("Cookie", customer1Cookie);

      // Must be 404 (not 403) to avoid confirming order existence
      expect(res.status).toBe(404);
      expect(res.body).toHaveProperty("error", "Order not found");
      expect(res.body).not.toHaveProperty("order");
      expect(res.body).not.toHaveProperty("items");
      expect(res.body).not.toHaveProperty("customerId");
    });

    it("Customer B requesting Customer A's order returns identical generic 404", async () => {
      const res = await request(app)
        .get(`/api/orders/${orderCustomer1Id}`)
        .set("Cookie", customer2Cookie);

      expect(res.status).toBe(404);
      expect(res.body).toHaveProperty("error", "Order not found");
    });
  });

  // 4. Client Price/Total Tampering Rejection
  describe("4. Tampering Protection with Server-Authoritative Totals (AC-07 / BR-03)", () => {
    it("ignores forged prices and totals submitted by the client and uses database prices", async () => {
      const res = await request(app)
        .post("/api/orders")
        .set("Cookie", customer1Cookie)
        .send({
          items: [
            {
              productId: testProductId,
              quantity: 1,
              price: 1, // Tampered price
              unitPriceAtOrder: 1, // Tampered snapshot
              totalMinor: 1, // Tampered total
            },
          ],
          totalMinor: 10, // Tampered grand total
        });

      expect(res.status).toBe(201);
      const product = await prisma.product.findUnique({ where: { id: testProductId } });
      // Grand total must match authoritative database price
      expect(res.body.order.totalMinor).toBe(product!.priceMinor);
      expect(res.body.order.items[0].unitPriceAtOrder).toBe(product!.priceMinor);
    });
  });

  // 5. Inactive Account & Session Lifecycle Invalidation
  describe("5. Inactive Accounts & Session Lifecycle Invalidation (BR-07, BR-08)", () => {
    it("rejects login attempt for a deactivated account with generic 401", async () => {
      // Create an inactive user
      const inactiveUser = await prisma.user.create({
        data: {
          email: "inactive-auth-test@example.com",
          name: "Inactive User",
          passwordHash: "$2a$10$wT0XqX1XzTz8WkUqXoO5.uH5Ea.K9t2.5F1G5k1H9q.Q0G1B0F1Xm",
          role: "CUSTOMER",
          isActive: false,
        },
      });

      const res = await request(app)
        .post("/api/auth/login")
        .send({ email: "inactive-auth-test@example.com", password: "password123" });

      expect(res.status).toBe(401);
      expect(res.body.error).toBe("Invalid email or password");

      await prisma.user.delete({ where: { id: inactiveUser.id } });
    });

    it("rejects subsequent requests immediately when an active user account is deactivated in database", async () => {
      // Create temporary active user & login
      const tempUser = await prisma.user.create({
        data: {
          email: "temp-deactivate@example.com",
          name: "Temp Deactivate",
          // password: "password123" hashed
          passwordHash: await import("bcryptjs").then((b) => b.hash("password123", 10)),
          role: "CUSTOMER",
          isActive: true,
        },
      });

      const loginRes = await request(app)
        .post("/api/auth/login")
        .send({ email: "temp-deactivate@example.com", password: "password123" });
      const tempCookie = loginRes.headers["set-cookie"][0];

      // Verify active session works
      const meResBefore = await request(app)
        .get("/api/auth/me")
        .set("Cookie", tempCookie);
      expect(meResBefore.status).toBe(200);

      // Now deactivate user in DB
      await prisma.user.update({
        where: { id: tempUser.id },
        data: { isActive: false },
      });

      // Subsequent call must be rejected with 401
      const meResAfter = await request(app)
        .get("/api/auth/me")
        .set("Cookie", tempCookie);
      expect(meResAfter.status).toBe(401);

      // Cleanup
      await prisma.session.deleteMany({ where: { userId: tempUser.id } });
      await prisma.user.delete({ where: { id: tempUser.id } });
    });

    it("rejects requests after user logs out and deletes session from database", async () => {
      // Customer 1 logs out
      const logoutRes = await request(app)
        .post("/api/auth/logout")
        .set("Cookie", customer1Cookie);
      expect(logoutRes.status).toBe(200);

      // Calling /me with that logged-out cookie must return 401
      const meRes = await request(app)
        .get("/api/auth/me")
        .set("Cookie", customer1Cookie);
      expect(meRes.status).toBe(401);
    });
  });
});
