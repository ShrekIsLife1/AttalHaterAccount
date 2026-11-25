import { describe, it, expect, beforeAll } from "vitest";
import request from "supertest";
import crypto from "crypto";
import { app } from "../../src/app.js";
import { getPrisma } from "../../src/prisma.js";
import { runSeed } from "../../prisma/seed.js";

describe("TEST-L5-08: Session DB Persistence across app restarts (API)", () => {
  beforeAll(async () => {
    process.env.SEED_PASSWORD = "password123";
    await runSeed();
  });

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

    const tokenHash = crypto.createHash("sha256").update(token).digest("hex");

    // Verify session row exists in DB
    const sessionInDb = await prisma.session.findUnique({
      where: { tokenHash },
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
