import { describe, it, expect, beforeAll, afterAll } from "vitest";
import request from "supertest";
import { app } from "../../src/app.js";
import { getPrisma } from "../../src/prisma.js";

const prisma = getPrisma();

describe("Authentication & Session RBAC (F-01 / AC-01..AC-04, AC-13)", () => {
  const customerCredentials = {
    email: "customer1@unimerch.ac.th",
    password: "Password123!"
  };

  const operatorCredentials = {
    email: "operator1@unimerch.ac.th",
    password: "Operator123!"
  };

  beforeAll(async () => {
    // Ensure test users exist in database
    await prisma.$connect();
  });

  afterAll(async () => {
    await prisma.$disconnect();
  });

  describe("TEST-01: Valid Login (AC-01)", () => {
    it("logs in with valid customer credentials, returns safe user object, and sets HttpOnly session cookie", async () => {
      const res = await request(app)
        .post("/api/auth/login")
        .send(customerCredentials);

      expect(res.status).toBe(200);
      expect(res.body).toHaveProperty("user");
      expect(res.body.user).toMatchObject({
        email: customerCredentials.email,
        role: "CUSTOMER",
        name: "Alice Customer"
      });
      expect(res.body.user).not.toHaveProperty("passwordHash");
      expect(res.body.user).not.toHaveProperty("password");

      // Verify Set-Cookie header
      const cookies = res.headers["set-cookie"];
      expect(cookies).toBeDefined();
      const sidCookie = Array.isArray(cookies)
        ? cookies.find((c: string) => c.startsWith("sid="))
        : cookies;
      expect(sidCookie).toBeDefined();
      expect(sidCookie).toMatch(/HttpOnly/i);
      expect(sidCookie).toMatch(/Path=\//i);
    });

    it("logs in with valid operator credentials, returns OPERATOR role", async () => {
      const res = await request(app)
        .post("/api/auth/login")
        .send(operatorCredentials);

      expect(res.status).toBe(200);
      expect(res.body.user).toMatchObject({
        email: operatorCredentials.email,
        role: "OPERATOR",
        name: "Ophelia Operator"
      });
      expect(res.body.user).not.toHaveProperty("passwordHash");
    });
  });

  describe("TEST-02: Invalid Credentials & Inactive Accounts (AC-02)", () => {
    it("returns HTTP 401 with generic error on invalid password", async () => {
      const res = await request(app)
        .post("/api/auth/login")
        .send({
          email: customerCredentials.email,
          password: "WrongPassword999!"
        });

      expect(res.status).toBe(401);
      expect(res.body).toHaveProperty("error");
      expect(res.body.error).toMatch(/invalid email or password/i);
      expect(res.headers["set-cookie"]).toBeUndefined();
    });

    it("returns HTTP 401 with identical generic error on non-existent email (no user enumeration)", async () => {
      const res = await request(app)
        .post("/api/auth/login")
        .send({
          email: "nonexistent@unimerch.ac.th",
          password: "Password123!"
        });

      expect(res.status).toBe(401);
      expect(res.body).toHaveProperty("error");
      expect(res.body.error).toMatch(/invalid email or password/i);
      expect(res.headers["set-cookie"]).toBeUndefined();
    });

    it("returns HTTP 400 Bad Request when email or password is missing", async () => {
      const res = await request(app)
        .post("/api/auth/login")
        .send({ email: "customer1@unimerch.ac.th" });

      expect(res.status).toBe(400);
      expect(res.body).toHaveProperty("error");
    });
  });

  describe("TEST-03: Session Identity & Route Protection (AC-03)", () => {
    it("returns HTTP 401 when GET /api/auth/me is requested without a session cookie", async () => {
      const res = await request(app).get("/api/auth/me");

      expect(res.status).toBe(401);
      expect(res.body).toHaveProperty("error");
    });

    it("returns HTTP 401 when GET /api/auth/me is requested with an invalid session token", async () => {
      const res = await request(app)
        .get("/api/auth/me")
        .set("Cookie", ["sid=invalid-token-12345"]);

      expect(res.status).toBe(401);
      expect(res.body).toHaveProperty("error");
    });

    it("returns current user profile when valid session cookie is provided", async () => {
      const loginRes = await request(app)
        .post("/api/auth/login")
        .send(customerCredentials);
      const cookie = loginRes.headers["set-cookie"];

      const meRes = await request(app)
        .get("/api/auth/me")
        .set("Cookie", cookie);

      expect(meRes.status).toBe(200);
      expect(meRes.body.user).toMatchObject({
        email: customerCredentials.email,
        role: "CUSTOMER"
      });
      expect(meRes.body.user).not.toHaveProperty("passwordHash");
    });
  });

  describe("TEST-04: Logout & Session Invalidation (AC-04)", () => {
    it("logs out successfully, clears cookie, and invalidates session in DB", async () => {
      // 1. Log in
      const loginRes = await request(app)
        .post("/api/auth/login")
        .send(customerCredentials);
      const cookie = loginRes.headers["set-cookie"];

      // 2. Call logout
      const logoutRes = await request(app)
        .post("/api/auth/logout")
        .set("Cookie", cookie);

      expect(logoutRes.status).toBe(200);
      expect(logoutRes.body).toHaveProperty("message");

      // Verify cookie cleared
      const setCookies = logoutRes.headers["set-cookie"];
      expect(setCookies).toBeDefined();

      // 3. Subsequent /api/auth/me returns 401
      const meAfterRes = await request(app)
        .get("/api/auth/me")
        .set("Cookie", cookie);

      expect(meAfterRes.status).toBe(401);
    });
  });
});
