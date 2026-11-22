# Deliverable 1 — PDF draft (living document)
Status legend: ✅ complete · 🟡 partial · ⬜ not started · 📸 screenshot needed
Release commit: <RELEASE_COMMIT>   Tag: <TAG>

## Front page   (filled in #15)
- Students: Clément Dominique Delrieu (ID 69540460016, @ClemDelGh), Baptiste Carré (ID 69540460014, @ShrekIsLife1)
- Theme / context: Theme 4 — E-Commerce/Ordering — Campus Merchandise Shop (UniMerch)
- Repository: https://github.com/ShrekIsLife1/AttalHaterAccount.git
- Release: tag <TAG>, commit <RELEASE_COMMIT>

## Navigation table   (page numbers filled in #15)
| Part | Pages | Main IDs | Execution evidence |
|---|---|---|---|

## Part A — SRS and product scope   ✅ (#1)

### A.1 Problem Statement & Context
The **UniMerch Campus Store** is an on-campus merchandise shop serving university students, faculty, alumni, and administrative staff. The shop offers branded merchandise, apparel (hoodies, t-shirts), stationery (notebooks, pens), and everyday campus accessories (water bottles, tote bags, mugs).

Currently, the physical store suffers from substantial operational bottlenecks:
- **Long Counter Queues:** During semester openings and campus events, students wait in long queues just to enquire about product availability and prices.
- **Stock Inconsistencies:** Store operators manually track physical inventory, leading to overselling or discovering that requested items are out of stock after payment attempts.
- **Manual Order Processing:** Paper-based receipts and untracked orders result in delayed fulfillment and occasional misplaced orders.
- **Pricing Discrepancies:** Outdated printed price tags lead to friction at checkout when prices are updated in central store logs.

**Solution Vision:** A robust web-based ordering application that allows customers to view authoritative catalog items with live availability, place multi-item orders with server-validated pricing, and track their order status. Store operators manage an organized incoming queue, review order lines, and progress orders through transparent fulfillment stages.

### A.2 Actors and Responsibilities
| Actor | Description | Core Responsibilities |
|---|---|---|
| **Customer** | Enrolled student or staff member purchasing merchandise | - Authenticate securely via email and password.<br>- Browse product catalog with authoritative prices and stock availability.<br>- Assemble and submit multi-line orders.<br>- View own order history and track order status.<br>- Cannot modify catalog, cannot accept orders, cannot view other customers' orders. |
| **Operator** | Campus store staff member managing fulfillment and catalog | - Authenticate securely via email and password.<br>- View incoming orders queue (`PLACED`) sorted chronologically.<br>- Accept incoming orders (`PLACED -> ACCEPTED`) with recorded timestamp and operator identity.<br>- Progress order fulfillment in subsequent sprints (`PREPARING -> READY -> COMPLETED`).<br>- Manage catalog items, pricing, and stock levels (Sprint 2).<br>- Cannot place orders as an operator; accesses customer orders within store scope. |

### A.3 Product Scope and Explicit Exclusions
- **In Scope:**
  - **Sprint 1 (Baseline & Working Slice):** Session-based authentication with role-based access control (`CUSTOMER`, `OPERATOR`); read-only catalog with live availability badges and minor-unit prices; multi-line order placement with server-side authoritative pricing, stock validation, atomic inventory decrement; customer order history and detail view; operator incoming orders queue and acceptance transition (`PLACED -> ACCEPTED`); persistent PostgreSQL database with idempotent seeding.
  - **Sprint 2 (Core Expansion):** Operator catalog management (create, update, toggle active status, restock); order cancellation by customer and rejection by operator; extended fulfillment lifecycle (`ACCEPTED -> PREPARING -> READY -> COMPLETED`); simulated payment workflow.
  - **Sprint 3 (Hardening & Analytics):** Operator sales and order analytics dashboard; order search and filtering; hardened error handling and performance benchmarks.
- **Explicit Exclusions:**
  - *No Real Payment Gateways:* Real payment integrations (Stripe, PayPal, banking APIs) are strictly excluded; simulated payment states are used.
  - *No External Delivery / Logistics APIs:* Pickup occurs on campus at the UniMerch service counter; no external courier tracking is integrated.
  - *No External Messaging Providers:* No external SMS/email services; all status updates remain internal to the web platform.
  - *No Self-Registration or Password Recovery in Sprint 1:* Seeded demo accounts with pre-hashed credentials are used.

### A.4 Functional Requirements (FR)
- **FR-01 (User Authentication):** A user can submit valid credentials (email and password) to log in. The system creates a secure session and returns the user's profile (`id`, `name`, `role`). Password hashes are never returned.
- **FR-02 (User Logout):** An authenticated user can log out. The backend invalidates the session server-side, clearing the authentication cookie. Subsequent requests with the terminated session are rejected.
- **FR-03 (Catalog Browsing):** An authenticated customer or operator can retrieve the catalog of products. Each product displays name, description, unit price (formatted in minor units), and an availability status (`inStock` or `unavailable`).
- **FR-04 (Order Placement):** A customer can submit an order containing 1 to $N$ distinct product lines with specified quantities. The server computes the total authoritatively, validates stock, snapshots unit prices, decrements inventory, and saves the order in `PLACED` status in a single atomic transaction.
- **FR-05 (Customer Order History & Detail):** A customer can view a list of all orders they previously placed (showing order ID, date, status, and total). The customer can open any of their own orders to inspect full line details.
- **FR-06 (Operator Incoming Orders):** An operator can view a queue of all incoming orders with `status = PLACED`, ordered chronologically (oldest first) to ensure fair first-in-first-out processing.
- **FR-07 (Operator Order Acceptance):** An operator can accept a `PLACED` order. The backend updates the order `status = ACCEPTED`, records `acceptedAt` timestamp, and records `acceptedByOperatorId` referencing the acting operator.
- **FR-08 (Operator Catalog Management - Sprint 2):** An operator can create a new product, edit metadata, adjust stock, and toggle active status.
- **FR-09 (Order Cancellation and Rejection - Sprint 2):** A customer can cancel a `PLACED` order; an operator can reject a `PLACED` order with a reason note.
- **FR-10 (Extended Fulfillment Transitions - Sprint 2):** Operators advance orders sequentially: `ACCEPTED -> PREPARING -> READY -> COMPLETED`.
- **FR-11 (Simulated Payment Processing - Sprint 2):** Customers execute simulated payments, transitioning status to `PAID` with a generated synthetic reference.
- **FR-12 (Sales and Order Analytics - Sprint 3):** Operators view aggregated sales metrics, revenue, order breakdown by status, and inventory turnover.
- **FR-13 (Order Search and Filtering - Sprint 3):** Customers and operators search and filter orders by status, date range, or customer.

### A.5 Business Rules (BR)
- **BR-01 (Authoritative Server-Side Pricing):** Order line totals and order grand totals must be calculated strictly on the backend using authoritative product prices stored in the database. Any client-submitted `price`, `unitPrice`, or `total` in the request body is completely ignored.
- **BR-02 (Line Quantity Boundaries):** Each order line `quantity` must be a positive integer such that $1 \le \text{quantity} \le \text{MAX\_QTY\_PER\_LINE}$ (configured to 10). Quantities $\le 0$, non-integers, missing values, or values $> 10$ must be rejected with HTTP 400.
- **BR-03 (Inventory Availability & Atomicity):** A product is orderable only if `isActive = true` and `stockQuantity >= requested_quantity`. An order cannot contain duplicate product entries across multiple lines. If any line item is unavailable or invalid, the entire order submission is rejected (HTTP 400 or 409), no partial order is saved, and product stock remains unchanged (all-or-nothing database transaction).
- **BR-04 (Price Snapshot Immutability):** When an order is created, the current unit price of each item is captured in `OrderItem.unitPriceAtOrder`. Any subsequent price updates to `Product.priceMinor` in the catalog must never alter historical orders or their computed totals.
- **BR-05 (Customer Ownership & Privacy):** A customer can access only orders where `Order.customerId` matches their own authenticated user ID. Any request by Customer A to read or inspect Customer B's order must return HTTP 404 (Not Found) without confirming the existence of the record or leaking private data.
- **BR-06 (Strict State Transition Lifecycle):** In Sprint 1, the only permitted order state transition is `PLACED -> ACCEPTED` initiated by an operator. Transitioning an order that is already `ACCEPTED` (or in any other status) must be rejected with HTTP 409 (Conflict), leaving database state untouched.
- **BR-07 (Secure Credential Storage):** Passwords must never be stored in plaintext. Passwords must be hashed using a salted cryptographic hashing algorithm (bcrypt with minimum work factor 10 or argon2) prior to database insertion.
- **BR-08 (Operator Scope and Role Restrictions):** Only authenticated users with role `OPERATOR` are authorized to list incoming orders or trigger the accept transition. Any request by a `CUSTOMER` to operator endpoints must be rejected with HTTP 403 (Forbidden).

### A.6 Non-Functional Requirements (NFR)
| NFR ID | Requirement Statement | Measurable Target | Verification Method | Sprint |
|---|---|---|---|---|
| **NFR-01** | **Authentication & Role Authorization Enforcement** | 100% of protected routes reject unauthenticated requests with HTTP 401 and empty/safe error payload; role violations return HTTP 403; cross-user order access returns HTTP 404. | Automated integration tests (`auth.api.test.ts`, `orders-access.api.test.ts`, `operator-orders.api.test.ts`). | Sprint 1 |
| **NFR-02** | **Relational Data Persistence Across Restarts** | All database records (users, products, orders, order items, sessions) persist across application process stops and restarts. | Automated persistence test (`persistence.api.test.ts`) that disconnects, queries data, and verifies state intact. | Sprint 1 |
| **NFR-03** | **Seed Reproducibility & Idempotence** | Executing the database seed command consecutively does not produce duplicate rows or trigger constraint violations. | Scripted test running `npm run seed && npm run seed` and asserting identical record counts. | Sprint 1 |
| **NFR-04** | **Fresh Clone Reproducibility** | A developer can clone a fresh repository and execute install, migration, seed, test, and dev server in under 5 minutes following only the `README.md`. | Timed manual and scripted clean-room test on a separate workspace clone. | Sprint 1 |
| **NFR-05** | **Order Placement Latency** | A valid 10-line order creation request responds with HTTP 201 in under $1000\text{ ms}$ on local developer environment. | Automated benchmark test measuring API round-trip duration under local test database. | Sprint 3 |
| **NFR-06** | **Responsive User Interface** | Web application layouts adapt cleanly without horizontal scrolling or clipping across screen widths from $375\text{ px}$ (mobile) to $1920\text{ px}$ (desktop). | Visual inspection and automated Playwright responsive viewport assertions. | Sprint 3 |

### A.7 Assumptions, Frozen Design Decisions, and Open Questions
| Topic / Decision | Chosen Resolution & Justification | Status |
|---|---|---|
| **Domain Context** | Campus merchandise store (UniMerch): single-store catalog, single fulfillment team, student/staff customers. | Frozen |
| **User Roles** | Exactly two roles: `CUSTOMER` and `OPERATOR`. Exactly one role per account. Simplifies Sprint 1 RBAC while fulfilling rubric requirements. | Frozen |
| **Monetary Representation** | All currency values (`priceMinor`, `totalMinor`, `unitPriceAtOrder`) are stored strictly as **integers in minor units** (e.g., satang or cents; 100 minor units = 1 unit). Float arithmetic is strictly prohibited to avoid rounding errors. Currency fixed to THB. | Frozen |
| **Sprint 1 Order Statuses** | Exactly two statuses in Sprint 1: `PLACED` and `ACCEPTED`. Later sprints introduce `REJECTED`, `CANCELLED`, `PREPARING`, `READY`, `COMPLETED`. | Frozen |
| **Order Lines & Limits** | 1 to $N$ lines per order. `quantity` between 1 and $\text{MAX\_QTY\_PER\_LINE} = 10$. Duplicate items within one order payload are rejected (HTTP 400). | Frozen |
| **Inventory Management** | `Product.isActive` (boolean) and `Product.stockQuantity` (integer $\ge 0$). Decremented atomically in the same database transaction as order creation. If stock is insufficient, whole order fails. | Frozen |
| **Authoritative Pricing** | Server re-queries database for product prices at order creation time. Any client-sent totals or prices are discarded. | Frozen |
| **Price Snapshot** | `OrderItem.unitPriceAtOrder` records unit price at order placement time. Future product catalog price changes never mutate historical orders. | Frozen |
| **Authentication Mechanism** | Server-side session table (`Session`) with cryptographically secure random session tokens delivered in `HttpOnly`, `SameSite=Lax` cookies. Session expiration set to 8 hours. Logout invalidates session in DB. | Frozen |
| **Error Handling Policy** | Generic HTTP 401 for bad credentials, missing session, expired session, or inactive account (no user enumeration). HTTP 403 for role violations. HTTP 404 without data leak for cross-customer order requests. HTTP 400 with field-specific errors for invalid input. HTTP 409 for invalid state transitions or concurrent conflicts. | Frozen |
| **Seed Data Specification** | Idempotent seed containing $\ge 3$ customers, $\ge 2$ operators, and $\ge 8$ products (including $\ge 1$ inactive product and $\ge 1$ product with `stockQuantity = 0`). Seed passwords loaded from environment variables, never committed to Git. | Frozen |
## Part B — Feature inventory and traceability   ✅ (#2)

> **Sprint 1 Active Scope & Boundary:**  
> **Only Sprint 1 is currently implemented and tested.** Features for Sprints 2 and 3 are documented solely to fulfill full-lifecycle planning and forward traceability. All active engineering contracts (Part E), database schemas, endpoints, and automated tests (Part F) are strictly restricted to Sprint 1 features (`F-01` to `F-05`) and their acceptance criteria (`AC-01` to `AC-18`).

### B.1 Feature Inventory Across Sprints
The product features are structured across three sprints to deliver an authoritative, working baseline in Sprint 1 before expanding operational capabilities in Sprint 2 and analytical depth in Sprint 3.

| Feature ID | Feature Name | Target Sprint | Primary Actor | Complexity / Priority | Associated Requirements | Description & Scope |
|---|---|---|---|---|---|---|
| **F-01** | Session Auth & Role-Based Access Control | Sprint 1 | Customer, Operator | Medium / High | FR-01, FR-02, FR-03, BR-07, BR-08, NFR-01 | Secure login via bcrypt credentials, `HttpOnly` session cookies, 8h expiration, role guard middleware (401 unauth, 403 forbidden), and server-side session revocation on logout. |
| **F-02** | Product Catalog & Availability View | Sprint 1 | Customer | Low / High | FR-04, BR-01, NFR-02 | Read-only listing of active products (`isActive=true`) with minor-unit integer pricing (THB satang) and dynamic stock availability badges ("In Stock" / "Out of Stock"). |
| **F-03** | Multi-Item Order Creation & Atomic Decrement | Sprint 1 | Customer | High / High | FR-05, FR-06, BR-01, BR-02, BR-03, BR-06, NFR-01, NFR-02 | Multi-line order submission ($1 \le \text{qty} \le 10$, no duplicates), authoritative server re-pricing (ignoring client prices), atomic stock decrement in a single DB transaction, price snapshots (`unitPriceAtOrder`), and initial status `PLACED`. |
| **F-04** | Customer Order History & Ownership Isolation | Sprint 1 | Customer | Medium / High | FR-07, FR-08, BR-05, NFR-01, NFR-02 | Chronological order history for the authenticated customer ("My Orders") with line-item totals. Strict ownership check returning HTTP 404 on cross-customer order access without metadata leakage. |
| **F-05** | Operator Order Queue & State Transition | Sprint 1 | Operator | Medium / High | FR-09, FR-10, BR-04, BR-08, NFR-01 | Filtered queue of incoming `PLACED` orders sorted oldest first. Operator acceptance transition (`PLACED -> ACCEPTED`) with `operatorId` and `acceptedAt` audit trail. Guard against invalid transitions (409 Conflict). |
| **F-06** | Operator Catalog & Stock Management | Sprint 2 | Operator | High / Medium | FR-11, BR-01, BR-08 | Operator product creation, pricing updates, inventory restocking (`stockQuantity += N`), and active/inactive visibility toggles. |
| **F-07** | Customer Cancellation & Operator Rejection | Sprint 2 | Customer, Operator | Medium / Medium | FR-12, BR-02, BR-04 | Safe cancellation for `PLACED` orders by customers, operator order rejection with obligatory reason note, and automatic atomic inventory rollback. |
| **F-08** | Extended Fulfillment Lifecycle | Sprint 2 | Operator | Medium / Medium | FR-12, BR-04, BR-08 | Multi-stage physical pickup progression: `ACCEPTED -> PREPARING -> READY -> COMPLETED` with audit timestamps and 409 transition guards. |
| **F-09** | Simulated Payment & Digital Counter Receipt | Sprint 2 | Customer, Operator | Low / Low | FR-12, BR-01 | Synthetic payment transaction generation upon order placement and downloadable/printable counter pickup receipt. |
| **F-10** | Operator Metrics & Sales Dashboard | Sprint 3 | Operator | Medium / Medium | FR-13, NFR-05 | Revenue aggregation in minor units, orders by status, queue health metrics, and top-selling merchandise breakdowns. |
| **F-11** | Advanced Search, Filter & Categorization | Sprint 3 | Customer, Operator | Low / Low | FR-13, NFR-06 | Product search by keyword/category, order filtering by status and date range, and customer lookup for operators. |
| **F-12** | System Hardening, Viewports & Performance Tuning | Sprint 3 | System / All | High / High | NFR-04, NFR-05, NFR-06 | Responsive viewports (375px to 1920px), order placement latency $< 1000\text{ ms}$, comprehensive E2E tests, and automated regression suite. |

### B.2 Acceptance Criteria Inventory (Sprint 1 Baseline)
| AC ID | Target Feature | Acceptance Criterion Statement | Verification Level |
|---|---|---|---|
| **AC-01** | F-01 | Given valid credentials, when `POST /api/auth/login` is called, server returns HTTP 200, sets `HttpOnly` session cookie, and returns user id, email, and role. | Integration / API |
| **AC-02** | F-01 | Given invalid credentials, when `POST /api/auth/login` is called, server returns generic HTTP 401 without user enumeration. | Integration / API |
| **AC-03** | F-01 | Given unauthenticated request or expired session, protected endpoints return HTTP 401. | Integration / API |
| **AC-04** | F-01 | Given authenticated session, when `POST /api/auth/logout` is called, server invalidates session in DB, clears cookie, and returns HTTP 200. | Integration / API |
| **AC-05** | F-02 | Given active catalog, when `GET /api/products` is called, server returns HTTP 200 with active products, minor-unit prices (`priceMinor`), and stock availability badges. Inactive items are excluded. | Integration / API |
| **AC-06** | F-03 | Given valid multi-item order with sufficient stock, when `POST /api/orders` is called, server atomically creates order (`PLACED`), snapshots prices, decrements stock, and returns HTTP 201. | Integration / API + DB |
| **AC-07** | F-03 | Given empty items array (`items: []`), when `POST /api/orders` is called, server rejects with HTTP 400 and creates no records. | Integration / API |
| **AC-08** | F-03 | Given order line exceeding available `stockQuantity`, when `POST /api/orders` is called, server aborts transaction with HTTP 400 and leaves stock unchanged. | Integration / API + DB |
| **AC-09** | F-03 | Given order containing inactive item (`isActive = false`), when `POST /api/orders` is called, server rejects with HTTP 400. | Integration / API |
| **AC-10** | F-03 | Given placed order, when server process is stopped and restarted, all order lines, totals, and decremented stock quantities remain intact in PostgreSQL. | Integration / Persistence |
| **AC-11** | F-04 | Given authenticated customer, when `GET /api/orders` is called, server returns HTTP 200 with customer's own orders sorted newest first with complete line totals. | Integration / API |
| **AC-12** | F-04 | Given customer A, when `GET /api/orders/:id` is called for customer B's order, server returns HTTP 404 without leaking metadata. | Integration / API |
| **AC-13** | F-01, F-05 | Given `CUSTOMER` role, when calling operator endpoints (`GET /api/operator/orders` or `PATCH /api/operator/orders/:id/accept`), server rejects with HTTP 403 Forbidden. | Integration / API |
| **AC-14** | F-05 | Given authenticated operator, when `GET /api/operator/orders` is called, server returns HTTP 200 with `PLACED` orders sorted chronologically (oldest first). | Integration / API |
| **AC-15** | F-05 | Given authenticated operator and `PLACED` order, when `PATCH /api/operator/orders/:id/accept` is called, server transitions status to `ACCEPTED`, records `operatorId` and `acceptedAt`, and returns HTTP 200. | Integration / API + DB |
| **AC-16** | F-05 | Given order already in `ACCEPTED` status, calling `PATCH /api/operator/orders/:id/accept` returns HTTP 409 Conflict. | Integration / API |
| **AC-17** | F-01, F-03 | Given `OPERATOR` role, attempting customer order creation (`POST /api/orders`) returns HTTP 403 Forbidden. | Integration / API |
| **AC-18** | F-01, F-02 | Running database seed script consecutively executes idempotently, populating required demo accounts ($\ge 3$ customers, $\ge 2$ operators) and products ($\ge 8$ products) without constraint errors. | Integration / Seed Script |

### B.3 Traceability Matrix (FR / BR / NFR $\rightarrow$ Features $\rightarrow$ Sprints $\rightarrow$ ACs)

| Req / Rule / NFR | Description | Feature | Sprint | Enforcing AC(s) | Verification Suite |
|---|---|---|---|---|---|
| **FR-01** | User Authentication | F-01 | S1 | AC-01, AC-02, AC-18 | `auth.api.test.ts` |
| **FR-02** | Session Logout | F-01 | S1 | AC-04 | `auth.api.test.ts` |
| **FR-03** | Role-Based Route Protection | F-01 | S1 | AC-03, AC-13, AC-17 | `rbac.api.test.ts` |
| **FR-04** | Browse Active Catalog & Stock | F-02 | S1 | AC-05, AC-18 | `catalog.api.test.ts` |
| **FR-05** | Multi-Line Order Placement | F-03 | S1 | AC-06, AC-07, AC-08, AC-09 | `orders.api.test.ts` |
| **FR-06** | Price Snapshot (`unitPriceAtOrder`) | F-03 | S1 | AC-06, AC-10 | `orders.api.test.ts` |
| **FR-07** | Customer Order History & Details | F-04 | S1 | AC-11 | `orders-customer.api.test.ts` |
| **FR-08** | Customer Data Isolation | F-04 | S1 | AC-12 | `orders-isolation.api.test.ts` |
| **FR-09** | Operator Incoming Queue | F-05 | S1 | AC-14 | `operator-orders.api.test.ts` |
| **FR-10** | Operator Order Acceptance | F-05 | S1 | AC-15, AC-16 | `operator-orders.api.test.ts` |
| **FR-11** | Operator Catalog Management | F-06 | S2 | — | Sprint 2 Contract Tests |
| **FR-12** | Extended Fulfillment & Cancellation | F-07, F-08, F-09 | S2 | — | Sprint 2 Contract Tests |
| **FR-13** | Reporting Dashboard & Analytics | F-10, F-11 | S3 | — | Sprint 3 Benchmark Tests |
| **BR-01** | Monetary Representation (minor units, THB satang) | F-02, F-03 | S1 | AC-05, AC-06 | Schema integer type + `orders.api.test.ts` |
| **BR-02** | Atomic Placement & Stock Decrement | F-03 | S1 | AC-06, AC-08, AC-10 | Prisma `$transaction` concurrency tests |
| **BR-03** | Authoritative Server Pricing | F-03 | S1 | AC-06 | API tests sending forged client prices |
| **BR-04** | Order Lifecycle (`PLACED -> ACCEPTED`, 409 guard) | F-05 | S1 | AC-15, AC-16 | Order state guard in `operator-orders.api.test.ts` |
| **BR-05** | Customer Order Ownership Isolation | F-04 | S1 | AC-12 | Scoped query in `orders-isolation.api.test.ts` |
| **BR-06** | Line Constraints ($1 \le \text{qty} \le 10$, no duplicates) | F-03 | S1 | AC-07, AC-08 | Zod schema validation tests |
| **BR-07** | Secure Credential Storage (bcrypt salt $\ge 10$) | F-01 | S1 | AC-01, AC-18 | DB seed & auth service tests |
| **BR-08** | Operator Scope Restrictions | F-01, F-05 | S1 | AC-13, AC-17 | Role middleware in `rbac.api.test.ts` |
| **NFR-01** | Auth & RBAC Route Enforcement (401/403/404) | F-01, F-04, F-05 | S1 | AC-01, AC-02, AC-03, AC-12, AC-13, AC-17 | Route security test suite |
| **NFR-02** | Relational Data Persistence across Restarts | F-02, F-03, F-04 | S1 | AC-10 | DB restart verification script |
| **NFR-03** | Seed Idempotence & Determinism | F-01, F-02 | S1 | AC-18 | Double-run seed test script |
| **NFR-04** | Fresh Clone Reproducibility ($< 5\text{ min}$) | F-12 | S1 | — | Clean-room clone verification |
| **NFR-05** | Order Placement Latency ($< 1000\text{ ms}$) | F-03, F-12 | S1/S3 | AC-06 | Latency benchmark test |
| **NFR-06** | Responsive Viewports (375px to 1920px) | F-12 | S3 | — | Playwright responsive viewport assertions |

### B.4 Coverage and Traceability Health Analysis
- **Requirements Coverage:** 13/13 FRs (100%), 8/8 BRs (100%), 6/6 NFRs (100%).
- **Forward Orphan Check:** 0 unmapped requirements.
- **Backward Orphan Check:** 0 ungrounded features or acceptance criteria.
- **Sprint 1 Containment:** 10/13 FRs, 8/8 BRs, 4/6 NFRs, and 18/18 ACs implemented in Sprint 1 baseline.

## Part C — System-Level SDS   ✅ (#3)

### C.1 System Architecture & Technology Stack
The UniMerch Campus Store is engineered as a modular **three-tier client-server architecture**:
1. **Presentation Layer (Web Client):** React 18 SPA bundled with Vite and written in TypeScript. Responsive UI styled using Bootstrap 5 with clean green-themed design tokens (`#1b5e20`, `#2e7d32`).
2. **Application / API Layer (Backend Server):** Node.js 20 runtime executing an Express modular server in TypeScript. Enforces all business rules, input validations (Zod schemas), and security middleware (`requireAuth`, `requireRole`).
3. **Data Layer (Relational Database):** PostgreSQL 16 database accessed through Prisma ORM 5. Guarantees relational integrity, foreign key cascades, and ACID transactions (`prisma.$transaction`) for order placement and stock decrements.

**Business Rule Enforcement:** All business rules are strictly enforced on the server. Client-side validation exists only for user feedback; client-submitted prices or totals are discarded.

![System Architecture Diagram](evidence/issue-03_architecture-diagram.png)

### C.2 Data Model & Persistence Architecture
The data model consists of five core entities in Sprint 1: `User`, `Session`, `Product`, `Order`, and `OrderItem`.

![Entity-Relationship Schema Diagram](evidence/issue-03_er-diagram.png)

#### Entity Schema & Constraints:
- **`User`:** `id` (PK Int), `email` (Unique String, normalized), `passwordHash` (String, salted bcrypt hash), `name` (String), `role` (`CUSTOMER` | `OPERATOR`), `isActive` (Boolean, default true), `createdAt`, `updatedAt`.
- **`Session`:** `id` (PK String, UUIDv4), `userId` (FK -> `User.id`, `onDelete: Cascade`), `tokenHash` (Unique String), `expiresAt` (DateTime, 8 hours lifetime), `createdAt`.
- **`Product`:** `id` (PK Int), `name` (String), `description` (String?), `priceMinor` (Int, CHECK `>= 0` in THB satang), `stockQuantity` (Int, CHECK `>= 0`), `isActive` (Boolean, default true), `createdAt`, `updatedAt`.
- **`Order`:** `id` (PK Int), `customerId` (FK -> `User.id`), `status` (`PLACED` | `ACCEPTED`), `totalMinor` (Int, CHECK `>= 0`), `createdAt` (DateTime), `acceptedAt` (DateTime?), `acceptedByOperatorId` (FK -> `User.id`, Nullable).
- **`OrderItem`:** `id` (PK Int), `orderId` (FK -> `Order.id`, `onDelete: Cascade`), `productId` (FK -> `Product.id`), `quantity` (Int, CHECK `> 0` and `<= 10`), `unitPriceAtOrder` (Int, CHECK `>= 0` — immutable price snapshot).

#### Migrations & Idempotent Seed:
- Database schema migrations are versioned via Prisma Migrate (`server/prisma/migrations/`).
- Idempotent seed script (`server/prisma/seed.ts`) uses `upsert` ensuring that executing `npm run seed` repeatedly causes zero duplicates and zero constraint errors.
- Demo dataset: $\ge 3$ customers, $\ge 2$ operators, $\ge 8$ products (including out-of-stock and inactive items).

### C.3 UI Conventions & Role Navigation
The web client features role-aware routing:
- **Public:** `/login` (clean form, non-revealing error message, disabled state during submission).
- **Customer:** `/catalog` (merchandise cards, price badges, stock badge, quantity picker), `/cart` (review lines, server-estimated total, checkout), `/my-orders` (personal order history), `/orders/:id` (order breakdown, status, snapshot prices).
- **Operator:** `/operator/orders` (chronological queue of `PLACED` orders, oldest first, with one-click Accept button and 409 transition guard).

**UI States Handled:** Every interactive component gracefully renders Idle, Loading (spinners/disabled inputs), Empty (clear contextual guidance), and Error (user-friendly alerts without backend stack traces).

### C.4 API Conventions & Safe Error Envelope
All endpoints communicate via JSON over HTTPS. Authenticated requests pass credentials via an `HttpOnly`, `SameSite=Lax` cookie named `session_token`.

#### Standard Status Codes:
- `200 OK` / `201 Created`: Successful request execution.
- `400 Bad Request`: Validation failure (syntax error, non-integer quantity, duplicate line items, quantity out of range $[1, 10]$).
- `401 Unauthorized`: Missing, invalid, or expired session token; invalid login credentials (generic message to avoid user enumeration).
- `403 Forbidden`: Authenticated user lacks required role (e.g. Customer calling operator endpoints).
- `404 Not Found`: Target record does not exist OR belongs to another customer (prevents ID enumeration/data leakage).
- `409 Conflict`: Business rule violation (out of stock, insufficient inventory, invalid state transition).
- `500 Internal Server Error`: Safe generic message returned; details logged only to server stderr.

### C.5 Role and Permission Matrix
| Protected Operation | Endpoint | Anonymous | Customer | Operator | Scope / Ownership Constraint |
|---|---|:---:|:---:|:---:|---|
| **Login** | `POST /api/auth/login` | Allowed | Allowed | Allowed | N/A |
| **Logout** | `POST /api/auth/logout` | 401 | Allowed | Allowed | Invalidates acting session |
| **Get Current User** | `GET /api/auth/me` | 401 | Allowed | Allowed | Reads acting user profile |
| **Browse Catalog** | `GET /api/products` | 401 | Allowed | Allowed | Entire shop catalog |
| **Place Order** | `POST /api/orders` | 401 | **Allowed** | 403 | Bound to acting `session.userId` |
| **List My Orders** | `GET /api/orders` | 401 | **Allowed** | 403 | Strict filter: `customerId == userId` |
| **View Order Detail** | `GET /api/orders/:id` | 401 | **Conditional** | **Allowed** | Customer: own order only (else 404); Operator: all orders |
| **List Incoming Orders** | `GET /api/operator/orders` | 401 | 403 | **Allowed** | All `PLACED` orders |
| **Accept Order** | `POST /api/operator/orders/:id/accept` | 401 | 403 | **Allowed** | Only `PLACED` orders (409 if already accepted) |
| *Manage Catalog (S2)* | `POST/PUT /api/operator/products` | 401 | 403 | Allowed | Catalog items within store |
| *Cancel Order (S2)* | `POST /api/orders/:id/cancel` | 401 | Conditional | 403 | Customer: own order while `PLACED` |
| *Reject Order (S2)* | `POST /api/operator/orders/:id/reject`| 401 | 403 | Allowed | Operator with rejection note |
| *Simulated Payment (S2)* | `POST /api/orders/:id/pay` | 401 | Conditional | 403 | Customer: own order while `ACCEPTED` |
| *Sales Analytics (S3)* | `GET /api/operator/analytics` | 401 | 403 | Allowed | Aggregated shop statistics |

### C.6 Authentication & Session Lifecycle
- **Password Hashing:** Passwords hashed via salted bcrypt (cost factor 10).
- **Session Tokens:** 32-byte cryptographically secure random tokens (`crypto.randomBytes(32)`).
- **Session Table:** Stored as SHA-256 token hashes in the `Session` table with an 8-hour expiration.
- **Cookie Security:** Delivered in `HttpOnly`, `SameSite=Lax`, `Path=/` cookies. Inaccessible to client JavaScript (XSS resilient).
- **Session Revocation:** On logout, the session row is deleted from the database and the cookie is cleared with `Max-Age=0`.

### C.7 Configuration & Deployment Architecture
- **Environment Variables:** `PORT`, `DATABASE_URL`, `SESSION_SECRET`, `CORS_ORIGIN`, `NODE_ENV`. Documented with clean placeholders in `.env.example`. No secrets committed.
- **Docker Suitability:** Multi-stage Dockerfile builds compiled JavaScript/CSS and executes lightweight production Node runtime.
- **Planned GCP Deployment (Lab 5 Readiness):** Backend container hosted on Google Cloud Run; relational database hosted on managed Google Cloud SQL (PostgreSQL); secrets managed securely via Google Secret Manager.
## Part D — Three-sprint plan   ✅ (#4)

### D.1 Three-Sprint Allocation Table

| Sprint | Checkpoint Date | Sprint Goal | Scope (Feature IDs) | Dependencies | Target Outcome / Deliverables |
|---|---|---|---|---|---|
| **Sprint 1** | **8 Nov 2026** | **Baseline Working Slice & Contracts:** Establish foundational security, relational data persistence, authoritative catalog, atomic multi-line order placement, and single-step operator acceptance. | • **F-01:** Session Auth & RBAC (`CUSTOMER`, `OPERATOR`)<br>• **F-02:** Authoritative Catalog & Live Stock<br>• **F-03:** Multi-Item Order Creation, Server Pricing & Atomic Decrement<br>• **F-04:** Customer Order History & Ownership Isolation<br>• **F-05:** Operator Order Queue & State Transition (`PLACED -> ACCEPTED`) | Base scaffold, PostgreSQL DB, idempotent seed script | **Working increment on `main`:**<br>- Verified session auth (bcrypt, HttpOnly cookie)<br>- Authoritative catalog with satang minor units<br>- Atomic order creation with transactional rollback on stockout<br>- Customer data isolation (HTTP 404 cross-access)<br>- Operator acceptance queue & transition<br>- Automated integration test suite (STS)<br>- Deliverable 1 PDF / ODT |
| **Sprint 2** | **29 Nov 2026** | **Core Operational Expansion:** Equip store operators with catalog/stock controls, implement cancellation/rejection with automatic inventory rollback, and support the multi-stage counter pickup lifecycle. | • **F-06:** Operator Catalog & Stock Management<br>• **F-07:** Customer Cancellation & Operator Rejection with Stock Rollback<br>• **F-08:** Extended Fulfillment Lifecycle (`ACCEPTED -> PREPARING -> READY -> COMPLETED`)<br>• **F-09:** Simulated Payment & Digital Counter Receipt | Sprint 1 baseline (`F-01`..`F-05`), transactional persistence | **Sprint 2 increment:**<br>- Operator back-office catalog CRUD<br>- Multi-stage state machine transitions with 409 conflict guards<br>- Automated inventory restitution on cancel/reject<br>- Simulated payment records & digital pickup receipts<br>- Deliverable 2 report |
| **Sprint 3** | **Progress: 29 Nov 2026<br>Complete: 13 Dec 2026** | **Operational Analytics & System Hardening:** Deliver store analytics dashboards, full-text product search, order filtering, responsive UI verification, and latency benchmarks. | • **F-10:** Operator Metrics & Sales Dashboard<br>• **F-11:** Advanced Search, Filtering & Categorization<br>• **F-12:** System Hardening, Responsive Viewports & Performance Tuning | Sprints 1 & 2 data models, Playwright responsive viewport harness | **Final Release package:**<br>- Sales & order metrics dashboard<br>- Full-text search and multi-criteria order filter<br>- Responsive layout verified across mobile (375px), tablet (768px), and desktop (1920px)<br>- Order creation latency $< 1000\text{ ms}$<br>- Full regression suite passing<br>- Final Delivery package |

### D.2 Feature Allocation & Inter-Feature Dependencies
- **Strict Sprint Allocation:** Every feature from `docs/features.md` appears in exactly one sprint:
  - Sprint 1 (5 features): `F-01`, `F-02`, `F-03`, `F-04`, `F-05`
  - Sprint 2 (4 features): `F-06`, `F-07`, `F-08`, `F-09`
  - Sprint 3 (3 features): `F-10`, `F-11`, `F-12`
- **Dependency Flow:**
  - `F-01` provides foundational authentication and role enforcement for all protected routes.
  - `F-02` feeds catalog stock and authoritative pricing into `F-03`.
  - `F-03` generates orders consumed by `F-04` (customer history) and `F-05` (operator queue).
  - Sprint 2 features (`F-06`..`F-09`) and Sprint 3 features (`F-10`..`F-12`) extend these core transactional tables without requiring destructive schema rewrites.

### D.3 Feasibility Justification for Sprint 1
The scope chosen for Sprint 1 is **compact, cohesive, and guaranteed to be feasible within the allocated timeframe**:
1. **Vertical Slice Focus:** Rather than building broad, shallow features across all actors, Sprint 1 implements a single complete vertical journey through the full stack (React UI $\rightarrow$ Express API $\rightarrow$ PostgreSQL database) from customer login to order acceptance.
2. **Explicit Scope Exclusions (Zero External Bottlenecks):** By formally excluding live payment gateways (Stripe/PayPal), external courier tracking APIs, and external email/SMS providers, the team eliminates third-party dependencies, webhook latency, and asynchronous failure modes.
3. **Pre-Built Architectural Foundation:** Utilizing Express/Node, React/Vite, and Prisma ORM against a local PostgreSQL database enables rapid local iteration, automatic end-to-end TypeScript type safety, and automated test execution with Supertest and Vitest.
4. **Deterministic Seed Data:** Pre-configured, bcrypt-hashed demo accounts ($\ge 3$ customers, $\ge 2$ operators) and catalog products allow clean-room automated test execution without relying on complex user registration workflows.
5. **Balanced Duo Workload:** The 15 granular issues are evenly split between Student Cl (8 issues) and Student Ba (7 issues), allowing parallel development paths (e.g., Ba drafting contracts and frontend tests while Cl builds authentication) without development bottlenecks.

## Part E — Sprint 1 engineering contracts   ✅ (#5)

### E.1 Sprint 1 Feature Contracts Summary

#### Feature F-01: Session Authentication & Role-Based Access Control
- **Behavior & Workflow:** Authenticates users via email and bcrypt-hashed passwords. Generates cryptographically secure 32-byte session token stored in PostgreSQL `Session` table (8-hour expiry) and transmitted via `HttpOnly`, `SameSite=Lax` cookies. Identity is established strictly from session lookup, never from request payload fields.
- **Endpoints:**
  - `POST /api/auth/login` $\rightarrow$ 200 (sets cookie, returns `{ id, email, role }`), 400 (malformed), 401 (invalid credentials).
  - `GET /api/auth/me` $\rightarrow$ 200 (returns authenticated user profile), 401 (unauthenticated).
  - `POST /api/auth/logout` $\rightarrow$ 200 (invalidates session in DB, clears cookie).
- **Data & Constraints:** `User` table (unique email, `passwordHash`, `role: CUSTOMER | OPERATOR`, `isActive`), `Session` table (unique token, `userId` FK cascade, `expiresAt`).

#### Feature F-02: Authoritative Product Catalog & Live Stock Availability
- **Behavior & Workflow:** Read-only product listing. Filters strictly for `isActive = true` products. Prices are stored and transmitted strictly in minor units (integer satang, e.g. 25000 = 250.00 THB) to eliminate float rounding errors. Real-time availability badges ("In Stock" vs "Out of Stock").
- **Endpoints:**
  - `GET /api/products` $\rightarrow$ 200 (returns active product list with integer `priceMinor` and `stockQuantity`).
- **Data & Constraints:** `Product` table (`name`, `description`, `priceMinor > 0`, `stockQuantity >= 0`, `isActive`).

#### Feature F-03: Multi-Item Order Creation, Server Pricing & Atomic Decrement
- **Behavior & Workflow:** Authenticated customer submits 1 to $N$ order lines. Re-queries product prices from PostgreSQL inside an atomic ACID transaction (`prisma.$transaction`). Rejects empty arrays, non-integer quantities, quantities $> 10$, duplicate product lines, inactive items, and stockouts with HTTP 400. Captures price snapshot `OrderItem.unitPriceAtOrder`. Decrements stock atomically and initializes order with status `PLACED`.
- **Endpoints:**
  - `POST /api/orders` $\rightarrow$ 201 (order created, total calculated, stock decremented), 400 (validation/stockout error, full rollback), 401 (unauthenticated), 403 (operator forbidden from placing orders).
- **Data & Constraints:** `Order` (`customerId` FK, `status: PLACED | ACCEPTED`, `totalMinor`), `OrderItem` (`orderId` FK, `productId` FK, `quantity`, `unitPriceAtOrder`, unique composite `[orderId, productId]`).

#### Feature F-04: Customer Order History & Ownership Isolation
- **Behavior & Workflow:** Customer reviews own historical orders sorted newest first (`createdAt DESC`). Scoped lookups enforce `customerId = session.userId`. Any query for another customer's order ID returns HTTP 404 without leaking metadata.
- **Endpoints:**
  - `GET /api/orders` $\rightarrow$ 200 (list of customer's own orders).
  - `GET /api/orders/:id` $\rightarrow$ 200 (order details and items), 404 (not found or owned by another user).

#### Feature F-05: Operator Order Queue & Single-Step Acceptance
- **Behavior & Workflow:** Store operator views incoming queue of orders in status `PLACED`, ordered chronologically (oldest first). Operator clicks accept, transitioning status from `PLACED` to `ACCEPTED`, recording `acceptedAt` timestamp and `acceptedByOperatorId`. Guards against duplicate acceptance with HTTP 409 Conflict.
- **Endpoints:**
  - `GET /api/operator/orders` $\rightarrow$ 200 (incoming `PLACED` queue), 403 (customer forbidden).
  - `PATCH /api/operator/orders/:id/accept` $\rightarrow$ 200 (status changed to `ACCEPTED`), 403 (customer forbidden), 404 (not found), 409 (already accepted or invalid state).

---

### E.2 Software Test Specification (STS) — Master Matrix

| TEST ID | Linked AC | Level | Precondition / Input Data | Action Executed | Expected Result & Assertions | Planned Test File |
|---|---|---|---|---|---|---|
| **TEST-01** | AC-01 | API | Seeded customer exists in DB | `POST /api/auth/login` valid email/pwd | HTTP 200, `Set-Cookie` contains `sid`, body returns `{ id, email, role }` without hash | `server/tests/sprint-1/auth.api.test.ts` |
| **TEST-02** | AC-02 | API | Unknown email or wrong password | `POST /api/auth/login` bad credentials | HTTP 401 Unauthorized, generic error message, no cookie set | `server/tests/sprint-1/auth.api.test.ts` |
| **TEST-03** | AC-03 | API | Missing or expired cookie | `GET /api/auth/me` and `GET /api/orders` | HTTP 401 Unauthorized, empty/safe error body, no protected data exposed | `server/tests/sprint-1/auth.api.test.ts` |
| **TEST-04** | AC-04 | API | Active authenticated session | `POST /api/auth/logout` then `GET /me` | Logout returns HTTP 200; subsequent `/me` returns HTTP 401; session deleted in DB | `server/tests/sprint-1/auth.api.test.ts` |
| **TEST-05** | AC-05 | API | Catalog with active & inactive items | `GET /api/products` | HTTP 200, returns active items with integer `priceMinor` and stock; inactive omitted | `server/tests/sprint-1/catalog.api.test.ts` |
| **TEST-06** | AC-05 | UI | Products returned by mock API | Render `<Catalog />` | Displays product cards, formatted THB prices, "In Stock" badge, disabled if stock = 0 | `client/tests/sprint-1/Catalog.test.tsx` |
| **TEST-07** | AC-06 | API | Customer session, valid items with stock | `POST /api/orders` valid payload | HTTP 201 Created, status `PLACED`, server-calculated total, stock decremented, price snapshot saved | `server/tests/sprint-1/orders-create.api.test.ts` |
| **TEST-08** | AC-07 | API | Payload with forged `price: 1` | `POST /api/orders` tampered price | HTTP 201 Created, total matches DB price calculation, forged client price ignored | `server/tests/sprint-1/orders-create.api.test.ts` |
| **TEST-09** | AC-08 | Unit | Pure pricing/validation service | Call with qty = 0, -1, 1.5, 11, or duplicates | Domain validation throws explicit validation exception for each boundary | `server/tests/sprint-1/orders-pricing.unit.test.ts` |
| **TEST-10** | AC-08 | API | Empty `items: []` or `quantity: 0` | `POST /api/orders` invalid quantity | HTTP 400 Bad Request with field errors; zero records persisted in DB | `server/tests/sprint-1/orders-create.api.test.ts` |
| **TEST-11** | AC-09 | API | Product has stock = 1, request qty = 2 | `POST /api/orders` exceeding stock | HTTP 400 Bad Request, transaction rolls back, stock remains exactly 1 | `server/tests/sprint-1/orders-create.api.test.ts` |
| **TEST-12** | AC-10 | API | Order exists; change product price in DB | `GET /api/orders/:id` for past order | HTTP 200, `unitPriceAtOrder` retains original price; historical total unchanged | `server/tests/sprint-1/orders-create.api.test.ts` |
| **TEST-13** | AC-11 | API | Customer A has 2 orders; Customer B has 1 | `GET /api/orders` as Customer A | HTTP 200, returns exactly Customer A's 2 orders sorted newest first | `server/tests/sprint-1/orders-access.api.test.ts` |
| **TEST-14** | AC-11 | UI | Customer orders mock data | Render `<MyOrders />` | Displays list of orders with IDs, date, `PLACED` badge, formatted total, link to details | `client/tests/sprint-1/MyOrders.test.tsx` |
| **TEST-15** | AC-12 | API | Order B belongs to B; auth as Customer A | `GET /api/orders/:idB` as Customer A | HTTP 404 Not Found; no order metadata or existence confirmation leaked | `server/tests/sprint-1/orders-access.api.test.ts` |
| **TEST-16** | AC-13 | API | Authenticated user with role `CUSTOMER` | `GET /api/operator/orders` | HTTP 403 Forbidden with `{ "error": "Operator access required" }` | `server/tests/sprint-1/operator-orders.api.test.ts` |
| **TEST-17** | AC-14 | API | 3 orders placed in DB | `GET /api/operator/orders` as Operator | HTTP 200, returns incoming `PLACED` orders ordered chronologically (oldest first) | `server/tests/sprint-1/operator-orders.api.test.ts` |
| **TEST-18** | AC-14 | UI | Incoming orders mock data | Render `<OperatorOrders />` | Displays queue table, customer email, order items, and enabled "Accept" button | `client/tests/sprint-1/OperatorOrders.test.tsx` |
| **TEST-19** | AC-15 | API | Order in status `PLACED`, operator auth | `PATCH /api/operator/orders/:id/accept` | HTTP 200, status becomes `ACCEPTED`, `acceptedAt` set, `acceptedByOperatorId` set | `server/tests/sprint-1/operator-orders.api.test.ts` |
| **TEST-20** | AC-16 | API | Order already in status `ACCEPTED` | `PATCH /api/operator/orders/:id/accept` second time | HTTP 409 Conflict; database state remains unchanged | `server/tests/sprint-1/operator-orders.api.test.ts` |
| **TEST-21** | AC-17 | Persistence | Seed script executed twice consecutively | Execute `npm run seed && npm run seed` | Both runs succeed with exit code 0; record counts identical; zero duplicate key errors | `server/tests/sprint-1/persistence.api.test.ts` |
| **TEST-22** | AC-18 | UI | Login view with mock auth context | Submit Customer vs Operator credentials | Customer login navigates to `/catalog`; Operator login navigates to `/operator/orders` | `client/tests/sprint-1/Login.test.tsx` |
| **TEST-23** | AC-18 | UI | Authenticated user clicks Logout | Click logout button | Calls logout API, clears auth context, redirects to `/login` | `client/tests/sprint-1/Login.test.tsx` |
| **TEST-24** | AC-19 | E2E | Browser instance, seeded DB | Complete Customer journey: Login $\rightarrow$ Catalog $\rightarrow$ Add to Cart $\rightarrow$ Submit $\rightarrow$ View Order | Order created in DB, visible on customer screen, catalog stock decremented | `e2e/sprint-1/customer-journey.spec.ts` |
| **TEST-25** | AC-19 | E2E | Order from TEST-24 | Operator journey: Login $\rightarrow$ Incoming Queue $\rightarrow$ Click Accept $\rightarrow$ Confirm `ACCEPTED` | Order accepted in DB; disappears from `PLACED` queue; customer reloads and sees `ACCEPTED` | `e2e/sprint-1/operator-journey.spec.ts` |
| **TEST-26** | AC-20 | E2E | Customer browser session | Customer navigates directly to `/operator/orders`; or attempts out-of-stock order | Direct operator navigation blocked with redirect; out-of-stock order displays visible rejection toast | `e2e/sprint-1/access-restrictions.spec.ts` |

---

### E.3 Product Definition of Done (DoD)
1. **Contract Adherence:** Implemented behavior matches `docs/sprints/sprint-1/F-01`..`F-05` without undocumented divergence.
2. **STS Test Execution:** All mapped tests (`TEST-01` to `TEST-26`) implemented, executed, and passing with exact command and counts recorded.
3. **TDD History:** Failing test commit precedes implementation commit on TDD issues (`#7`, `#10`, `#12`).
4. **Security & Secrets:** Zero secrets in Git or fixtures; passwords hashed with bcrypt; calculations in integer minor units.
5. **Living PDF Draft & Evidence:** `PDF_DRAFT.md` updated in the same PR, evidence saved in `evidence/`, `.odt` regenerated.
6. **Peer Review:** Branch reviewed and approved on GitHub with substantive specific comments before merging to `sprint1-staging`.

## Part F — Working Sprint 1 and verification
### F.1 Setup summary   ✅ (#6, #15)
- **Node.js Environment:** Node.js v20.20.2, npm v10.8.2.
- **Database Engine:** PostgreSQL 16 on `localhost:5432` (`DATABASE_URL="postgresql://postgres:postgres@localhost:5432/unimerch?schema=public"`).
- **ORM & Migrations:** Prisma ORM 5.x with declarative schema (`server/prisma/schema.prisma`). Initial migration generated and applied via `npx prisma migrate resolve --applied 20261122000000_init` / `prisma migrate deploy`.
- **Database Seeding:** Executed via `npm run seed` (`tsx prisma/seed.ts`), idempotently upserting 5 users (3 Customers, 2 Operators with bcrypt hashes) and 8 products (including inactive and out-of-stock items).
- **Evidence Files:**
  - `docs/deliverable-1/evidence/issue-06_seed-output.txt`
  - `docs/deliverable-1/evidence/issue-06_persistence-test.txt`
  - `docs/deliverable-1/evidence/issue-06_seed_terminal.png`
  - `docs/deliverable-1/evidence/issue-06_persistence_test.png`

### F.2 Program demonstrations   (release commit: <RELEASE_COMMIT>)
| # | Scenario | Feature/AC | Role | Start conditions | Steps | Expected | Actual | Evidence file | Status | Issue |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Login | AC-01, AC-18 | Customer | Seeded DB | `POST /api/auth/login` and React Login UI form submission | HTTP 200, sets `sid` cookie, renders role-appropriate navigation (Customer sees Catalog & My Orders; Operator sees Incoming Orders) | Verified via Vitest suite (6 tests pass) & Supertest suite | `docs/deliverable-1/evidence/issue-08_AC-18_login-ui-tests.txt` | ✅ | #7, #8 |
| S2 | Normal order journey + persisted retrieval | AC-05, AC-06, AC-11 | Customer | | | | | | ⬜ | #10, #11 |
| S3 | DB proof | AC-06, AC-10 | — | | | | | | ⬜ | #10 |
| S4 | Rule rejection | AC-08, AC-09 | Customer | | | | | | ⬜ | #10 |
| S5 | Operator accepts order | AC-14, AC-15 | Operator | | | | | | ⬜ | #12 |
| S6 | Invalid transition (409) | AC-16 | Operator | | | | | | ⬜ | #12 |
| S7 | Forbidden role operation | AC-13 | Customer | Authenticated Customer session | Access operator-only route | HTTP 403 Forbidden with permission error | Verified via Supertest suite | `docs/deliverable-1/evidence/issue-07_auth_test.png` | ✅ | #7, #12, #13 |
| S8 | Ownership restriction | AC-12 | Customer | | | | | | ⬜ | #13 |
| S9 | Unauthenticated access | AC-03 | — | No session cookie | `GET /api/auth/me` without cookie | HTTP 401 Unauthorized with safe error | Verified via Supertest suite | `docs/deliverable-1/evidence/issue-07_auth_test.png` | ✅ | #7, #13 |
| S10 | Logout | AC-04 | Customer | Active session | `POST /api/auth/logout` followed by `/me` | HTTP 200, clears `sid`, subsequent `/me` gives 401 | Verified via Supertest suite | `docs/deliverable-1/evidence/issue-07_auth_test.png` | ✅ | #7 |
### F.3 Build and automated test results
- Commands and tested commit: `npm test` (Vitest v2.1.9 on client and server)
- Passed / failed / skipped counts: 23 passed, 0 failed, 1 skipped (server: 17 passed, client: 6 passed)
| AC | Planned TEST | Actual test file / name | Level | Result | Issue |
|---|---|---|---|---|---|
| **AC-01** | TEST-01 | `server/tests/sprint-1/auth.api.test.ts` (Valid login: customer & operator, HttpOnly sid cookie, safe payload) | API | ✅ PASS (2/2) | #7 |
| **AC-02** | TEST-02 | `server/tests/sprint-1/auth.api.test.ts` (Invalid credentials: wrong pwd, unknown email, missing input) | API | ✅ PASS (3/3) | #7 |
| **AC-03** | TEST-03 | `server/tests/sprint-1/auth.api.test.ts` (Session identity & route protection: missing cookie, invalid token, profile) | API | ✅ PASS (3/3) | #7 |
| **AC-04** | TEST-04 | `server/tests/sprint-1/auth.api.test.ts` (Logout & invalidation: cookie clear, DB session deletion, subsequent 401) | API | ✅ PASS (1/1) | #7 |
| **AC-13** | TEST-16 | `server/tests/sprint-1/auth.api.test.ts` (RBAC protection: unauth 401, customer forbidden 403, operator allowed 200) | API | ✅ PASS (3/3) | #7 |
| **AC-17** | TEST-21 | `server/tests/sprint-1/persistence.api.test.ts` (idempotent seed, relational persistence, schema validation) | Persistence | ✅ PASS (4/4) | #6 |
| **AC-18** | TEST-22, TEST-23 | `client/tests/sprint-1/Login.test.tsx` (Login form, busy state, generic error, role-based nav, logout) | UI | ✅ PASS (6/6) | #8 |
- Excerpt 1 (domain rule): ⬜ (#10)
- Excerpt 2 (ownership restriction): ⬜ (#13)
- TDD evidence (failing → passing, commit hashes):
  - **Issue #7 (Auth & Session RBAC):** Failing test commit `cdc98d8` (`test: issue #7 - add failing API integration tests...`) → Passing implementation commit `d44cba7` (`feat: issue #7 - implement session authentication...`) | ✅ Proven
  - **Issue #10 (Order creation & pricing engine):** ⬜ (#10)
  - **Issue #12 (Operator accept workflow):** ⬜ (#12)
### F.4 Engineering workflow and history
| Issue | Feature/AC | Branch | Author | Reviewer | Review comment | Merged to staging | Merged to main |
|---|---|---|---|---|---|---|---|
| #0 | Repository setup, PR template, basecode comment cleanup, PDF draft skeleton | `issue/00-initial-setup` | Cl | Ba | Checked obsolete comments removal and PR template/draft setup | PR #2 (merged) | via release PR |
| #1 | FR-01…FR-13, BR-01…BR-08, NFR-01…NFR-06 (SRS specification) | `issue/01-srs` | Cl | Ba | Reviewed SRS Part A, validated domain decisions and problem statement | PR #4 (merged) | via release PR |
| #2 | Part B — Feature inventory and traceability (F-01…F-12, AC-01…AC-18, RTM) | `issue/02-traceability` | Ba | Cl | Reviewed feature inventory, traceability matrix, and coverage checks | PR #6 (merged) | via release PR |
| #3 | Part C — System-Level SDS (Architecture, Data Model, API/UI, Roles, Security, GCP) | `issue/03-system-sds` | Cl | Ba | Reviewed 3-tier architecture, ER schema, role matrix, and GCP deployment plan | PR #8 (merged) | via release PR |
| #4 | Part D — Three-sprint plan (roadmap table, feature allocation, feasibility) | `issue/04-sprint-plan` | Ba | Cl | Reviewed 3-sprint plan, confirmed feature coverage and Sprint 1 feasibility | PR #9 (merged) | via release PR |
| #5 | Part E — Sprint 1 engineering contracts (F-01…F-05, STS TEST-01…26, DoD) | `issue/05-sprint1-contracts` | Ba | Cl | Reviewed feature contracts, STS matrix (TEST-01..26), and DoD | PR #12 (merged) | via release PR |
| #6 | AC-17 (Scaffold, PostgreSQL schema, migrations, idempotent seed, persistence test) | `issue/06-scaffold-db-seed` | Cl | Ba | Reviewed Prisma schema, migration 20261122000000_init, seed idempotency, and persistence test suite | PR #14 (merged) | via release PR |
| #7 | F-01 / AC-01..AC-04, AC-13 (Session authentication, login, logout, me, and RBAC middleware) | `issue/07-auth-session-rbac` | Cl | Ba | Reviewed session authentication, bcrypt verification, HttpOnly cookie lifecycle, and RBAC middleware | PR #16 (merged) | via release PR |
| #8 | F-01 / AC-18 (Login UI, busy state, generic error, role-conditional navigation, and session clearing on logout) | `feature/08-login-ui` | Ba | Cl | (Pending PR review) | PR (pending) | via release PR |

History sequence (contract → tests → implementation):
| Date | Commit | What |
|---|---|---|
| 2026-11-18 | `eea640b` | chore: setup issue 0 - remove outdated comments, add PR template and PDF draft skeleton |
| 2026-11-18 | `bd71d5b` | docs: complete Part A SRS and product scope baseline |
| 2026-11-20 | `c91d830` | docs: issue #2 - complete feature inventory and traceability matrix (Part B) |
| 2026-11-21 | `73d4a2b` | docs: issue #3 - complete System-Level SDS specification (Part C) |
| 2026-11-22 | `f2ead04` | docs: issue #4 - complete three-sprint plan and feasibility justification (Part D) |
| 2026-11-22 | `eac2826` | docs: issue #5 - complete Sprint 1 engineering contracts, STS, and DoD (Part E) |
| 2026-11-22 | `79fd61d` | feat: issue #6 - scaffold, database schema, Prisma migrations, idempotent seed, and persistence tests |
| 2026-11-22 | `cdc98d8` | test: issue #7 - add failing API integration tests for authentication and session lifecycle (TEST-01..TEST-04) |
| 2026-11-22 | `d44cba7` | feat: issue #7 - implement session authentication, login, logout, me, and RBAC middleware |
| 2026-11-22 | `pending` | feat: issue #8 - implement login UI, auth context, role-conditional navigation, and vitest suite |

Board status screenshot: ⬜ (#15)   Release PR / tag: ⬜ (#15)
### F.5 Contributions, AI use, limitations
| Student | Issues/PRs authored | PRs reviewed | Pair work |
|---|---|---|---|
| Cl | #0 (Scaffold & Draft setup), #1 (SRS specification), #3 (System-Level SDS), #6 (Database scaffold, migrations, seed & persistence), #7 (Backend auth, session & RBAC middleware) | #2 (Traceability matrix & Feature inventory), #4 (Reviewed Three-sprint plan), #5 (Reviewed Engineering contracts), #8 (Reviewing Login UI) | Architecture & domain design alignment, schema validation |
| Ba | #2 (Feature inventory & Traceability matrix), #4 (Three-sprint plan), #5 (Engineering contracts & STS), #8 (Login UI & Authenticated Shell) | #0 (Reviewed PR #2), #1 (Reviewed PR #4), #3 (Reviewed PR #8), #6 (Reviewed PR #14), #7 (Reviewed PR #16) | Architecture & domain design alignment, schema validation |

AI-use declaration:
- Claude / Antigravity: Assisted Cl with cleaning outdated comments, scaffolding PR template/draft skeleton (`#0`), and drafting SRS Part A (`#1`). Assisted Ba with decomposing features (F-01..12), formalizing acceptance criteria (AC-01..18), synthesizing bidirectional traceability matrices (`docs/features.md`, `docs/traceability.md`), and authoring Part B in `PDF_DRAFT.md` (`#2`). Assisted Cl with authoring `docs/system-sds.md`, designing the 3-tier architecture, data schemas, role/permission matrix, and generating visual diagrams (`#3`). Assisted Ba with establishing the three-sprint roadmap, drafting `docs/sprints/plan.md`, formatting the dependency graph, and documenting Part D in `PDF_DRAFT.md` (`#4`). Assisted Ba with writing feature engineering contracts (`F-01` to `F-05`), compiling the complete Software Test Specification (`TEST-01` to `TEST-26`), establishing the Product Definition of Done, and documenting Part E in `PDF_DRAFT.md` (`#5`). Assisted Cl with configuring Prisma ORM, authoring migrations and idempotent seed scripts, and implementing persistence test suite for AC-17 (`#6`). Assisted Cl with TDD test authoring (TEST-01..04, TEST-16), session management implementation with SHA-256 token hashing, HttpOnly cookie lifecycle, and RBAC middleware for F-01 (`#7`). Assisted Ba with developing the React authentication context (`AuthContext.tsx`), Login component with busy indicator and generic error handling (`Login.tsx`), role-segregated navigation bar (`Navbar.tsx`), and automated component testing in Vitest (`Login.test.tsx`) for Issue #8. Reviewed and verified by Ba and Cl.

Known limitations / incomplete work / skipped tests:
- None for Part A, Part B, Part C, Part D, Part E specifications, Part F.1 persistence foundation, or Part F.3 authentication suite.