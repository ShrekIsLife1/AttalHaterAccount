import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { runSeed } from "../../prisma/seed.js";
import { getPrisma } from "../../src/prisma.js";

describe("TEST-L5-09: Safe Production Seed & Idempotency (Unit/API)", () => {
  const originalEnv = process.env;

  beforeEach(() => {
    process.env = { ...originalEnv };
  });

  afterEach(() => {
    process.env = originalEnv;
  });

  it("seed in production mode throws error if SEED_PASSWORD is missing or set to insecure default", async () => {
    process.env.NODE_ENV = "production";
    delete process.env.SEED_PASSWORD;

    await expect(runSeed()).rejects.toThrowError(/SEED_PASSWORD/);

    process.env.SEED_PASSWORD = "password123";
    await expect(runSeed()).rejects.toThrowError(/insecure/i);
  });

  it("seed is idempotent and running twice does not duplicate records", async () => {
    process.env.NODE_ENV = "test";
    process.env.SEED_PASSWORD = "test-secure-seed-pwd";

    const prisma = getPrisma();
    await runSeed();
    const userCount1 = await prisma.user.count();
    const productCount1 = await prisma.product.count();

    await runSeed();
    const userCount2 = await prisma.user.count();
    const productCount2 = await prisma.product.count();

    expect(userCount2).toBe(userCount1);
    expect(productCount2).toBe(productCount1);
  });
});
