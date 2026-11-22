import crypto from "crypto";
import { Request, Response, NextFunction } from "express";
import { User, Session, Role } from "@prisma/client";
import { getPrisma } from "../prisma.js";

declare global {
  namespace Express {
    interface Request {
      user?: User;
      sessionRecord?: Session;
    }
  }
}

export function hashToken(token: string): string {
  return crypto.createHash("sha256").update(token).digest("hex");
}

export async function authMiddleware(req: Request, _res: Response, next: NextFunction) {
  const token = req.cookies?.sid;
  if (!token || typeof token !== "string") {
    return next();
  }

  try {
    const prisma = getPrisma();
    const tokenHash = hashToken(token);

    const session = await prisma.session.findUnique({
      where: { tokenHash },
      include: { user: true }
    });

    if (!session) {
      return next();
    }

    // Check expiration
    if (session.expiresAt < new Date()) {
      // Invalidate expired session
      await prisma.session.delete({ where: { id: session.id } }).catch(() => {});
      return next();
    }

    // Check if user is active
    if (!session.user || !session.user.isActive) {
      return next();
    }

    req.user = session.user;
    req.sessionRecord = session;
  } catch (error) {
    console.error("Auth middleware error:", error);
  }

  return next();
}

export function requireAuth(req: Request, res: Response, next: NextFunction) {
  if (!req.user) {
    return res.status(401).json({ error: "Authentication required" });
  }
  return next();
}

export function requireRole(...roles: Role[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      return res.status(401).json({ error: "Authentication required" });
    }
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: "Forbidden: insufficient permissions" });
    }
    return next();
  };
}
