import { getPrisma } from "../src/prisma.js";

async function main() {
  const prisma = getPrisma();
  void prisma;
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await getPrisma().$disconnect();
  });
