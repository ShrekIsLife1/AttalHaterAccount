# Software Test Specification (STS) — Sprint 1 Baseline

**Project:** UniMerch Campus Store (Theme 4: E-Commerce or Ordering System)  
**Course:** CPE 334 — Introduction to Software Engineering in the Age of AI Agents  
**Authors:** Student Ba (Author, Issue #5) & Student Cl (Reviewer)  
**Scope:** Complete Sprint 1 Test Plan (TEST-01 to TEST-26)  
**Status:** Approved Engineering Contract Baseline  

---

## 1. Test Strategy & Traceability Overview

The Sprint 1 Software Test Specification maps **every single Acceptance Criterion (`AC-01` through `AC-20`)** to concrete, automated, reproducible tests across the test pyramid:
- **Unit Tests:** Isolated business logic and input boundary calculations (pricing, quantity bounds, duplicate checks).
- **API / Integration Tests:** Supertest HTTP endpoint execution against real PostgreSQL instance, validating status codes, cookies, JSON schemas, rollbacks, and RBAC guards.
- **UI / Component Tests:** Vitest + React Testing Library verifying role-based navigation, empty states, and error handling.
- **E2E Tests:** Playwright browser automation simulating complete customer and operator domain journeys.
- **Persistence & Idempotence Tests:** Dedicated script and tests proving database survival across server restarts and deterministic seed execution.

---

## 2. STS Master Test Matrix

| TEST ID | Linked AC | Level | Precondition / Input Data | Action Executed | Expected Result & Assertions | Planned File Path |
|---|---|---|---|---|---|---|
| **TEST-01** | AC-01 | API | Seeded customer account exists in DB | `POST /api/auth/login` with valid email & password | HTTP 200, `Set-Cookie` header contains `sid` (`HttpOnly`), response body returns `{ id, email, role: 'CUSTOMER' }` without password hash | `server/tests/sprint-1/auth.api.test.ts` |
| **TEST-02** | AC-02 | API | Non-existent email or wrong password | `POST /api/auth/login` with invalid credentials | HTTP 401 Unauthorized, generic error `{ "error": "Invalid email or password" }`, no cookie set | `server/tests/sprint-1/auth.api.test.ts` |
| **TEST-03** | AC-03 | API | No session cookie or expired session | `GET /api/auth/me` and `GET /api/orders` | HTTP 401 Unauthorized, empty/safe error body, no protected data exposed | `server/tests/sprint-1/auth.api.test.ts` |
| **TEST-04** | AC-04 | API | Active authenticated session | `POST /api/auth/logout` followed by `GET /api/auth/me` | Logout returns HTTP 200; subsequent `/me` returns HTTP 401; session record deleted in DB | `server/tests/sprint-1/auth.api.test.ts` |
| **TEST-05** | AC-05 | API | Seeded catalog with active and inactive items | `GET /api/products` | HTTP 200, returns active items with integer `priceMinor` and stock availability badge; inactive items are omitted | `server/tests/sprint-1/catalog.api.test.ts` |
| **TEST-06** | AC-05 | UI | Seeded products returned by API mock | Render `<Catalog />` component | Displays active product cards, formatted THB prices, "In Stock" badge for stock > 0, and disabled "Unavailable" button for stock = 0 | `client/tests/sprint-1/Catalog.test.tsx` |
| **TEST-07** | AC-06 | API | Authenticated customer, valid items with stock | `POST /api/orders` with `[{ productId, quantity: 2 }]` | HTTP 201 Created, status `PLACED`, total equals server calculation, DB stock decremented by 2, `unitPriceAtOrder` snapshotted | `server/tests/sprint-1/orders-create.api.test.ts` |
| **TEST-08** | AC-07 | API | Authenticated customer, payload contains forged `price: 1` or `total: 100` | `POST /api/orders` with tampered price data | HTTP 201 Created, order total matches authoritative DB price calculation, forged client values completely ignored | `server/tests/sprint-1/orders-create.api.test.ts` |
| **TEST-09** | AC-08 | Unit | Pure pricing/validation domain service | Calculate order with `qty = 0`, `-1`, `1.5`, `11`, or duplicate item IDs | Validation throws domain validation exception for each boundary violation | `server/tests/sprint-1/orders-pricing.unit.test.ts` |
| **TEST-10** | AC-08 | API | Authenticated customer, empty `items: []` or `quantity: 0` | `POST /api/orders` with invalid quantity | HTTP 400 Bad Request with field validation errors; zero orders or items created in database | `server/tests/sprint-1/orders-create.api.test.ts` |
| **TEST-11** | AC-09 | API | Authenticated customer, requested item has `stock = 1`, requested `qty = 2` | `POST /api/orders` exceeding stock | HTTP 400 Bad Request, error indicates stockout; atomic transaction rolls back; stock remains exactly 1 | `server/tests/sprint-1/orders-create.api.test.ts` |
| **TEST-12** | AC-10 | API | Existing order placed with hoodie at ฿750; update product catalog price to ฿900 in DB | `GET /api/orders/:id` for existing order | HTTP 200, `unitPriceAtOrder` remains ฿750; historical order total unaffected by catalog price change | `server/tests/sprint-1/orders-create.api.test.ts` |
| **TEST-13** | AC-11 | API | Customer A has 2 orders; Customer B has 1 order | `GET /api/orders` as Customer A | HTTP 200, returns exactly Customer A's 2 orders sorted newest first; Customer B's order is absent | `server/tests/sprint-1/orders-access.api.test.ts` |
| **TEST-14** | AC-11 | UI | Customer orders returned by mock API | Render `<MyOrders />` component | Displays list of orders with IDs, date, `PLACED` badge, total amount, and link to details | `client/tests/sprint-1/MyOrders.test.tsx` |
| **TEST-15** | AC-12 | API | Order B belongs to Customer B; Customer A is authenticated | `GET /api/orders/:idB` as Customer A | HTTP 404 Not Found with generic error payload; no order metadata or existence confirmation leaked | `server/tests/sprint-1/orders-access.api.test.ts` |
| **TEST-16** | AC-13 | API | Authenticated user with role `CUSTOMER` | `GET /api/operator/orders` and `PATCH /api/operator/orders/:id/accept` | HTTP 403 Forbidden with `{ "error": "Operator access required" }` | `server/tests/sprint-1/operator-orders.api.test.ts` |
| **TEST-17** | AC-14 | API | 3 orders placed in DB at different timestamps | `GET /api/operator/orders` as Operator | HTTP 200, returns incoming `PLACED` orders ordered chronologically (oldest first) | `server/tests/sprint-1/operator-orders.api.test.ts` |
| **TEST-18** | AC-14 | UI | Incoming orders mock data | Render `<OperatorOrders />` component | Displays table with incoming orders, customer emails, order lines, and enabled "Accept" button | `client/tests/sprint-1/OperatorOrders.test.tsx` |
| **TEST-19** | AC-15 | API | Order in status `PLACED`, authenticated operator | `PATCH /api/operator/orders/:id/accept` | HTTP 200, status updated to `ACCEPTED`, `acceptedAt` timestamp set, `acceptedByOperatorId` matches session operator ID | `server/tests/sprint-1/operator-orders.api.test.ts` |
| **TEST-20** | AC-16 | API | Order already in status `ACCEPTED` | `PATCH /api/operator/orders/:id/accept` second time | HTTP 409 Conflict with `{ "error": "Order cannot be accepted from current status" }`; state unchanged | `server/tests/sprint-1/operator-orders.api.test.ts` |
| **TEST-21** | AC-17 | Persistence | Orders and users present; seed script executed twice consecutively | Execute `npm run seed && npm run seed` | Both seed runs exit code 0; record counts identical; zero duplicate key constraint violations | `server/tests/sprint-1/persistence.api.test.ts` |
| **TEST-22** | AC-18 | UI | Render login screen with mock auth context | Submit login form with Customer vs Operator credentials | Customer login redirects to `/catalog` with Customer shell; Operator login redirects to `/operator/orders` with Operator shell | `client/tests/sprint-1/Login.test.tsx` |
| **TEST-23** | AC-18 | UI | Authenticated user clicks Logout | Click logout button | Calls logout API, clears auth context, redirects to `/login` | `client/tests/sprint-1/Login.test.tsx` |
| **TEST-24** | AC-19 | E2E | Browser instance, seeded test database | Complete Customer journey: Login $\rightarrow$ browse catalog $\rightarrow$ add to cart $\rightarrow$ submit order $\rightarrow$ verify order in My Orders | Order created in DB, visible on customer screen, stock decremented in catalog | `server/tests/sprint-1/e2e-workflow.api.test.ts` & `client/tests/sprint-1/WorkflowE2E.test.tsx` |
| **TEST-25** | AC-19 | E2E | Order placed from TEST-24 | Operator journey: Login $\rightarrow$ view incoming queue $\rightarrow$ click accept $\rightarrow$ confirm status is `ACCEPTED` | Order accepted in DB, disappears from `PLACED` queue; Customer reloads and sees `ACCEPTED` status | `server/tests/sprint-1/e2e-workflow.api.test.ts` & `client/tests/sprint-1/WorkflowE2E.test.tsx` |
| **TEST-26** | AC-20 | E2E | Customer browser session | Customer attempts operator queue/accept routes; out-of-stock order submission; cross-customer order lookup | UI redirects / hides operator controls; backend returns 401/403/400/404 with atomic rollback and zero leak | `server/tests/sprint-1/e2e-workflow.api.test.ts` & `client/tests/sprint-1/WorkflowE2E.test.tsx` |

---

## 3. Permission Matrix Verification Table (System SDS Alignment)

The following verification matrix directly mirrors the **Role and Permission Matrix** in `docs/system-sds.md` (Section 5) and maps every Sprint 1 endpoint and security boundary to its automated regression test:

| Protected Operation | Endpoint | Anonymous | Customer | Operator | Scope / Ownership Constraint | Automated Test Coverage | Status |
|---|---|:---:|:---:|:---:|---|---|:---:|
| **Login** | `POST /api/auth/login` | Allowed | Allowed | Allowed | Authenticates valid credentials, sets `HttpOnly` session cookie; rejects invalid or inactive credentials with generic 401 | `server/tests/sprint-1/auth.api.test.ts` (TEST-01, TEST-02), `authorization.api.test.ts` | ✅ PASS |
| **Logout** | `POST /api/auth/logout` | 401 | Allowed | Allowed | Invalidates acting session in database and clears `sid` cookie | `server/tests/sprint-1/auth.api.test.ts` (TEST-04), `authorization.api.test.ts` | ✅ PASS |
| **Get Current User** | `GET /api/auth/me` | 401 | Allowed | Allowed | Reads acting user profile without password hash; rejects missing, forged, expired or deactivated session | `server/tests/sprint-1/auth.api.test.ts` (TEST-03), `authorization.api.test.ts` | ✅ PASS |
| **Browse Catalog** | `GET /api/products` | Allowed | Allowed | Allowed | Public access; strictly returns active items (`isActive = true`) with integer `priceMinor` | `server/tests/sprint-1/catalog.api.test.ts` (TEST-05) | ✅ PASS |
| **Place Order** | `POST /api/orders` | 401 | **Allowed** | 403 | Bound to acting `session.userId`; server authoritative pricing; atomic stock decrement; Operator receives 403 | `server/tests/sprint-1/orders-create.api.test.ts` (TEST-07..TEST-12), `authorization.api.test.ts` | ✅ PASS |
| **List My Orders** | `GET /api/orders` | 401 | **Allowed** | 403 | Strict filter: `customerId == userId`, sorted newest first; Operator receives 403 | `server/tests/sprint-1/orders-access.api.test.ts` (TEST-13), `authorization.api.test.ts` | ✅ PASS |
| **View Order Detail** | `GET /api/orders/:id` | 401 | **Conditional** | **Allowed** | Customer: own order only (else 404 Not Found without leak); Operator: any store order | `server/tests/sprint-1/orders-access.api.test.ts` (TEST-15), `authorization.api.test.ts` | ✅ PASS |
| **List Incoming Orders** | `GET /api/operator/orders` | 401 | 403 | **Allowed** | Operator only; chronological `PLACED` queue; Customer receives 403 | `server/tests/sprint-1/operator-orders.api.test.ts` (TEST-16, TEST-17), `authorization.api.test.ts` | ✅ PASS |
| **Accept Order** | `PATCH /api/operator/orders/:id/accept` | 401 | 403 | **Allowed** | Operator only; transitions `PLACED -> ACCEPTED`; Customer receives 403; non-PLACED receives 409 Conflict | `server/tests/sprint-1/operator-orders.api.test.ts` (TEST-16, TEST-19, TEST-20), `authorization.api.test.ts` | ✅ PASS |

