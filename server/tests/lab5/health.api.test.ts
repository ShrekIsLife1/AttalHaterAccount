import { describe, it, expect, vi, beforeEach } from "vitest";
import request from "supertest";
import { app } from "../../src/app.js";
import * as prismaModule from "../../src/prisma.js";

describe("TEST-L5-05..06: Health and Readiness Endpoints (API)", () => {
  it("TEST-L5-05: GET /api/health returns 200 { status: 'ok' } without DB access", async () => {
    const res = await request(app).get("/api/health");
    expect(res.status).toBe(200);
    expect(res.body).toHaveProperty("status", "ok");
  });

  it("TEST-L5-06: GET /api/ready returns 200 when DB is connected, and 503 when unreachable", async () => {
    // 1. Success case
    const resOk = await request(app).get("/api/ready");
    expect(resOk.status).toBe(200);
    expect(resOk.body).toHaveProperty("db", "connected");

    // 2. Failure case (simulate DB failure)
    const mockPrisma = {
      $queryRaw: vi.fn().mockRejectedValueOnce(new Error("Connection lost")),
    };
    const spy = vi.spyOn(prismaModule, "getPrisma").mockReturnValueOnce(mockPrisma as any);

    const resFail = await request(app).get("/api/ready");
    expect(resFail.status).toBe(503);
    expect(resFail.body).toHaveProperty("db", "disconnected");

    spy.mockRestore();
  });
});
