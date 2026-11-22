import crypto from "crypto";
import { Router, Request, Response } from "express";
import bcrypt from "bcryptjs";
import { z } from "zod";
import { getPrisma } from "../prisma.js";
import { hashToken, requireAuth } from "../middleware/auth.js";

export const authRouter = Router();

const loginSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(1, "Password is required")
});

// POST /api/auth/login
authRouter.post("/login", async (req: Request, res: Response) => {
  const parseResult = loginSchema.safeParse(req.body);
  if (!parseResult.success) {
    return res.status(400).json({
      error: "Validation error",
      details: parseResult.error.errors.map(e => e.message)
    });
  }

  const { email, password } = parseResult.data;
  const prisma = getPrisma();

  try {
    const user = await prisma.user.findUnique({
      where: { email: email.toLowerCase().trim() }
    });

    // Generic error to prevent user enumeration
    if (!user || !user.isActive) {
      return res.status(401).json({ error: "Invalid email or password" });
    }

    const passwordMatch = await bcrypt.compare(password, user.passwordHash);
    if (!passwordMatch) {
      return res.status(401).json({ error: "Invalid email or password" });
    }

    // Generate random 32-byte cryptographic session token
    const rawToken = crypto.randomBytes(32).toString("hex");
    const tokenHash = hashToken(rawToken);
    const expiresAt = new Date(Date.now() + 8 * 60 * 60 * 1000); // 8 hours

    await prisma.session.create({
      data: {
        userId: user.id,
        tokenHash,
        expiresAt
      }
    });

    res.cookie("sid", rawToken, {
      httpOnly: true,
      sameSite: "lax",
      path: "/",
      maxAge: 8 * 60 * 60 * 1000,
      secure: process.env.NODE_ENV === "production"
    });

    return res.status(200).json({
      user: {
        id: user.id,
        name: user.name,
        email: user.email,
        role: user.role
      }
    });
  } catch (error) {
    console.error("Login error:", error);
    return res.status(500).json({ error: "Internal server error" });
  }
});

// GET /api/auth/me
authRouter.get("/me", requireAuth, (req: Request, res: Response) => {
  const user = req.user!;
  return res.status(200).json({
    user: {
      id: user.id,
      name: user.name,
      email: user.email,
      role: user.role
    }
  });
});

// POST /api/auth/logout
authRouter.post("/logout", async (req: Request, res: Response) => {
  const token = req.cookies?.sid;
  if (token && typeof token === "string") {
    try {
      const prisma = getPrisma();
      const tokenHash = hashToken(token);
      await prisma.session.deleteMany({
        where: { tokenHash }
      });
    } catch (error) {
      console.error("Logout DB cleanup error:", error);
    }
  }

  res.clearCookie("sid", {
    path: "/",
    httpOnly: true,
    sameSite: "lax"
  });

  return res.status(200).json({
    message: "Logged out successfully"
  });
});
