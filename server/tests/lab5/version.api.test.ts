import { describe, it, expect } from "vitest";
import request from "supertest";
import { app } from "../../src/app.js";

describe("TEST-L5-07: Version Endpoint (API)", () => {
  it("GET /api/version returns GIT_SHA from env, and leaks no extra sensitive info", async () => {
    process.env.GIT_SHA = "1234567890abcdef1234567890abcdef12345678";
    const res = await request(app).get("/api/version");
    expect(res.status).toBe(200);
    expect(res.body).toEqual({ commit: "1234567890abcdef1234567890abcdef12345678" });
    expect(res.body).not.toHaveProperty("DATABASE_URL");
    expect(res.body).not.toHaveProperty("SESSION_SECRET");
  });
});
