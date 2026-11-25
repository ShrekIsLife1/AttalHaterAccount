# Lab 5 Deliverable — Living Document (Evidence Index & Answers)

**Status Legend:** ✅ Complete · 🟡 In Progress · 🔲 Planned · 📸 Screenshot Attached / Captured  
**Target Submission:** `lab5_sec1_AttalHaterAccount.pdf`  
**Public Repository:** [https://github.com/ShrekIsLife1/AttalHaterAccount](https://github.com/ShrekIsLife1/AttalHaterAccount)  
**Base Release (Sprint 1):** Commit `c029872` / Tag `v0.1.0-sprint1`  

---

## Answer Part 0: Team and Evidence Index

### 0.1 Team Metadata & Public Infrastructure

| Item | Details |
|---|---|
| **Course & Term** | CPE 334 Software Engineering — Lab 5: Cloud Deployment & CI/CD on GCP |
| **Team / Group Name** | `AttalHaterAccount` (Theme 4 — UniMerch Campus Store) |
| **Student 1 (Ba)** | Baptiste Carré (Student ID: `69540460014`, GitHub: `@ShrekIsLife1`) |
| **Student 2 (Cl)** | Clément Dominique Delrieu (Student ID: `69540460016`, GitHub: `@ClemDelGh`) |
| **Public GitHub Repo** | [https://github.com/ShrekIsLife1/AttalHaterAccount](https://github.com/ShrekIsLife1/AttalHaterAccount) (Verified accessible in incognito mode) |
| **Course GCP Project ID** | `cpe-se-course-2026` |
| **GCP Region** | `asia-southeast1` |
| **Team Resource Prefix** | `s3c35c9bd` |
| **Artifact Registry** | `asia-southeast1-docker.pkg.dev/cpe-se-course-2026/s3c35c9bd` |
| **Cloud Run Service** | `s3c35c9bd` (Planned live URL provisioned in #16 / #20) |
| **Cloud Run Migration Job**| `s3c35c9bd-migrate` |

---

### 0.2 Lab 5 Contribution Table (Pair Work Breakdown)

| Issue | Title | Author | Reviewer | PR Link | Status |
|---|---|:---:|:---:|---|:---:|
| **#16** | GCP account, project, budget alert & baseline | **Ba** | Cl | [PR #44](https://github.com/ShrekIsLife1/AttalHaterAccount/pull/44) | ✅ Merged |
| **#17** | Cloud-ready configuration, probes, `.env.example` | **Cl** | Ba | [PR #45](https://github.com/ShrekIsLife1/AttalHaterAccount/pull/45) | ✅ Merged |
| **#18** | Dockerize application & container verification | **Ba** | Cl | [PR #46](https://github.com/ShrekIsLife1/AttalHaterAccount/pull/46) | 🟡 In Review |
| **#19** | CI on Pull Requests (`test-and-docker`, C-01) | **Cl** | Ba | *Pending #18* | 🔲 Planned |
| **#20** | First deployment to GCP & domain journey (C-04) | **Ba** | Cl | *Pending #19* | 🔲 Planned |
| **#21** | GitHub ↔ GCP (WIF) & failing PR gate (C-02) | **Cl** | Ba | *Pending #20* | 🔲 Planned |
| **#22** | Repeatable deploy pipeline & release commit (C-06) | **Ba** | Cl | *Pending #21* | 🔲 Planned |
| **#23** | Cloud persistence & rollback verification (C-05) | **Cl** | Ba | *Pending #22* | 🔲 Planned |
| **#24** | Cost control: pause/resume Cloud SQL & quota audit | **Ba** | Cl | *Pending #20* | 🔲 Planned |
| **#25** | Final deployment documentation & deliverable PDF | **Cl** | Ba | *Pending #24* | 🔲 Planned |

---

### 0.3 Consolidated Evidence Index (Traceability Matrix)

| Rubric Part | Required Evidence | Check / ID | Artifact / Link / Reference | Verification Result |
|---|---|:---:|---|---|
| **Part 0: Team & Index** | Public repo & contribution records | R-10, R-11, R-12 | [GitHub Repository](https://github.com/ShrekIsLife1/AttalHaterAccount) | Incognito verified; alternating roles respected |
| **Part 1: CI & Quality Gate** | CI workflow & passing PR | C-01, R-05 | `.github/workflows/ci-docker.yml` | *To be captured in #19* |
| **Part 1: CI & Quality Gate** | Branch protection & blocked failing PR | C-02, R-06 | Temp branch PR & merge gate screenshot | *To be captured in #21* |
| **Part 2: Docker & Config** | Unified multi-stage Dockerfile & clean build | C-03, R-01 | [Dockerfile](file:///home/lapulga/Documents/cours/Thailande/SWE/lab%20duo/AttalHaterAccount/Dockerfile), `TEST-L5-10` | Builds cleanly from clean tree with GIT_SHA |
| **Part 2: Docker & Config** | Local compose stack runs with `.env.example` | C-03, R-01 | [docker-compose.yml](file:///home/lapulga/Documents/cours/Thailande/SWE/lab%20duo/AttalHaterAccount/docker-compose.yml), `TEST-L5-11` | DB healthy, migrations pass, `/api/ready` 200 |
| **Part 2: Docker & Config** | Non-root user & zero secrets baked in | R-01, R-02 | `TEST-L5-12` (`node` UID 1000) | No `.env` or `.git` in image |
| **Part 2: Docker & Config** | Environment table & no secrets committed | R-02 | [deployment.md](file:///home/lapulga/Documents/cours/Thailande/SWE/lab%20duo/AttalHaterAccount/docs/labs/lab05/deployment.md) Sec 2 | 8 variables documented; Secret Scanning active |
| **Part 3: GCP & Persistence** | Live domain customer ordering journey | C-04, R-03 | Public Cloud Run URL | *To be captured in #20* |
| **Part 3: GCP & Persistence** | Data persistence across service restart | C-05, R-04 | Cloud SQL records & `/api/ready` | *To be captured in #23* |
| **Part 4: Release Pipeline** | Continuous deployment on merge to main | C-06, R-07 | `.github/workflows/deploy.yml` | *To be captured in #22* |
| **Part 4: Release Pipeline** | Release revision equals commit SHA | R-08 | `GET /api/version` matches release commit | *To be captured in #22* |

---

## Answer Part 1: CI and Quality Gate (Issues #19 & #21)

*(Section populated during Issues #19 and #21)*
- **CI Workflow File:** `.github/workflows/ci-docker.yml`
- **Check C-01 (Passing PR):** Links and summaries of the `test-and-docker` job.
- **Check C-02 (Failing PR Merge Gate):** Screenshot of failing temporary branch PR blocked by branch ruleset.

---

## Answer Part 2: Docker and Reproducible Configuration (Issues #17 & #18)

### 2.1 Unified Production Container (`Dockerfile`)
- **Multi-Stage Architecture:**
  - Stage 1 (`client-builder`): Compiles React TypeScript Vite SPA (`npm run build`) to static assets in `/app/client/dist`.
  - Stage 2 (`server-builder`): Generates Prisma Client (`npx prisma generate`) and compiles TypeScript Express backend (`npm run build`).
  - Stage 3 (`production`): Minimal Alpine runtime (`node:24-alpine`) running as unprivileged user `USER node` (UID 1000). Serves both the REST API and the React SPA on port 3000.
- **Traceability (`GIT_SHA`):** Injected as build argument (`ARG GIT_SHA="dev"`), exposed via `ENV GIT_SHA=${GIT_SHA}`, and queried by `GET /api/version` (TEST-L5-14).
- **Graceful Shutdown:** `ENTRYPOINT ["./docker-entrypoint.sh"]` with `exec "$@"` ensures PID 1 receives SIGTERM signals from Cloud Run.

### 2.2 Local Container Stack (`docker-compose.yml`)
- Orchestrates:
  - `unimerch-db`: PostgreSQL 16 Alpine with persistent volume `postgres_data` and healthcheck via `pg_isready`.
  - `unimerch-migrate`: Transient container executing `npx prisma migrate deploy && npm run prisma:seed`.
  - `unimerch-server`: Express backend serving the application on port 3000.
  - `unimerch-client`: Preview reverse-proxy on port 5173.
- Starts out of the box using only default values from `.env.example`.

### 2.3 Check C-03 & Container Test Suite (`TEST-L5-10` to `TEST-L5-14`)

Automated script: `scripts/test-container.sh`.

```bash
# Execution Command
bash scripts/test-container.sh
```

| Test ID | Verified Criteria | Evidence / Result |
|---|---|:---:|
| **TEST-L5-10** | `docker build .` succeeds from clean tree with `GIT_SHA` build arg | Pass (Built `unimerch:test`) |
| **TEST-L5-11** | `docker compose up --build` with `.env.example`: DB healthy, migration/seed exits 0, `/api/ready` 200 | Pass (`{"status":"ready","db":"connected"}`) |
| **TEST-L5-12** | Container runs as non-root (`id -u` = 1000) and contains zero `.env` or `.git` files | Pass (UID 1000, zero secrets found) |
| **TEST-L5-13** | UI served (`GET /` returns HTML) and API reachable (`GET /api/products`) | Pass (HTML returned & catalog JSON received) |
| **TEST-L5-14** | `GET /api/version` matches `GIT_SHA` passed at build time | Pass (`{"commit":"<GIT_SHA>"}`) |

### 2.4 Cloud-Ready Environment Configuration (Issue #17)
- All runtime configurations read strictly from environment variables via Zod schema validation in `server/src/config.ts`.
- `.env.example` contains only harmless placeholders (`DATABASE_URL`, `SESSION_SECRET`, `PORT`, `CORS_ORIGIN`, `NODE_ENV`, `MAX_QTY_PER_LINE`, `GIT_SHA`, `SEED_PASSWORD`).
- Zero passwords, tokens, or connection strings committed to Git. GitHub Push Protection and Secret Scanning active.

---

## Answer Part 3: GCP Deployment and Persistence (Issues #16, #20, #23, #24)

### 3.1 Course GCP Infrastructure Setup (Issue #16)
- Course Project ID: `cpe-se-course-2026` (Region: `asia-southeast1`)
- Team Prefix: `s3c35c9bd`
- Dedicated Smallest-Tier Cloud SQL PostgreSQL Instance provisioned.
- Cloud Run Service (`s3c35c9bd`) and Migration Job (`s3c35c9bd-migrate`) created.
- Budget alert configured with thresholds (50%, 90%, 100%) and notification to team.

*(Live URL verification C-04 and persistence checks C-05 to be completed in Issues #20 & #23)*

---

## Answer Part 4: Repeatable Release Pipeline (Issue #22)

*(Section populated during Issue #22)*
- Continuous deployment workflow (`.github/workflows/deploy.yml`).
- Verification C-06: staging → main release PR, automated migration, deployment by commit digest, and smoke test.
