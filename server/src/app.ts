import express, { Request, Response } from "express";
import cors from "cors";
import cookieParser from "cookie-parser";
import path from "node:path";
import fs from "node:fs";
import { getPrisma } from "./prisma.js";
import { authMiddleware, requireRole } from "./middleware/auth.js";
import { authRouter } from "./routes/auth.js";
import { productsRouter } from "./routes/products.js";
import { ordersRouter } from "./routes/orders.js";
import { operatorOrdersRouter } from "./routes/operatorOrders.js";

// Initialize Prisma
void getPrisma();

export const app = express();

app.use(cors({
  origin: process.env.CORS_ORIGIN || "http://localhost:5173",
  credentials: true
}));
app.use(express.json());
app.use(cookieParser());
app.use(authMiddleware);

// Routes
app.use("/api/auth", authRouter);
app.use("/api/products", productsRouter);
app.use("/api/orders", ordersRouter);
app.use("/api/operator/orders", operatorOrdersRouter);

app.get("/api/health", (_req: Request, res: Response) => {
  res.status(200).json({ status: "ok", service: "TokTickIT API" });
});

app.get("/api/ready", async (_req: Request, res: Response) => {
  try {
    const prisma = getPrisma();
    await prisma.$queryRaw`SELECT 1`;
    res.status(200).json({ status: "ready", db: "connected" });
  } catch {
    res.status(503).json({ status: "not_ready", db: "disconnected" });
  }
});

app.get("/api/version", (_req: Request, res: Response) => {
  res.status(200).json({ commit: process.env.GIT_SHA || "unknown" });
});

// Protected test endpoint for RBAC validation
app.get("/api/test/operator-only", requireRole("OPERATOR"), (_req: Request, res: Response) => {
  res.status(200).json({ message: "Operator authorized" });
});

// Serve built React client in production
const clientDistCandidates = [
  path.resolve(process.cwd(), "../client/dist"),
  path.resolve(process.cwd(), "client/dist"),
  "/app/client/dist",
];
const clientDist = clientDistCandidates.find((dir) => fs.existsSync(dir));

if (clientDist) {
  app.use(express.static(clientDist));
  app.get("*", (req: Request, res: Response, next) => {
    if (req.path.startsWith("/api")) {
      return next();
    }
    res.sendFile(path.join(clientDist, "index.html"));
  });
}

export default app;
