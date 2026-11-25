import { z } from "zod";

/**
 * Cloud-Ready Configuration Schema (R-02, TEST-L5-01..03)
 * Validates that all required environment variables are provided and correctly typed.
 * Prevents silent fallback to insecure defaults in production.
 */
const ConfigSchema = z.object({
  DATABASE_URL: z.string({
    required_error: "Missing required environment variable: DATABASE_URL",
  }).min(1, "Missing required environment variable: DATABASE_URL"),

  PORT: z.coerce.number({
    invalid_type_error: "PORT must be a valid number",
  }).default(3000),

  SESSION_SECRET: z.string({
    required_error: "Missing required environment variable: SESSION_SECRET",
  }).min(1, "Missing required environment variable: SESSION_SECRET"),

  CORS_ORIGIN: z.string().default("http://localhost:5173"),

  NODE_ENV: z.enum(["development", "test", "production"]).default("development"),

  MAX_QTY_PER_LINE: z.coerce.number({
    invalid_type_error: "MAX_QTY_PER_LINE must be a valid number",
  }).default(10),

  GIT_SHA: z.string().default("unknown"),

  SEED_PASSWORD: z.string().optional(),
});

export type AppConfig = z.infer<typeof ConfigSchema>;

let cachedConfig: AppConfig | null = null;

export function loadConfig(env = process.env): AppConfig {
  // If in production mode, ensure SESSION_SECRET is strictly provided and not a dummy fallback
  if (env.NODE_ENV === "production") {
    if (!env.SESSION_SECRET || env.SESSION_SECRET.trim() === "") {
      throw new Error("Missing required environment variable in production: SESSION_SECRET");
    }
  }

  const result = ConfigSchema.safeParse(env);
  if (!result.success) {
    const errorDetails = result.error.errors.map((e) => {
      const field = e.path.join(".");
      return `${field || "config"}: ${e.message}`;
    }).join(", ");

    // Never print raw secrets/values in errors, only the variable name and issue
    throw new Error(`Invalid configuration: ${errorDetails}`);
  }

  return result.data;
}

export function getConfig(): AppConfig {
  if (!cachedConfig) {
    cachedConfig = loadConfig();
  }
  return cachedConfig;
}

export function resetConfig(): void {
  cachedConfig = null;
}
