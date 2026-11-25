import { describe, it, expect } from "vitest";
import fs from "node:fs";
import path from "node:path";

describe("TEST-L5-04: .env.example Validation (Script)", () => {
  it("every process.env.X read in server/src appears in .env.example and contains no real secrets", () => {
    const envExamplePath = path.resolve(process.cwd(), ".env.example");
    const rootEnvExamplePath = path.resolve(process.cwd(), "../.env.example");

    const exampleContent = fs.existsSync(envExamplePath)
      ? fs.readFileSync(envExamplePath, "utf-8")
      : fs.readFileSync(rootEnvExamplePath, "utf-8");

    // Check no real-looking secrets in .env.example
    const secretKeywords = ["password", "secret", "token", "key"];
    const lines = exampleContent.split("\n");
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith("#")) continue;
      const [key, value] = trimmed.split("=");
      if (!value) continue;

      const lowerKey = key.toLowerCase();
      const cleanValue = value.replace(/['"]/g, "").trim();

      if (secretKeywords.some((k) => lowerKey.includes(k))) {
        // Values for secrets must be clearly placeholder
        expect(
          cleanValue.includes("change") ||
          cleanValue.includes("example") ||
          cleanValue.includes("secret") ||
          cleanValue.includes("placeholder") ||
          cleanValue.includes("password123") ||
          cleanValue === ""
        ).toBe(true);
      }
    }

    // Inspect server/src to collect all process.env.VAR usage
    const srcDir = path.resolve(process.cwd(), "src");
    const envVarsUsed = new Set<string>();

    function scanDir(dir: string) {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory()) {
          scanDir(fullPath);
        } else if (entry.isFile() && (entry.name.endsWith(".ts") || entry.name.endsWith(".js"))) {
          const content = fs.readFileSync(fullPath, "utf-8");
          const matches = content.matchAll(/process\.env\.([A-Z0-9_]+)/g);
          for (const match of matches) {
            envVarsUsed.add(match[1]);
          }
        }
      }
    }

    scanDir(srcDir);

    // Each env var used in code should be documented in .env.example
    const documentedVars = new Set<string>();
    for (const line of lines) {
      const trimmed = line.trim();
      if (trimmed && !trimmed.startsWith("#") && trimmed.includes("=")) {
        documentedVars.add(trimmed.split("=")[0].trim());
      }
    }

    for (const usedVar of envVarsUsed) {
      expect(
        documentedVars.has(usedVar),
        `Variable process.env.${usedVar} used in src/ is missing from .env.example`
      ).toBe(true);
    }
  });
});
