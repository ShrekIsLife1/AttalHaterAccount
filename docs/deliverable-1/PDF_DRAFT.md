# Deliverable 1 — PDF draft (living document)
Status legend: ✅ complete · 🟡 partial · ⬜ not started · 📸 screenshot needed
Release commit: <RELEASE_COMMIT>   Tag: <TAG>

## Front page   (filled in #15)
- Students: Cl (ID …), Ba (ID …)
- Theme / context: Theme 4 — E-Commerce/Ordering — Campus Merchandise Shop
- Repository: https://github.com/ShrekIsLife1/AttalHaterAccount.git
- Release: tag <TAG>, commit <RELEASE_COMMIT>

## Navigation table   (page numbers filled in #15)
| Part | Pages | Main IDs | Execution evidence |
|---|---|---|---|

## Part A — SRS and product scope   ⬜ (#1)
## Part B — Feature inventory and traceability   ⬜ (#2)
## Part C — System-Level SDS   ⬜ (#3)
## Part D — Three-sprint plan   ⬜ (#4)
## Part E — Sprint 1 engineering contracts   ⬜ (#5)

## Part F — Working Sprint 1 and verification
### F.1 Setup summary   ⬜ (#6, #15)
### F.2 Program demonstrations   (release commit: <RELEASE_COMMIT>)
| # | Scenario | Feature/AC | Role | Start conditions | Steps | Expected | Actual | Evidence file | Status | Issue |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Login | AC-01, AC-18 | Customer | | | | | | ⬜ | #7, #8 |
| S2 | Normal order journey + persisted retrieval | AC-05, AC-06, AC-11 | Customer | | | | | | ⬜ | #10, #11 |
| S3 | DB proof | AC-06, AC-10 | — | | | | | | ⬜ | #10 |
| S4 | Rule rejection | AC-08, AC-09 | Customer | | | | | | ⬜ | #10 |
| S5 | Operator accepts order | AC-14, AC-15 | Operator | | | | | | ⬜ | #12 |
| S6 | Invalid transition (409) | AC-16 | Operator | | | | | | ⬜ | #12 |
| S7 | Forbidden role operation | AC-13 | Customer | | | | | | ⬜ | #12, #13 |
| S8 | Ownership restriction | AC-12 | Customer | | | | | | ⬜ | #13 |
| S9 | Unauthenticated access | AC-03 | — | | | | | | ⬜ | #7, #13 |
| S10 | Logout | AC-04 | Customer | | | | | | ⬜ | #7 |
### F.3 Build and automated test results
- Commands and tested commit:
- Passed / failed / skipped counts:
| AC | Planned TEST | Actual test file / name | Level | Result | Issue |
|---|---|---|---|---|---|
- Excerpt 1 (domain rule): ⬜ (#10)
- Excerpt 2 (ownership restriction): ⬜ (#13)
- TDD evidence (failing → passing, commit hashes): ⬜ (#7, #10, #12)
### F.4 Engineering workflow and history
| Issue | Feature/AC | Branch | Author | Reviewer | Review comment | Merged to staging | Merged to main |
|---|---|---|---|---|---|---|---|
History sequence (contract → tests → implementation):
| Date | Commit | What |
|---|---|---|
Board status screenshot: ⬜ (#15)   Release PR / tag: ⬜ (#15)
### F.5 Contributions, AI use, limitations
| Student | Issues/PRs authored | PRs reviewed | Pair work |
|---|---|---|---|
AI-use declaration:
Known limitations / incomplete work / skipped tests:
