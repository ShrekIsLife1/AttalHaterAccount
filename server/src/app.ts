import express, { Request, Response } from "express";
import cors from "cors";
import { getPrisma } from "./prisma.js";

void getPrisma;

export const app = express();

app.use(cors());
app.use(express.json());

app.get("/api/health", (_req: Request, res: Response) => {
  res.status(501).json({ error: "Not implemented yet" });
});

export default app;
