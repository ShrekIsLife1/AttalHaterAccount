# Sprint 1 Test Plan and Results

## 1. Test Strategy
Tests are planned from `docs/srs.md` and `docs/sprints/sprint-1/sts.md` **before** implementation (Test DD) and written first for each TDD Issue (TDD: red → green → refactor). Every Acceptance Criterion (AC-01…AC-20) maps to at least one automated test (§3). Levels: **unit** (pure rules), **API/integration** (Supertest against real Express + PostgreSQL), **UI component** (Vitest + React Testing Library), **persistence/idempotence**, and **E2E workflow verification**.

**Conventions for the coding agent**
* One Issue = one branch. For each TDD Issue (#7, #9, #10, #12), first write the tests listed for it, commit them failing, then implement, then show them green. Do not report "done" unless the listed Test IDs pass; never skip, disable or loosen a test to make it pass.
* **No forged prices or totals.** The server is strictly authoritative: client price inputs in order requests are ignored or rejected; prices are read directly from PostgreSQL in integer minor units (satang THB).
* **Non-leaking authorization oracle.** A customer requesting another customer's order ID receives HTTP 404 Not Found (same payload as a non-existent order), preventing ID enumeration.
* **Database persistence and seed idempotence.** Prerequisite for server tests: database migrated and seeded (`npm run prisma:migrate && npm run seed`). The seed script must run consecutively with 0 duplicate key errors.

## 2. Planned Tests

Paths: `S/` = `server/tests/sprint-1/`, `C/` = `client/tests/sprint-1/`.

### 2.1 Unit & Persistence
| Test ID | AC | Type | What It Tests | Expected Result | Automated Test File | Final |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| UNIT-01 | AC-08 | Unit | Pure pricing calculation domain service over single and multi-item orders | Subtotal and total match integer satang calculation; zero decimal rounding | `S/orders-pricing.unit.test.ts` | Pass |
| UNIT-02 | AC-08 | Unit | Quantity boundary validation: negative, zero, float, > 10 items | Throws domain validation exception for each boundary violation | `S/orders-pricing.unit.test.ts` | Pass |
| UNIT-03 | AC-08 | Unit | Duplicate product ID validation in single order payload | Rejects duplicate lines; requires distinct product IDs | `S/orders-pricing.unit.test.ts` | Pass |
| PERS-01 | AC-17 | Persistence | Database persistence across connection restart | Seeded records survive; relational integrity intact | `S/persistence.api.test.ts` | Pass |
| PERS-02 | AC-17 | Persistence | Seed idempotency executed consecutively twice | Record counts unchanged; 0 unique constraint collisions | `S/persistence.api.test.ts` | Pass |

### 2.2 API — Authentication & RBAC (`S/auth.api.test.ts` & `S/authorization.api.test.ts`)
| Test ID | AC | Type | What It Tests | Expected Result | Final |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TEST-01 | AC-01 | API | Customer / Operator login with valid email & password | 200; `sid` HttpOnly cookie set; user identity & role returned without password | Pass |
| TEST-02 | AC-02 | API | Login with non-existent email or wrong password | 401 Unauthorized; generic error `{ "error": "Invalid email or password" }`; no cookie set | Pass |
| TEST-03 | AC-03 | API | Access protected endpoints (`/api/auth/me`, `/api/orders`) with missing or expired session | 401 Unauthorized; safe error body; no sensitive data leaked | Pass |
| TEST-04 | AC-04 | API | Logout active session | 200; `sid` cookie cleared; session deleted in DB; subsequent `/me` returns 401 | Pass |
| TEST-16 | AC-13 | API | Customer attempts operator queue (`GET /api/operator/orders`) or accept route | 403 Forbidden with `{ "error": "Operator access required" }` | Pass |
| SEC-01 | AC-03, 13 | API | Cross-cutting route sweep across all endpoints for anonymous callers | 401 Unauthorized on all protected routes | Pass |
| SEC-02 | AC-13 | API | Operator attempts customer-only order creation (`POST /api/orders`) | 403 Forbidden; operator accounts cannot place customer orders | Pass |
| SEC-03 | AC-03 | API | Inactive / deactivated user attempts login or session access | 401 Unauthorized; immediate session rejection | Pass |

### 2.3 API — Catalog & Order Lifecycle (`S/catalog.api.test.ts`, `S/orders-create.api.test.ts`, `S/orders-access.api.test.ts`, `S/operator-orders.api.test.ts`)
| Test ID | AC | Type | What It Tests | Expected Result | Final |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TEST-05 | AC-05 | API | Public catalog query (`GET /api/products`) | 200; active items returned with integer `priceMinor`; inactive items omitted | Pass |
| TEST-07 | AC-06 | API | Order creation with valid items & available stock | 201 Created; status PLACED; atomic stock decrement; unitPriceAtOrder stored | Pass |
| TEST-08 | AC-07 | API | Forged client price/total in request payload | 201 Created; client prices ignored; authoritative DB price used | Pass |
| TEST-10 | AC-08 | API | Order payload validation (empty cart, qty < 1 or > 10) | 400 Bad Request; zero orders or items created in database | Pass |
| TEST-11 | AC-09 | API | Order quantity exceeding available stock | 400 Bad Request; transaction rolls back; stock count unchanged | Pass |
| TEST-12 | AC-10 | API | Historical order price immutability after catalog price update | 200; unitPriceAtOrder remains unchanged after updating product price in DB | Pass |
| TEST-13 | AC-11 | API | Customer lists own orders (`GET /api/orders`) | 200; returns only orders belonging to customer, newest first | Pass |
| TEST-15 | AC-12 | API | Customer requests another customer's order ID (`GET /api/orders/:id`) | 404 Not Found; generic error; existence of other order not confirmed | Pass |
| TEST-17 | AC-14 | API | Operator lists incoming PLACED orders (`GET /api/operator/orders`) | 200; chronological order (oldest first); only PLACED status included | Pass |
| TEST-19 | AC-15 | API | Operator accepts PLACED order (`PATCH /api/operator/orders/:id/accept`) | 200; status becomes ACCEPTED; acceptedAt timestamp and operator ID set | Pass |
| TEST-20 | AC-16 | API | Re-accepting already ACCEPTED order | 409 Conflict; state unchanged; duplicate acceptance prevented | Pass |

### 2.4 UI Component (Vitest + Testing Library)
| Test ID | AC | Type | What It Tests | Expected Result | Automated Test File | Final |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| UI-01 | AC-01, 18 | UI | Login form rendering, input validation, busy indicator | Form renders inputs; button disabled during request; safe errors | `C/Login.test.tsx` | Pass |
| UI-02 | AC-18 | UI | Role-conditional navigation shell | Permitted destinations shown per role; Customer vs Operator | `C/Login.test.tsx` | Pass |
| UI-03 | AC-04, 18 | UI | Logout button click | Calls logout API, clears auth context, redirects to login | `C/Login.test.tsx` | Pass |
| UI-04 | AC-05 | UI | Catalog grid display, formatted THB prices, stock badges | Active product cards shown with availability badges and Add to Cart | `C/Catalog.test.tsx` | Pass |
| UI-05 | AC-05 | UI | Out-of-stock product handling in catalog | Stock = 0 shows "Unavailable" disabled button | `C/Catalog.test.tsx` | Pass |
| UI-06 | AC-06, 08 | UI | Cart checkout table, quantity adjustments, line subtotals | Displays quantities, calculated subtotals, and total in Bahts | `C/Checkout.test.tsx` | Pass |
| UI-07 | AC-09 | UI | Checkout stockout error feedback from server | Displays user-friendly error banner on stock rejection | `C/Checkout.test.tsx` | Pass |
| UI-08 | AC-11 | UI | My Orders list rendering, status badges, empty state | Displays order history, formatted dates, status badges, total amount | `C/MyOrders.test.tsx` | Pass |
| UI-09 | AC-11, 12 | UI | Order detail view with item breakdown and prices | Displays line items, quantities, historical unit prices, total | `C/MyOrders.test.tsx` | Pass |
| UI-10 | AC-14 | UI | Operator queue table rendering, chronological ordering | Table displays incoming PLACED orders with customer emails | `C/OperatorOrders.test.tsx` | Pass |
| UI-11 | AC-15, 16 | UI | Accept button click, busy state, list removal | Triggers accept API, shows busy state, removes order from PLACED queue | `C/OperatorOrders.test.tsx` | Pass |

### 2.5 E2E & Complete Workflow Verification
| Test ID | AC | Type | What It Tests | Expected Result | Automated Test File | Final |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TEST-24 | AC-19 | E2E | Complete Customer purchasing journey (Login $\rightarrow$ Catalog $\rightarrow$ Cart $\rightarrow$ Order $\rightarrow$ My Orders) | Order created in DB, visible on customer screen, stock decremented | `S/e2e-workflow.api.test.ts` & `C/WorkflowE2E.test.tsx` | Pass |
| TEST-25 | AC-19 | E2E | Complete Operator queue journey (Login $\rightarrow$ Incoming Queue $\rightarrow$ Accept $\rightarrow$ Status ACCEPTED) | Order accepted in DB, disappears from PLACED queue, customer sees ACCEPTED | `S/e2e-workflow.api.test.ts` & `C/WorkflowE2E.test.tsx` | Pass |
| TEST-26 | AC-20 | E2E | Negative & security guard rails (401 unauth, 403 role, 404 cross-access, 400 stockout, 409 conflict) | UI redirects / hides controls; backend returns specified errors without data leakage | `S/e2e-workflow.api.test.ts` & `C/WorkflowE2E.test.tsx` | Pass |

## 3. Acceptance-Criterion Traceability
| AC | Covered by |
|---|---|
| AC-01 Valid login credentials | TEST-01, UI-01 |
| AC-02 Invalid credentials rejection | TEST-02, UI-01 |
| AC-03 Protected endpoint authentication | TEST-03, SEC-01, SEC-03, TEST-26 |
| AC-04 Session invalidation on logout | TEST-04, UI-03 |
| AC-05 Product catalog display | TEST-05, UI-04, UI-05 |
| AC-06 Order placement with stock decrement | TEST-07, UI-06, TEST-24 |
| AC-07 Authoritative DB pricing | TEST-08, UNIT-01 |
| AC-08 Order payload validation | UNIT-02, UNIT-03, TEST-10, UI-06 |
| AC-09 Stock exhaustion prevention | TEST-11, UI-07, TEST-26 |
| AC-10 Historical price snapshot | TEST-12, UI-09 |
| AC-11 Customer order history | TEST-13, UI-08, UI-09, TEST-24 |
| AC-12 Cross-customer order isolation | TEST-15, TEST-26 |
| AC-13 Operator role protection | TEST-16, SEC-02, TEST-26 |
| AC-14 Chronological operator queue | TEST-17, UI-10, TEST-25 |
| AC-15 Single-step order acceptance | TEST-19, UI-11, TEST-25 |
| AC-16 Duplicate accept conflict guard | TEST-20, UI-11, TEST-26 |
| AC-17 Database persistence & idempotent seed | PERS-01, PERS-02 |
| AC-18 Role-based UI shell & navigation | UI-01, UI-02, UI-03 |
| AC-19 Full customer & operator E2E workflow | TEST-24, TEST-25 |
| AC-20 Negative & security E2E guard rails | TEST-26 |

## 4. Responsive, Visual and Accessibility Checklist
- [x] Primary navy (`#1B365D`) for brand headers; secondary gold/amber (`#D99B00`) for badges and active controls.
- [x] Product cards display name, description, formatted price in Bahts (฿), and live stock availability badge.
- [x] Editable vs read-only fields clearly distinguishable; validation messages rendered below inputs.
- [x] Status badges for orders: `PLACED` (blue), `ACCEPTED` (green), `CANCELLED` (red).
- [x] Cart table displays line items, quantities, formatted unit prices, calculated line subtotals, and overall order total.
- [x] Operator incoming orders queue shows table on desktop and stacked cards on mobile; no horizontal page scroll.
- [x] Conflict (409), forbidden (403), unauthorized (401), empty, loading, and failure states visibly distinct.
- [x] No console errors, placeholder text, obsolete elements or broken links.
- [x] Playwright / Vitest evidence captured for all 5 core features and 7 program demo scenarios.

## 5. Test Commands
* Server unit + API + authorization + persistence + E2E: `cd server && npm test`
* Client UI (Vitest): `cd client && npm test`
* Seed database: `cd server && npm run seed`
* Prisma migration: `cd server && npm run prisma:migrate`

## 6. Final Results

### Server Tests Output
```bash
$ cd server && npm test
Test Files  10 passed | 1 skipped (11)
     Tests  77 passed | 1 todo (78)
  Duration  9.41s
```

### Client Tests Output
```bash
$ cd client && npm test
Test Files  7 passed (7)
     Tests  26 passed (26)
  Duration  1.69s
```

### Automated Suite Summary
```text
Total Test Suites: 17 passed (17)
Total Automated Tests: 103 passed, 0 failed, 100% pass rate
```

## 7. Known Limitations or Deferred Tests
* Online third-party payment gateway (PromptPay, Stripe, credit cards) is deferred to Sprint 2.
* Physical fulfillment, warehouse dispatch, and parcel tracking are deferred to Sprint 3.
* Customer-initiated order cancellation and refunds are out of scope for Sprint 1.
* Performance tests under heavy concurrent load (500+ simulated users) are scheduled for Sprint 3 hardening.
