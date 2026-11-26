import { getPrisma } from "../src/prisma.js";
import bcrypt from "bcryptjs";

export async function runSeed() {
  if (process.env.SEED_DEMO_DATA === "false") {
    console.log("SEED_DEMO_DATA is false: skipping seed.");
    return;
  }

  const prisma = getPrisma();
  const isProduction = process.env.NODE_ENV === "production";
  const seedPassword = process.env.SEED_PASSWORD || process.env.DEMO_USER_PASSWORD;

  if (isProduction) {
    if (!seedPassword) {
      throw new Error("Missing required environment variable: SEED_PASSWORD is required in production mode");
    }
    if (seedPassword === "password123") {
      throw new Error("Insecure SEED_PASSWORD detected: 'password123' cannot be used in production mode");
    }
  }

  const defaultPassword = seedPassword || "password123";
  const passwordHash = await bcrypt.hash(defaultPassword, 10);

  // 1. Seed Users (>= 3 Customers, >= 2 Operators)
  const usersData = [
    {
      email: "customer1@example.com",
      name: "Alice Customer",
      role: "CUSTOMER" as const,
      passwordHash,
      isActive: true,
    },
    {
      email: "customer2@example.com",
      name: "Bob Customer",
      role: "CUSTOMER" as const,
      passwordHash,
      isActive: true,
    },
    {
      email: "customer3@example.com",
      name: "Charlie Customer",
      role: "CUSTOMER" as const,
      passwordHash,
      isActive: true,
    },
    {
      email: "operator1@example.com",
      name: "Dave Operator",
      role: "OPERATOR" as const,
      passwordHash,
      isActive: true,
    },
    {
      email: "operator2@example.com",
      name: "Eve Operator",
      role: "OPERATOR" as const,
      passwordHash,
      isActive: true,
    },
  ];

  for (const u of usersData) {
    await prisma.user.upsert({
      where: { email: u.email },
      update: {
        name: u.name,
        role: u.role,
        passwordHash: u.passwordHash,
        isActive: u.isActive,
      },
      create: u,
    });
  }

  // 2. Seed Products (>= 8 products, incl. 1 with stock 0 and 1 inactive)
  const productsData = [
    {
      name: "UniMerch Classic Hoodie",
      description: "Warm heavyweight cotton hoodie with embroidered campus crest.",
      priceMinor: 59000, // 590.00 THB
      stockQuantity: 25,
      isActive: true,
    },
    {
      name: "UniMerch Heritage T-Shirt",
      description: "100% organic cotton breathable campus t-shirt.",
      priceMinor: 29000, // 290.00 THB
      stockQuantity: 50,
      isActive: true,
    },
    {
      name: "Campus Spiral Notebook A5",
      description: "160-page lined spiral notebook with water-resistant cover.",
      priceMinor: 8500, // 85.00 THB
      stockQuantity: 40,
      isActive: true,
    },
    {
      name: "Ceramic Coffee Mug",
      description: "350ml microwave-safe ceramic mug with campus logo.",
      priceMinor: 15000, // 150.00 THB
      stockQuantity: 30,
      isActive: true,
    },
    {
      name: "Insulated Water Bottle 750ml",
      description: "Double-walled stainless steel bottle keeps drinks cold for 24h.",
      priceMinor: 35000, // 350.00 THB
      stockQuantity: 20,
      isActive: true,
    },
    {
      name: "Embroidered University Cap",
      description: "Adjustable 6-panel cotton twill cap with embroidered monogram.",
      priceMinor: 22000, // 220.00 THB
      stockQuantity: 15,
      isActive: true,
    },
    {
      name: "Metal Ballpoint Pen Set",
      description: "Set of 2 engraved metal pens in gift box (temporarily out of stock).",
      priceMinor: 12000, // 120.00 THB
      stockQuantity: 0, // Out of stock boundary item
      isActive: true,
    },
    {
      name: "Vintage Canvas Tote Bag",
      description: "Durable vintage canvas tote bag (discontinued line).",
      priceMinor: 18000, // 180.00 THB
      stockQuantity: 10,
      isActive: false, // Inactive item
    },
  ];

  for (const p of productsData) {
    const existing = await prisma.product.findFirst({ where: { name: p.name } });
    if (existing) {
      await prisma.product.update({
        where: { id: existing.id },
        data: p,
      });
    } else {
      await prisma.product.create({
        data: p,
      });
    }
  }

  console.log("Seeding completed successfully: 5 users and 8 products upserted.");
}

async function main() {
  await runSeed();
}

if (process.argv[1]?.endsWith("seed.ts")) {
  main()
    .catch((e) => {
      console.error(e);
      process.exit(1);
    })
    .finally(async () => {
      await getPrisma().$disconnect();
    });
}
