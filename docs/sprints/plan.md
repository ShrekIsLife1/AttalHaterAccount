# Three-Sprint Product Plan

**Project:** UniMerch Campus Store (Theme 4: E-Commerce or Ordering System)  
**Course:** CPE 334 — Introduction to Software Engineering in the Age of AI Agents  
**Authors:** Student Ba (Author, Issue #4) & Student Cl (Reviewer)  
**Status:** Approved Baseline  

---

## 1. Executive Summary & Delivery Strategy

The UniMerch Campus Store is planned across three progressive, time-boxed sprints. The roadmap follows a strict **Specification-Driven Development (SDD)** and **Test-Driven Development (TDD)** discipline:
1. **Sprint 1 (Baseline & Working Slice):** Establish the core domain foundation, architectural conventions, database persistence, and a verified vertical slice covering authentication, product browsing, atomic multi-item ordering, customer order tracking, and operator order acceptance.
2. **Sprint 2 (Core Operational Expansion):** Expand operational control for store operators (catalog and inventory management), add order cancellation/rejection with automatic inventory rollback, implement the multi-stage physical fulfillment lifecycle, and integrate simulated payments.
3. **Sprint 3 (Hardening, Analytics & Experience):** Add analytical dashboards for store operations, full-text product search and order filtering, responsive design validation across screen sizes (375px to 1920px), and performance/reliability hardening.

---

## 2. Three-Sprint Roadmap Table

| Sprint | Checkpoint Date | Sprint Goal | Feature IDs & Scope | Key Dependencies | Completion Outcome / Deliverables |
|---|---|---|---|---|---|
| **Sprint 1** | **8 Nov 2026** | **Baseline Working Slice & Engineering Contracts**<br>Deliver an authoritative end-to-end purchasing workflow from authenticated customer catalog browsing to atomic multi-line order placement and operator order acceptance. | • **F-01:** Session Auth & RBAC (`CUSTOMER`, `OPERATOR`)<br>• **F-02:** Authoritative Catalog & Real-Time Stock<br>• **F-03:** Multi-Item Order Creation, Server Pricing & Atomic Decrement<br>• **F-04:** Customer Order History & Ownership Isolation<br>• **F-05:** Operator Order Queue & State Transition (`PLACED -> ACCEPTED`) | • Project scaffold & Docker readiness<br>• PostgreSQL DB & Prisma schema<br>• Idempotent seed data | **Working Sprint 1 increment on `main`:**<br>- Verified session auth (bcrypt, HttpOnly cookie)<br>- Authoritative catalog (minor-unit integer pricing)<br>- Atomic multi-line order placement with DB rollback on stockout<br>- Customer data isolation (HTTP 404 cross-access)<br>- Operator acceptance queue & transition<br>- Automated integration tests (STS suites)<br>- Living PDF Deliverable 1 (`PDF_DRAFT.md` / `deliverable-1.odt`) |
| **Sprint 2** | **29 Nov 2026** | **Core Operational Expansion & Fulfillment Lifecycle**<br>Equip store staff with catalog and inventory management, implement customer cancellation and operator rejection with inventory restitution, track multi-stage order fulfillment, and simulate checkout payment. | • **F-06:** Operator Catalog & Stock Management (CRUD, restock, active toggle)<br>• **F-07:** Order Cancellation & Rejection with Stock Rollback<br>• **F-08:** Extended Fulfillment Lifecycle (`ACCEPTED -> PREPARING -> READY -> COMPLETED`)<br>• **F-09:** Simulated Payment & Digital Counter Receipt | • Sprint 1 baseline (`F-01` to `F-05`)<br>• Relational persistence and atomic transaction mechanisms | **Sprint 2 release increment:**<br>- Operator back-office catalog CRUD<br>- Multi-stage state machine transitions with 409 conflict guards<br>- Automated inventory restitution on cancel/reject<br>- Simulated payment records and digital pickup receipts<br>- Deliverable 2 report with updated contracts |
| **Sprint 3** | **Progress: 29 Nov 2026<br>Complete: 13 Dec 2026** | **Operational Analytics, Search & System Hardening**<br>Provide business intelligence dashboards for operators, advanced catalog search and order filtering, validate responsive viewport adaptability, and benchmark application latency. | • **F-10:** Operator Metrics & Sales Dashboard<br>• **F-11:** Advanced Search, Filtering & Categorization<br>• **F-12:** System Hardening, Responsive Viewports & Performance Tuning | • Sprint 1 & 2 operational data models<br>• Playwright responsive viewport harness | **Final Release candidate & submission:**<br>- Sales analytics (revenue totals, order status counts, top products)<br>- Full-text search and multi-criteria order filter<br>- Responsive UI verified on mobile (375px), tablet (768px), and desktop (1920px)<br>- Sub-second order creation latency ($< 1000\text{ ms}$)<br>- Full regression test suite passing<br>- Final Delivery package |

---

## 3. Feature Allocation and Dependency Graph

### 3.1 Feature Allocation Matrix
Every feature in the product inventory (`F-01` to `F-12`) is strictly allocated to exactly one sprint:
- **Sprint 1 (5 Features):** `F-01`, `F-02`, `F-03`, `F-04`, `F-05`
- **Sprint 2 (4 Features):** `F-06`, `F-07`, `F-08`, `F-09`
- **Sprint 3 (3 Features):** `F-10`, `F-11`, `F-12`

### 3.2 Inter-Feature Dependencies

```
[F-01: Session Auth & RBAC]
   │
   ├──────────────────────────────┬──────────────────────────────┐
   ▼                              ▼                              ▼
[F-02: Product Catalog]   [F-04: Order History]        [F-05: Operator Queue]
   │                              ▲                              ▲
   ▼                              │                              │
[F-03: Multi-Line Orders] ────────┴──────────────────────────────┘
   │
   ├──────────────────────────────┬──────────────────────────────┐
   ▼                              ▼                              ▼
[F-06: Operator Catalog]  [F-07: Cancel & Reject]       [F-08: Extended Lifecycle]
(Sprint 2)                (Sprint 2)                    (Sprint 2)
   │                              │                              │
   └──────────────┬───────────────┴──────────────────────────────┘
                  ▼
          [F-09: Simulated Payment] (Sprint 2)
                  │
   ┌──────────────┴───────────────┬──────────────────────────────┐
   ▼                              ▼                              ▼
[F-10: Metrics Dashboard] [F-11: Advanced Search]       [F-12: System Hardening]
(Sprint 3)                (Sprint 3)                    (Sprint 3)
```

- `F-01` serves as the foundational security layer for all protected customer and operator routes.
- `F-02` feeds catalog data to `F-03` for order composition and stock validation.
- `F-03` is the core transaction engine; `F-04` and `F-05` display and transition orders generated by `F-03`.
- `F-06`, `F-07`, `F-08`, and `F-09` build directly upon the Sprint 1 entities (`Product`, `Order`, `OrderItem`).
- `F-10`, `F-11`, and `F-12` consume historical transactional data and optimize the system for production release.

---

## 4. Sprint 1 Feasibility Justification

The scope selected for Sprint 1 is **highly feasible, strictly contained, and fully aligned with the course expectations**:
1. **Vertical Slice Cohesion:** Sprint 1 implements a single, complete business flow: Customer logs in $\rightarrow$ browses catalog $\rightarrow$ submits multi-item order with server-calculated price and atomic inventory decrement $\rightarrow$ reviews order history $\rightarrow$ Operator logs in $\rightarrow$ views queue $\rightarrow$ accepts order.
2. **Explicit Scope Exclusions (Zero External Bottlenecks):** By formally excluding live payment gateways (Stripe/PayPal), external courier/shipping APIs, and external SMS/email notification providers, the team eliminates external API credentials, webhook latency, and third-party downtime.
3. **Pre-Built Architectural Foundations:** Utilizing an Express/Node backend, React/Vite frontend, and Prisma ORM against a local PostgreSQL database enables fast local iteration, automatic type safety across frontend and backend, and rapid automated testing with Vitest and Supertest.
4. **Deterministic Seed Data:** Testing does not depend on dynamic external user registration; pre-configured, bcrypt-hashed demo accounts ($\ge 3$ customers, $\ge 2$ operators) allow reproducible, automated end-to-end verification.
5. **Team Workload Distribution:** With 15 granular issues split evenly between Student Cl (8 issues) and Student Ba (7 issues), parallel development paths (e.g., Ba drafting contracts and frontend tests while Cl implements backend auth) guarantee completion within the allocated timeline.
