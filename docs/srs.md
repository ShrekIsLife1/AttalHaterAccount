# Software Requirements Specification (SRS)

**Project:** UniMerch Campus Store (Theme 4: E-Commerce or Ordering System)  
**Course:** CPE 334 — Introduction to Software Engineering in the Age of AI Agents  
**Scope:** Full Product Baseline (Sprints 1, 2, and 3)  
**Authors:** Student Cl (Author) & Student Ba (Reviewer)  
**Status:** Approved Baseline  

---

## 1. Problem Statement & Context

### 1.1 Context
The **UniMerch Campus Store** is an on-campus merchandise shop serving university students, faculty, alumni, and administrative staff. The shop offers branded merchandise, apparel (hoodies, t-shirts), stationery (notebooks, pens), and everyday campus accessories (water bottles, tote bags, mugs).

### 1.2 Stakeholder Problem
Currently, the physical store suffers from substantial operational bottlenecks:
- **Long Counter Queues:** During semester openings and campus events, students wait in long queues just to enquire about product availability and prices.
- **Stock Inconsistencies:** Store operators manually track physical inventory, leading to overselling or discovering that requested items are out of stock after payment attempts.
- **Manual Order Processing:** Paper-based receipts and untracked orders result in delayed fulfillment and occasional misplaced orders.
- **Pricing Discrepancies:** Outdated printed price tags lead to friction at checkout when prices are updated in central store logs.

### 1.3 Solution Vision
A robust web-based ordering application that allows customers to view authoritative catalog items with live availability, place multi-item orders with server-validated pricing, and track their order status. Store operators manage an organized incoming queue, review order lines, and progress orders through transparent fulfillment stages.

---

## 2. Actors and Responsibilities

| Actor | Description | Core Responsibilities |
|---|---|---|
| **Customer** | Enrolled student or staff member purchasing merchandise | - Authenticate securely via email and password.<br>- Browse product catalog with authoritative prices and stock availability.<br>- Assemble and submit multi-line orders.<br>- View own order history and track order status.<br>- Cannot modify catalog, cannot accept orders, cannot view other customers' orders. |
| **Operator** | Campus store staff member managing fulfillment and catalog | - Authenticate securely via email and password.<br>- View incoming orders queue (`PLACED`) sorted chronologically.<br>- Accept incoming orders (`PLACED -> ACCEPTED`) with recorded timestamp and operator identity.<br>- Progress order fulfillment in subsequent sprints (`PREPARING -> READY -> COMPLETED`).<br>- Manage catalog items, pricing, and stock levels (Sprint 2).<br>- Cannot place orders as an operator; accesses customer orders within store scope. |

---

## 3. Product Scope and Explicit Exclusions

### 3.1 In Scope
- **Sprint 1 (Baseline & Working Slice):**
  - Session-based authentication with role-based access control (`CUSTOMER`, `OPERATOR`).
  - Read-only product catalog displaying live availability badges and minor-unit prices.
  - Multi-line customer order placement with server-side pricing, inventory validation, and atomic stock decrement.
  - Customer order history ("My Orders") and individual order detail retrieval.
  - Operator incoming order list and atomic order acceptance transition (`PLACED -> ACCEPTED`).
  - Persistent relational database storage (PostgreSQL via Prisma) and idempotent seed data.
- **Sprint 2 (Core Expansion):**
  - Operator catalog management (create, update, toggle active status, restock).
  - Order cancellation by customer (while `PLACED`) and rejection by operator with reason.
  - Extended order fulfillment lifecycle (`ACCEPTED -> PREPARING -> READY -> COMPLETED`).
  - Simulated payment transaction and receipt generation.
- **Sprint 3 (Hardening & Reporting):**
  - Operator sales and order metrics summary (sales total, orders by status, popular items).
  - Order filtering by status and date; product search by keyword and category.
  - Hardened error handling, comprehensive E2E verification, and performance benchmarks.

### 3.2 Explicit Exclusions
- **No Real Payment Gateways:** Integration with live payment gateways (Stripe, PayPal, promptpay banking APIs) is strictly excluded; simulated payment states and synthetic transactions are used.
- **No External Delivery / Logistics APIs:** Delivery is on-campus pickup at the UniMerch service counter; no third-party courier APIs (DHL, Kerry) are integrated.
- **No External Communication Providers:** No external SMS (Twilio) or email (SendGrid) providers; order notifications and status updates occur strictly within the authenticated web application.
- **No Self-Registration or Password Recovery in Sprint 1:** User accounts are provisioned via reproducible, idempotent seed scripts with pre-hashed credentials. Self-registration and password reset workflows are out of scope for Sprint 1.

---

## 4. Functional Requirements (FR)

### 4.1 Sprint 1 Requirements (Baseline Vertical Slice)
- **FR-01 (User Authentication):** A user can submit valid credentials (email and password) to log in. The system creates a secure session and returns the user's profile (`id`, `name`, `role`). Password hashes are never returned.
- **FR-02 (User Logout):** An authenticated user can log out. The backend invalidates the session server-side, clearing the authentication cookie. Subsequent requests with the terminated session are rejected.
- **FR-03 (Catalog Browsing):** An authenticated customer or operator can retrieve the catalog of products. Each product displays name, description, unit price (formatted in minor units), and an availability status (`inStock` or `unavailable`).
- **FR-04 (Order Placement):** A customer can submit an order containing 1 to $N$ distinct product lines with specified quantities. The server computes the total authoritatively, validates stock, snapshots unit prices, decrements inventory, and saves the order in `PLACED` status in a single atomic transaction.
- **FR-05 (Customer Order History & Detail):** A customer can view a list of all orders they previously placed (showing order ID, date, status, and total). The customer can open any of their own orders to inspect full line details.
- **FR-06 (Operator Incoming Orders):** An operator can view a queue of all incoming orders with `status = PLACED`, ordered chronologically (oldest first) to ensure fair first-in-first-out processing.
- **FR-07 (Operator Order Acceptance):** An operator can accept a `PLACED` order. The backend updates the order `status = ACCEPTED`, records `acceptedAt` timestamp, and records `acceptedByOperatorId` referencing the acting operator.

### 4.2 Sprint 2 Requirements (Core Expansion)
- **FR-08 (Operator Catalog Management):** An operator can create a new product, edit product metadata (name, description, price in minor units), adjust `stockQuantity`, and toggle product `isActive` status.
- **FR-09 (Order Cancellation and Rejection):** A customer can cancel their own order while it remains in `PLACED` status (restoring stock). An operator can reject a `PLACED` order with an operator reason note (restoring stock).
- **FR-10 (Extended Fulfillment Transitions):** An operator can advance an order through sequential statuses: `ACCEPTED -> PREPARING -> READY -> COMPLETED`.
- **FR-11 (Simulated Payment Processing):** A customer can execute a simulated payment for an accepted order, transitioning payment status from `PENDING` to `PAID` with a generated synthetic transaction reference.

### 4.3 Sprint 3 Requirements (Hardening & Reporting)
- **FR-12 (Sales and Order Analytics):** An operator can view aggregated sales figures: total revenue in minor units, order counts categorized by status, and inventory turnover by item.
- **FR-13 (Order Search and Filtering):** Users can search and filter orders: customers filter own orders by status and date range; operators filter all orders by customer email, status, and date range.

---

## 5. Business Rules (BR)

- **BR-01 (Authoritative Server-Side Pricing):** Order line totals and order grand totals must be calculated strictly on the backend using authoritative product prices stored in the database. Any client-submitted `price`, `unitPrice`, or `total` in the request body is completely ignored.
- **BR-02 (Line Quantity Boundaries):** Each order line `quantity` must be a positive integer such that $1 \le \text{quantity} \le \text{MAX\_QTY\_PER\_LINE}$ (configured to 10). Quantities $\le 0$, non-integers, missing values, or values $> 10$ must be rejected with HTTP 400.
- **BR-03 (Inventory Availability & Atomicity):** A product is orderable only if `isActive = true` and `stockQuantity >= requested_quantity`. An order cannot contain duplicate product entries across multiple lines. If any line item is unavailable or invalid, the entire order submission is rejected (HTTP 400 or 409), no partial order is saved, and product stock remains unchanged (all-or-nothing database transaction).
- **BR-04 (Price Snapshot Immutability):** When an order is created, the current unit price of each item is captured in `OrderItem.unitPriceAtOrder`. Any subsequent price updates to `Product.priceMinor` in the catalog must never alter historical orders or their computed totals.
- **BR-05 (Customer Ownership & Privacy):** A customer can access only orders where `Order.customerId` matches their own authenticated user ID. Any request by Customer A to read or inspect Customer B's order must return HTTP 404 (Not Found) without confirming the existence of the record or leaking private data.
- **BR-06 (Strict State Transition Lifecycle):** In Sprint 1, the only permitted order state transition is `PLACED -> ACCEPTED` initiated by an operator. Transitioning an order that is already `ACCEPTED` (or in any other status) must be rejected with HTTP 409 (Conflict), leaving database state untouched.
- **BR-07 (Secure Credential Storage):** Passwords must never be stored in plaintext. Passwords must be hashed using a salted cryptographic hashing algorithm (bcrypt with minimum work factor 10 or argon2) prior to database insertion.
- **BR-08 (Operator Scope and Role Restrictions):** Only authenticated users with role `OPERATOR` are authorized to list incoming orders or trigger the accept transition. Any request by a `CUSTOMER` to operator endpoints must be rejected with HTTP 403 (Forbidden).

---

## 6. Non-Functional Requirements (NFR)

| NFR ID | Requirement Statement | Measurable Target | Verification Method | Sprint |
|---|---|---|---|---|
| **NFR-01** | **Authentication & Role Authorization Enforcement** | 100% of protected routes reject unauthenticated requests with HTTP 401 and empty/safe error payload; role violations return HTTP 403; cross-user order access returns HTTP 404. | Automated integration tests (`auth.api.test.ts`, `orders-access.api.test.ts`, `operator-orders.api.test.ts`). | Sprint 1 |
| **NFR-02** | **Relational Data Persistence Across Restarts** | All database records (users, products, orders, order items, sessions) persist across application process stops and restarts. | Automated persistence test (`persistence.api.test.ts`) that disconnects, queries data, and verifies state intact. | Sprint 1 |
| **NFR-03** | **Seed Reproducibility & Idempotence** | Executing the database seed command consecutively does not produce duplicate rows or trigger constraint violations. | Scripted test running `npm run seed && npm run seed` and asserting identical record counts. | Sprint 1 |
| **NFR-04** | **Fresh Clone Reproducibility** | A developer can clone a fresh repository and execute install, migration, seed, test, and dev server in under 5 minutes following only the `README.md`. | Timed manual and scripted clean-room test on a separate workspace clone. | Sprint 1 |
| **NFR-05** | **Order Placement Latency** | A valid 10-line order creation request responds with HTTP 201 in under $1000\text{ ms}$ on local developer environment. | Automated benchmark test measuring API round-trip duration under local test database. | Sprint 3 |
| **NFR-06** | **Responsive User Interface** | Web application layouts adapt cleanly without horizontal scrolling or clipping across screen widths from $375\text{ px}$ (mobile) to $1920\text{ px}$ (desktop). | Visual inspection and automated Playwright responsive viewport assertions. | Sprint 3 |

---

## 7. Assumptions, Frozen Design Decisions, and Open Questions

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
