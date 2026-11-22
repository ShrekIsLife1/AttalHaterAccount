import { describe, it, expect, beforeAll, afterAll } from "vitest";
import { getPrisma } from "../../src/prisma.js";
import { runSeed } from "../../prisma/seed.js";

describe("Persistence & Seed Foundation (AC-17 / TEST-21)", () => {
  const prisma = getPrisma();

  beforeAll(async () => {
    // Run seed once
    await runSeed();
  });

  afterAll(async () => {
    await prisma.$disconnect();
  });

  it("persists seeded users and products correctly", async () => {
    const userCount = await prisma.user.count();
    const productCount = await prisma.product.count();

    expect(userCount).toBeGreaterThanOrEqual(5);
    expect(productCount).toBeGreaterThanOrEqual(8);

    // Verify roles
    const customers = await prisma.user.findMany({ where: { role: "CUSTOMER" } });
    const operators = await prisma.user.findMany({ where: { role: "OPERATOR" } });

    expect(customers.length).toBeGreaterThanOrEqual(3);
    expect(operators.length).toBeGreaterThanOrEqual(2);

    // Verify boundary products (out of stock and inactive)
    const outOfStock = await prisma.product.findFirst({ where: { stockQuantity: 0 } });
    const inactive = await prisma.product.findFirst({ where: { isActive: false } });

    expect(outOfStock).toBeDefined();
    expect(outOfStock?.name).toBe("Metal Ballpoint Pen Set");

    expect(inactive).toBeDefined();
    expect(inactive?.name).toBe("Vintage Canvas Tote Bag");
  });

  it("is idempotent: running seed a second time produces no duplicates or constraint errors", async () => {
    const countBefore = await prisma.product.count();
    const userBefore = await prisma.user.count();

    // Run seed second time
    await runSeed();

    const countAfter = await prisma.product.count();
    const userAfter = await prisma.user.count();

    expect(countAfter).toBe(countBefore);
    expect(userAfter).toBe(userBefore);
  });

  it("enforces unique constraint on user email", async () => {
    const duplicateEmail = "customer1@example.com";
    await expect(
      prisma.user.create({
        data: {
          email: duplicateEmail,
          name: "Duplicate User",
          passwordHash: "dummyhash",
          role: "CUSTOMER",
        },
      })
    ).rejects.toThrow();
  });

  it("data persists across client disconnect and reconnect", async () => {
    // Disconnect client
    await prisma.$disconnect();

    // Reconnect and query
    const newPrisma = getPrisma();
    const products = await newPrisma.product.findMany();
    expect(products.length).toBeGreaterThanOrEqual(8);
  });
});
