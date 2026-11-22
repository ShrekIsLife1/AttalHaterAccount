import express, { Request, Response } from "express";
import cors from "cors";
import cookieParser from "cookie-parser";
import { getPrisma } from "./prisma.js";
import { authMiddleware, requireRole } from "./middleware/auth.js";
import { authRouter } from "./routes/auth.js";

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

app.get("/api/health", (_req: Request, res: Response) => {
  res.status(200).json({ status: "ok", service: "TokTickIT API" });
});

// Protected test endpoint for RBAC validation
app.get("/api/test/operator-only", requireRole("OPERATOR"), (_req: Request, res: Response) => {
  res.status(200).json({ message: "Operator authorized" });
});

export default app;
