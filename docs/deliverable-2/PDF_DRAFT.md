# Lab 5 — UniMerch Campus Store: Cloud Deployment & CI/CD on GCP

**Team:** `AttalHaterAccount` (Theme 4 — UniMerch Campus Store)  
**Baptiste Carré** — Student ID `69540460014` (`@ShrekIsLife1`)  
**Clément Dominique Delrieu** — Student ID `69540460016` (`@ClemDelGh`)  
**GitHub repository:** https://github.com/ShrekIsLife1/AttalHaterAccount  
**Live Cloud Run URL:** https://s3c35c9bd-4d7hbszvwq-as.a.run.app  

---

## Answer Part 0 — Team & Evidence Index

**Repository:** https://github.com/ShrekIsLife1/AttalHaterAccount  
**Issues:** https://github.com/ShrekIsLife1/AttalHaterAccount/issues  
**Pull Requests:** https://github.com/ShrekIsLife1/AttalHaterAccount/pulls  
**Deployment Docs:** https://github.com/ShrekIsLife1/AttalHaterAccount/blob/main/docs/labs/lab05/deployment.md  
**Test Matrix:** https://github.com/ShrekIsLife1/AttalHaterAccount/blob/main/docs/labs/lab05/tests.md  

### 0.1 Pair Contributions (#16–#25)

| Issue | Title | Author | Reviewer | PR |
|---|---|:---:|:---:|---|
| #16 | GCP account, project, budget alert & baseline | Ba | Cl | #44 |
| #17 | Cloud-ready config, probes, `.env.example` | Cl | Ba | #45 |
| #18 | Dockerize application & container verification | Ba | Cl | #46 |
| #19 | CI on Pull Requests (`test-and-docker`, C-01) | Cl | Ba | #47 |
| #20 | First deployment to GCP & domain journey (C-04) | Ba | Cl | #48 |
| #21 | GitHub ↔ GCP (WIF) & failing PR gate (C-02) | Cl | Ba | #50 |
| #22 | Repeatable deploy pipeline & release commit (C-06) | Ba | Cl | #51 |
| #23 | Cloud persistence & rollback verification (C-05) | Cl | Ba | #52 |
| #24 | Cost control: pause/resume Cloud SQL & quota audit | Ba | Cl | #49 |
| #25 | Final deployment docs & deliverable PDF | Cl | Ba | #53 |

### 0.2 Commit History on `main` (feature branches → `lab5-staging` → `main`)

> *[Screenshot: GitHub Insights → Network graph]*

### 0.3 Public Repository Verified in Incognito

> *[Screenshot: Repository opened in incognito browser]*

---

## Answer Part 1 — CI and Quality Gate (C-01, C-02)

**CI Workflow:** https://github.com/ShrekIsLife1/AttalHaterAccount/blob/main/.github/workflows/ci-docker.yml

### 1.1 Check C-01 — Passing PR (`test-and-docker`)

> *[Screenshot: Passing `test-and-docker` run on PR #47 / #50]*

### 1.2 Check C-02 — Branch Protection & Blocked Failing PR

> *[Screenshot: Branch protection ruleset (`lab5-staging` & `main`) requiring `test-and-docker`]*

> *[Screenshot: Failing PR blocked — "Required status checks must pass before merging"]*

### 1.3 Workload Identity Federation (`environment: demo`)

> *[Screenshot: GitHub Settings → Environments → demo variables (`WIF_PROVIDER`, `WIF_SERVICE_ACCOUNT`, `GCP_PROJECT_ID`, `GCP_REGION`) — zero JSON key]*

---

## Answer Part 2 — Docker and Reproducible Configuration (C-03)

**Dockerfile:** https://github.com/ShrekIsLife1/AttalHaterAccount/blob/main/Dockerfile  
**Docker Compose:** https://github.com/ShrekIsLife1/AttalHaterAccount/blob/main/docker-compose.yml  
**.env.example:** https://github.com/ShrekIsLife1/AttalHaterAccount/blob/main/.env.example  

### 2.1 Check C-03 — Clean `docker build` & `docker compose up` (`TEST-L5-10..14`)

> *[Screenshot: Terminal `bash scripts/test-container.sh` — non-root UID 1000, `/api/ready` 200, `/api/version` matches `GIT_SHA`]*

---

## Answer Part 3 — GCP Deployment and Persistence (C-04, C-05)

**Live URL:** https://s3c35c9bd-4d7hbszvwq-as.a.run.app

### 3.1 Check C-04 — Live Domain Customer Journey (`TEST-L5-20..25`)

> *[Screenshot: `GET /api/ready` returning `{"status":"ready","db":"connected"}`]*

> *[Screenshot: Customer sign in → add to cart → checkout → order detail on Cloud Run URL]*

> *[Screenshot: Business rule rejection (400/409) & RBAC 403 on operator route]*

### 3.2 Check C-05 — Cloud Persistence & Rollback (`TEST-L5-43..47`)

> *[Screenshot: Customer order persists in `/api/orders/my-orders` after Cloud Run restart / redeploy]*

> *[Screenshot: Cloud SQL pause/resume (`TEST-L5-48..51`) & Cloud Run `min-instances=0`]*

---

## Answer Part 4 — Repeatable Release Pipeline (C-06)

**CD Workflow:** https://github.com/ShrekIsLife1/AttalHaterAccount/blob/main/.github/workflows/deploy.yml

### 4.1 Check C-06 — Automated Release on `main` (`TEST-L5-32..42`)

> *[Screenshot: `Deploy demo` GitHub Actions run green (`test-and-docker` → WIF auth → build/push → `release.sh` → `smoke_test.py`)]*

### 4.2 Release Revision Matches Commit SHA (R-08)

> *[Screenshot: `curl https://s3c35c9bd-4d7hbszvwq-as.a.run.app/api/version` matching `main` release commit SHA]*
