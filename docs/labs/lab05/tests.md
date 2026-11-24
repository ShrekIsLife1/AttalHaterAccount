# Lab 5 Software Test Specifications & Traceability Matrix

## Consolidated Lab 5 Test Map

| Requirement / Check | Issue | Planned TEST IDs | Level | Description | Status |
|---|---|---|---|---|:---:|
| **R-12, Cost Control** | #16 | — | Cloud Setup | GCP portal activation, team resources, budget controls, public repo & push protection | ✅ Done |
| **R-02, R-04** | #17 | TEST-L5-01..04, L5-08..09 | Unit / API | Config loader, `.env.example`, session DB persistence, safe production seed | ✅ Done |
| **R-01, C-03** | #18 | TEST-L5-10..14 | Container | Docker multi-stage build from fresh clone, docker-compose local stack, non-root user | 🔲 Planned |
| **R-05, C-01** | #19 | TEST-L5-15..19 | CI Workflow | GitHub Actions `test-and-docker` job on PRs into `sprint1-staging` and `main` | 🔲 Planned |
| **R-03, R-04, C-04** | #20 | TEST-L5-20..25 | Live / Smoke | First deployment on Cloud Run, live domain customer order journey, failure rejections | 🔲 Planned |
| **R-06, R-09, C-02** | #21 | TEST-L5-26..31 | Merge Gate | Workload Identity Federation, branch protection ruleset, failing PR blocked | 🔲 Planned |
| **R-07, R-08, C-06** | #22 | TEST-L5-32..42 | Release Pipeline | `deploy.yml`, automated smoke test, release by commit SHA digest | 🔲 Planned |
| **R-04, C-05** | #23 | TEST-L5-43..47 | Persistence / Rollback | Data persistence across service restart and redeploy, additive migrations, rollback | 🔲 Planned |
| **Cost Control** | #24 | TEST-L5-48..51 | Operations | Pause/resume Cloud SQL procedure, Cloud Run min=0 instances, spend tracking | 🔲 Planned |
| **R-08, R-11, DoD** | #25 | TEST-L5-52..58 | Documentation | Final release verification, `deployment.md`, secret scan, and LEB2 deliverable PDF | 🔲 Planned |

---

## Detailed Test Specifications: Issue #17 (Cloud-Ready Configuration)

| TEST ID | Level | Test Description | Target File | Result |
|---|---|---|---|:---:|
| **TEST-L5-01** | Unit | Config loader returns typed values when all variables are set | `server/tests/lab5/config.unit.test.ts` | Pass |
| **TEST-L5-02** | Unit | Missing required variable (`DATABASE_URL`, `SESSION_SECRET`) throws error naming variable without leaking value | `server/tests/lab5/config.unit.test.ts` | Pass |
| **TEST-L5-03** | Unit | Invalid types (`MAX_QTY_PER_LINE=abc`) rejected; production rejects insecure/missing secrets | `server/tests/lab5/config.unit.test.ts` | Pass |
| **TEST-L5-04** | Script | Every `process.env.X` read in `server/src` appears in `.env.example`; contains only placeholders | `server/tests/lab5/env-example.test.ts` | Pass |
| **TEST-L5-05** | API | `GET /api/health` returns 200 `{ status: "ok" }` without database dependency | `server/tests/lab5/health.api.test.ts` | Pass |
| **TEST-L5-06** | API | `GET /api/ready` returns 200 when DB connected, 503 when unreachable | `server/tests/lab5/health.api.test.ts` | Pass |
| **TEST-L5-07** | API | `GET /api/version` returns `GIT_SHA` from environment without leaking sensitive variables | `server/tests/lab5/version.api.test.ts` | Pass |
| **TEST-L5-08** | API | Session persists across requests and survives app restart via PostgreSQL `Session` table | `server/tests/lab5/session-persistence.api.test.ts` | Pass |
| **TEST-L5-09** | Unit/API | Seed in production rejects missing or default `SEED_PASSWORD`; seed is strictly idempotent | `server/tests/lab5/seed-config.test.ts` | Pass |
