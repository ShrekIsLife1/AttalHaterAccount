import { describe, it, expect, beforeAll, afterAll, beforeEach } from "vitest";
import request from "supertest";
import { app } from "../../src/app.js";
import { getPrisma } from "../../src/prisma.js";
import { runSeed } from "../../prisma/seed.js";

const prisma = getPrisma();

describe("E2E Integration & Complete Workflow Journey (AC-19, AC-20 / TEST-24, TEST-25, TEST-26)", () => {
  const seedPassword = process.env.SEED_PASSWORD || "password123";

  beforeAll(async () => {
    await prisma.$connect();
    await runSeed();
  });

  beforeEach(async () => {
    await runSeed();
  });

  afterAll(async () => {
    await prisma.$disconnect();
  });

  describe("TEST-24: Complete Customer Purchasing Journey (AC-19 / F-01..F-04)", () => {
    it("completes full flow: customer login -> browse catalog -> place multi-item order -> verify DB stock decrement -> verify order in My Orders", async () => {
      // Step 1: Customer Authentication
      const loginRes = await request(app)
        .post("/api/auth/login")
        .send({ email: "customer1@example.com", password: seedPassword });

      expect(loginRes.status).toBe(200);
      expect(loginRes.body.user).toMatchObject({
        email: "customer1@example.com",
        role: "CUSTOMER"
      });

      const cookies = loginRes.headers["set-cookie"];
      const customerCookie = Array.isArray(cookies)
        ? cookies.find((c: string) => c.startsWith("sid=")) || cookies[0]
        : cookies;
      expect(customerCookie).toBeDefined();

      // Step 2: Browse active catalog & check available products
      const catalogRes = await request(app)
        .get("/api/products")
        .set("Cookie", customerCookie);

      expect(catalogRes.status).toBe(200);
      expect(Array.isArray(catalogRes.body)).toBe(true);

      const hoodie = catalogRes.body.find((p: any) => p.name.includes("Hoodie"));
      const tshirt = catalogRes.body.find((p: any) => p.name.includes("T-Shirt"));
      expect(hoodie).toBeDefined();
      expect(tshirt).toBeDefined();

      const initialHoodieStock = hoodie.stockQuantity;
      const initialTshirtStock = tshirt.stockQuantity;
      expect(initialHoodieStock).toBeGreaterThanOrEqual(2);
      expect(initialTshirtStock).toBeGreaterThanOrEqual(3);

      // Step 3: Place multi-item order
      const orderPayload = {
        items: [
          { productId: hoodie.id, quantity: 2 },
          { productId: tshirt.id, quantity: 3 }
        ]
      };

      const placeRes = await request(app)
        .post("/api/orders")
        .set("Cookie", customerCookie)
        .send(orderPayload);

      expect(placeRes.status).toBe(201);
      expect(placeRes.body).toHaveProperty("order");
      const order = placeRes.body.order;

      expect(order.status).toBe("PLACED");
      const expectedTotal = hoodie.priceMinor * 2 + tshirt.priceMinor * 3;
      expect(order.totalMinor).toBe(expectedTotal);
      expect(order.items).toHaveLength(2);

      // Verify price snapshot in order line items
      const hoodieLine = order.items.find((i: any) => i.productId === hoodie.id);
      const tshirtLine = order.items.find((i: any) => i.productId === tshirt.id);
      expect(hoodieLine.unitPriceAtOrder).toBe(hoodie.priceMinor);
      expect(tshirtLine.unitPriceAtOrder).toBe(tshirt.priceMinor);

      // Step 4: Verify atomic stock decrement directly in PostgreSQL database
      const dbHoodie = await prisma.product.findUnique({ where: { id: hoodie.id } });
      const dbTshirt = await prisma.product.findUnique({ where: { id: tshirt.id } });
      expect(dbHoodie!.stockQuantity).toBe(initialHoodieStock - 2);
      expect(dbTshirt!.stockQuantity).toBe(initialTshirtStock - 3);

      // Step 5: Customer reviews My Orders list
      const ordersListRes = await request(app)
        .get("/api/orders")
        .set("Cookie", customerCookie);

      expect(ordersListRes.status).toBe(200);
      const customerOrders = ordersListRes.body.orders;
      expect(Array.isArray(customerOrders)).toBe(true);

      const foundOrder = customerOrders.find((o: any) => o.id === order.id);
      expect(foundOrder).toBeDefined();
      expect(foundOrder.status).toBe("PLACED");
      expect(foundOrder.totalMinor).toBe(expectedTotal);

      // Step 6: Customer views order detail by ID
      const orderDetailRes = await request(app)
        .get(`/api/orders/${order.id}`)
        .set("Cookie", customerCookie);

      expect(orderDetailRes.status).toBe(200);
      expect(orderDetailRes.body.order.id).toBe(order.id);
      expect(orderDetailRes.body.order.status).toBe("PLACED");
    });
  });

  describe("TEST-25: Complete Operator Order Processing Journey (AC-19 / F-05)", () => {
    it("completes full flow: customer places order -> operator logs in -> views queue -> accepts order -> order status is ACCEPTED in DB and customer view", async () => {
      // Step 1: Customer logs in & places an order
      const custLogin = await request(app)
        .post("/api/auth/login")
        .send({ email: "customer2@example.com", password: seedPassword });
      const custCookies = custLogin.headers["set-cookie"];
      const customerCookie = Array.isArray(custCookies)
        ? custCookies.find((c: string) => c.startsWith("sid=")) || custCookies[0]
        : custCookies;

      const product = await prisma.product.findFirst({ where: { isActive: true, stockQuantity: { gt: 5 } } });

      const placeRes = await request(app)
        .post("/api/orders")
        .set("Cookie", customerCookie)
        .send({ items: [{ productId: product!.id, quantity: 2 }] });

      expect(placeRes.status).toBe(201);
      const placedOrderId = placeRes.body.order.id;

      // Step 2: Operator logs in
      const opLogin = await request(app)
        .post("/api/auth/login")
        .send({ email: "operator1@example.com", password: seedPassword });

      expect(opLogin.status).toBe(200);
      expect(opLogin.body.user.role).toBe("OPERATOR");
      const opCookies = opLogin.headers["set-cookie"];
      const operatorCookie = Array.isArray(opCookies)
        ? opCookies.find((c: string) => c.startsWith("sid=")) || opCookies[0]
        : opCookies;

      // Step 3: Operator views incoming queue
      const queueRes = await request(app)
        .get("/api/operator/orders")
        .set("Cookie", operatorCookie);

      expect(queueRes.status).toBe(200);
      expect(Array.isArray(queueRes.body)).toBe(true);

      const targetOrder = queueRes.body.find((o: any) => o.id === placedOrderId);
      expect(targetOrder).toBeDefined();
      expect(targetOrder.status).toBe("PLACED");

      // Step 4: Operator accepts order
      const acceptRes = await request(app)
        .patch(`/api/operator/orders/${placedOrderId}/accept`)
        .set("Cookie", operatorCookie);

      expect(acceptRes.status).toBe(200);
      expect(acceptRes.body.order.status).toBe("ACCEPTED");
      expect(acceptRes.body.order.acceptedAt).toBeDefined();
      expect(acceptRes.body.order.acceptedByOperatorId).toBe(opLogin.body.user.id);

      // Step 5: Verify order disappears from the incoming PLACED queue
      const updatedQueueRes = await request(app)
        .get("/api/operator/orders")
        .set("Cookie", operatorCookie);

      const stillInQueue = updatedQueueRes.body.find((o: any) => o.id === placedOrderId);
      expect(stillInQueue).toBeUndefined();

      // Step 6: Verify customer sees updated ACCEPTED status on reload
      const custDetailRes = await request(app)
        .get(`/api/orders/${placedOrderId}`)
        .set("Cookie", customerCookie);

      expect(custDetailRes.status).toBe(200);
      expect(custDetailRes.body.order.status).toBe("ACCEPTED");
      expect(custDetailRes.body.order.acceptedAt).not.toBeNull();
    });
  });

  describe("TEST-26: Access Boundaries & Failure Guard Rails (AC-20 / BR-04, BR-08, NFR-01)", () => {
    it("enforces access boundaries: unauthenticated access redirects/401, customer role forbidden from operator queue, out-of-stock atomic rejection", async () => {
      // 1. Unauthenticated access rejected with 401
      const unauthGet = await request(app).get("/api/orders");
      expect(unauthGet.status).toBe(401);

      const unauthOp = await request(app).get("/api/operator/orders");
      expect(unauthOp.status).toBe(401);

      // 2. Customer login
      const custLogin = await request(app)
        .post("/api/auth/login")
        .send({ email: "customer3@example.com", password: seedPassword });
      const custCookies = custLogin.headers["set-cookie"];
      const customerCookie = Array.isArray(custCookies)
        ? custCookies.find((c: string) => c.startsWith("sid=")) || custCookies[0]
        : custCookies;

      // 3. Customer role forbidden from operator queue and actions (403)
      const custToOpQueue = await request(app)
        .get("/api/operator/orders")
        .set("Cookie", customerCookie);
      expect(custToOpQueue.status).toBe(403);

      const custToOpAccept = await request(app)
        .patch("/api/operator/orders/1/accept")
        .set("Cookie", customerCookie);
      expect(custToOpAccept.status).toBe(403);

      // 4. Out-of-stock / excessive quantity submission rejected with 400 and zero DB change
      const soldOutProduct = await prisma.product.findFirst({ where: { stockQuantity: 0 } });
      const activeProduct = await prisma.product.findFirst({ where: { isActive: true, stockQuantity: { gt: 0 } } });

      const initialActiveStock = activeProduct!.stockQuantity;
      const initialOrderCount = await prisma.order.count();

      const outOfStockRes = await request(app)
        .post("/api/orders")
        .set("Cookie", customerCookie)
        .send({
          items: [
            { productId: activeProduct!.id, quantity: 1 },
            { productId: soldOutProduct!.id, quantity: 1 }
          ]
        });

      expect(outOfStockRes.status).toBe(400);
      expect(outOfStockRes.body).toHaveProperty("error");
      expect(outOfStockRes.body.error).toMatch(/Insufficient stock/i);

      // Verify zero DB changes: stock untouched, no partial order created
      const currentActiveStock = await prisma.product.findUnique({ where: { id: activeProduct!.id } });
      expect(currentActiveStock!.stockQuantity).toBe(initialActiveStock);

      const currentOrderCount = await prisma.order.count();
      expect(currentOrderCount).toBe(initialOrderCount);

      // 5. Ownership isolation: cannot view another customer's order (returns 404 without leaking existence)
      // Create order for customer1
      const orderCust1 = await prisma.order.create({
        data: {
          customerId: 1, // customer1
          status: "PLACED",
          totalMinor: 5000,
          items: {
            create: [{ productId: activeProduct!.id, quantity: 1, unitPriceAtOrder: 5000 }]
          }
        }
      });

      // Customer 3 attempts to view customer 1's order
      const crossViewRes = await request(app)
        .get(`/api/orders/${orderCust1.id}`)
        .set("Cookie", customerCookie);

      expect(crossViewRes.status).toBe(404);
      expect(crossViewRes.body).toHaveProperty("error");
      expect(crossViewRes.body.error).toBe("Order not found");
    });
  });
});
