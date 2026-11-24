import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { loadConfig } from "../../src/config.js";

describe("TEST-L5-01..03: Config Loader (Unit)", () => {
  const originalEnv = process.env;

  beforeEach(() => {
    process.env = { ...originalEnv };
  });

  afterEach(() => {
    process.env = originalEnv;
  });

  it("TEST-L5-01: returns typed values when all required environment variables are set", () => {
    process.env.DATABASE_URL = "postgresql://user:pass@localhost:5432/testdb";
    process.env.PORT = "4000";
    process.env.SESSION_SECRET = "test-secret-min-32-chars-long-value";
    process.env.CORS_ORIGIN = "http://localhost:5173";
    process.env.NODE_ENV = "test";
    process.env.MAX_QTY_PER_LINE = "10";
    process.env.GIT_SHA = "abcdef1234567890abcdef1234567890abcdef12";

    const config = loadConfig();
    expect(config.DATABASE_URL).toBe("postgresql://user:pass@localhost:5432/testdb");
    expect(config.PORT).toBe(4000);
    expect(config.SESSION_SECRET).toBe("test-secret-min-32-chars-long-value");
    expect(config.CORS_ORIGIN).toBe("http://localhost:5173");
    expect(config.NODE_ENV).toBe("test");
    expect(config.MAX_QTY_PER_LINE).toBe(10);
    expect(config.GIT_SHA).toBe("abcdef1234567890abcdef1234567890abcdef12");
  });

  it("TEST-L5-02: missing required variable throws error naming the variable, never its value", () => {
    delete process.env.DATABASE_URL;
    process.env.SESSION_SECRET = "supersecret";

    expect(() => loadConfig()).toThrowError(/DATABASE_URL/);
    try {
      loadConfig();
    } catch (err: any) {
      expect(err.message).toContain("DATABASE_URL");
      expect(err.message).not.toContain("supersecret");
    }
  });

  it("TEST-L5-03: rejects invalid numeric values like MAX_QTY_PER_LINE=abc and missing secret without default in production", () => {
    process.env.DATABASE_URL = "postgresql://user:pass@localhost:5432/testdb";
    process.env.SESSION_SECRET = "some-secret";
    process.env.MAX_QTY_PER_LINE = "invalid_number";

    expect(() => loadConfig()).toThrowError(/MAX_QTY_PER_LINE/);

    // In production mode, SESSION_SECRET cannot be fallback/empty
    process.env.NODE_ENV = "production";
    delete process.env.SESSION_SECRET;
    expect(() => loadConfig()).toThrowError(/SESSION_SECRET/);
  });
});
