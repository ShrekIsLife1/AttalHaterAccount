# Product Definition of Done (DoD) — Sprint 1 Baseline

**Project:** UniMerch Campus Store (Theme 4: E-Commerce or Ordering System)  
**Course:** CPE 334 — Introduction to Software Engineering in the Age of AI Agents  
**Authors:** Student Ba (Author, Issue #5) & Student Cl (Reviewer)  
**Status:** Approved Engineering Contract Baseline  

---

## 1. Purpose & Application Scope

This Definition of Done (DoD) governs all engineering work delivered during Sprint 1. An Issue, feature branch, or Pull Request is strictly considered **Done** only when all criteria in this checklist are verified and approved by the peer reviewer before merging into `sprint1-staging`.

---

## 2. Global Definition of Done Checklist

### 2.1 Specification & Contract Adherence
- [ ] **Contract Compliance:** The implemented behavior strictly adheres to the engineering contracts defined in `docs/sprints/sprint-1/` (`F-01` through `F-05`). Any deviations or necessary refinements are documented with explicit justification in the contract and living draft.
- [ ] **Boundary & Negative Cases Handled:** All edge conditions (e.g. quantity boundaries $1 \le \text{qty} \le 10$, empty arrays, inactive products, insufficient stock, double acceptance, cross-user order queries) are explicitly handled with documented HTTP status codes (`400`, `401`, `403`, `404`, `409`).

### 2.2 Testing & Quality Assurance
- [ ] **Test Coverage:** All planned tests from the Software Test Specification (`docs/sprints/sprint-1/sts.md`, `TEST-01` through `TEST-26`) are implemented and passing.
- [ ] **TDD Workflow Followed:** For TDD Issues (`#7`, `#10`, `#12`), the author commits failing tests first (`test: ...`), followed by implementation (`feat: ...`). Git commit history proves test precedence.
- [ ] **No Weakened Tests:** No automated assertion is stubbed, commented out, or weakened to produce false passes. Skipped or incomplete work is disclosed transparently in the living draft.
- [ ] **Command & Counts Recorded:** The test command, tested commit hash, and passed/failed counts are captured and recorded in the PR description and evidence logs.

### 2.3 Code Quality & Security
- [ ] **No Hardcoded Secrets:** Passwords, tokens, database credentials, and session secrets are never committed to Git or embedded in test fixtures. All credentials are read from environment variables or seed configuration files.
- [ ] **Authoritative Calculations:** Monetary calculations (`priceMinor`, `totalMinor`) are executed exclusively on the server in integer minor units (satang). Float arithmetic is strictly prohibited.
- [ ] **Peer Understanding:** The PR diff has been inspected line-by-line by the author, and both teammates understand all AI-assisted implementation logic.

### 2.4 Living PDF Draft & Evidence Capture
- [ ] **Living Draft Updated:** `docs/deliverable-1/PDF_DRAFT.md` is updated in the same PR with the sections, tables, and scenario walkthroughs contributed by this Issue.
- [ ] **Execution Evidence Preserved:** Test execution logs and UI screenshots are saved under `docs/deliverable-1/evidence/` using the standard naming convention: `issue-<NN>_<AC-or-scenario>_<description>.<txt|png>`.
- [ ] **ODT Document Regenerated:** `docs/deliverable-1/deliverable-1.odt` is re-rendered to ensure continuous readiness for submission.

### 2.5 GitHub Workflow & Integration
- [ ] **Dedicated Branch:** Work performed on a feature branch branched from `sprint1-staging`.
- [ ] **PR Template Filled:** PR description references the linked Issue, lists Feature/AC IDs, provides test execution commands/results, and updates the checklist.
- [ ] **Substantive Peer Review:** The other teammate conducts a thorough code review and posts a specific, substantive check/finding (never just "LGTM").
- [ ] **Integrated & Closed:** PR merged into `sprint1-staging` via clean merge, and the GitHub Issue is moved to `Done` on the Project board.
