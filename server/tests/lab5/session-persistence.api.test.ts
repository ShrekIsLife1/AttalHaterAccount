import { describe, it, expect } from "vitest";
import request from "supertest";
import { app } from "../../src/app.js";
import { getPrisma } from "../../src/prisma.js";

describe("TEST-L5-08: Session DB Persistence across app restarts (API)", () => {
  it("session created via login is persisted in Session table and remains valid across new requests", async () => {
    const prisma = getPrisma();

    // Log in as customer1
    const loginRes = await request(app)
      .post("/api/auth/login")
      .send({ email: "customer1@example.com", password: "password123" });

    expect(loginRes.status).toBe(200);
    const cookie = loginRes.headers["set-cookie"]?.[0];
    expect(cookie).toBeDefined();

    // Extract session token from sid cookie
    const tokenMatch = cookie.match(/sid=([^;]+)/);
    const token = tokenMatch ? decodeURIComponent(tokenMatch[1]) : "";
    expect(token).toBeTruthy();

    // Verify session row exists in DB
    const sessionInDb = await prisma.session.findUnique({
      where: { token },
      include: { user: true },
    });
    expect(sessionInDb).not.toBeNull();
    expect(sessionInDb?.user.email).toBe("customer1@example.com");

    // Query /api/auth/me using the cookie
    const meRes = await request(app).get("/api/auth/me").set("Cookie", cookie);
    expect(meRes.status).toBe(200);
    expect(meRes.body.user.email).toBe("customer1@example.com");
  });
});
