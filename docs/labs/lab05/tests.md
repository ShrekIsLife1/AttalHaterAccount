# Lab 5 Software Test Specifications & Traceability Matrix

## Consolidated Lab 5 Test Map

| Requirement / Check | Issue | Planned TEST IDs | Level | Description | Status |
|---|---|---|---|---|:---:|
| **R-12, Cost Control** | #16 | — | Cloud Setup | GCP portal activation, team resources, budget controls, public repo & push protection | ✅ Done |
| **R-02, R-04** | #17 | TEST-L5-01..04, L5-08..09 | Unit / API | Config loader, `.env.example`, session DB persistence, safe production seed | ✅ Done |
| **R-01, C-03** | #18 | TEST-L5-10..14 | Container | Docker multi-stage build from fresh clone, docker-compose local stack, non-root user | ✅ Done |
| **R-05, C-01** | #19 | TEST-L5-15..19 | CI Workflow | GitHub Actions `test-and-docker` job on PRs into `lab5-staging` and `main` | ✅ Done |
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

---

## Detailed Test Specifications: Issue #18 (Dockerize Application)

| TEST ID | Level | Test Description | Verification Method | Result |
|---|---|---|---|:---:|
| **TEST-L5-10** | Container | Unified multi-stage `Dockerfile` builds cleanly from fresh tree with `GIT_SHA` build arg | `docker build --build-arg GIT_SHA=$(git rev-parse HEAD) -t unimerch:test .` | Pass |
| **TEST-L5-11** | Container | `docker compose up --build` with `.env.example` starts DB, executes migration/seed, answers `/api/ready` | `docker compose up -d --build && curl -fsS localhost:3000/api/ready` | Pass |
| **TEST-L5-12** | Container | Non-root runtime user (`USER node`, UID ≠ 0); zero `.env` or `.git` files inside container | `docker run --rm unimerch:test id -u` & `find /app -name '.env*'` | Pass |
| **TEST-L5-13** | Container | Unified container serves client SPA at `GET /` and API endpoints at `GET /api/products` | `curl -s localhost:3000/ \| grep -i "<html"` & `curl -s localhost:3000/api/products` | Pass |
| **TEST-L5-14** | Container | `GET /api/version` returns commit SHA exactly matching `GIT_SHA` passed at build time | `curl -s localhost:3000/api/version` matches `git rev-parse HEAD` | Pass |

---

## Detailed Test Specifications: Issue #19 (CI on Pull Requests)

| TEST ID | Level | Test Description | Verification Method / Evidence | Result |
|---|---|---|---|:---:|
| **TEST-L5-15** | CI | A PR targeting `lab5-staging` or `main` triggers job `test-and-docker` running all stages (deploy script stubs, server tests, client tests, Docker build) | GitHub Actions workflow trigger & run status | Pass |
| **TEST-L5-16** | CI | Run log captures full test summaries with counts (passed/failed/skipped) for all suites including Lab 5 | GitHub Actions step execution logs | Pass |
| **TEST-L5-17** | CI | Workflow fails when any test step fails; zero `continue-on-error` or `\|\| true` bypasses | Workflow review of `.github/workflows/ci-docker.yml` | Pass |
| **TEST-L5-18** | CI | CI triggers consistently on PRs into both `lab5-staging` and `main`, as well as on `workflow_dispatch` | Workflow triggers `pull_request` branches config | Pass |
| **TEST-L5-19** | CI | Offline deploy script stubs (`test_deploy_stub.sh`, `test_release_stub.sh`, `test_smoke.py`) execute in CI before backend tests | CI step 3 execution | Pass |
