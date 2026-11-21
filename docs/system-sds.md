# System-Level Software Design Specification (SDS)

**Project:** UniMerch Campus Store (Theme 4: E-Commerce or Ordering System)  
**Document:** System-Level Architecture & Technical Design Specification  
**Authors:** Student Cl (Author) & Student Ba (Reviewer)  
**Status:** Approved Engineering Baseline (Part C)  

---

## 1. System Architecture & Technology Stack

### 1.1 Architectural Overview
The UniMerch Campus Store is structured as a classical, robust **three-tier client-server modular architecture**:

1. **Presentation Layer (UI Client):** Single Page Application (SPA) built with React 18, TypeScript, and Vite. Responsive styling is provided by Bootstrap 5 with custom CSS variables.
2. **Application / API Layer (Backend Server):** Modular Node.js / Express application written in TypeScript. Enforces all business logic, authorization policies, schema validation (Zod), and session management.
3. **Data Layer (Persistent Relational Database):** PostgreSQL 16 database managed via Prisma ORM 5. Persists entities across restarts with declarative schema migrations and strict integrity constraints.

```
+-----------------------------------------------------------------------------------+
|                            PRESENTATION TIER (Browser)                            |
|  React 18 + TypeScript + Vite | Role-Aware Navigation Shell | Bootstrap 5 Layout  |
+-----------------------------------------------------------------------------------+
                                     |
               HTTPS / JSON REST (HttpOnly Session Cookie)
                                     v
+-----------------------------------------------------------------------------------+
|                        APPLICATION / API TIER (Node.js/Express)                   |
|  - Auth Middleware (Session verification, role checking)                          |
|  - Domain Engine (Authoritative pricing, stock guards, state transition engine)   |
|  - Input Validation (Zod schemas, field error sanitization)                       |
+-----------------------------------------------------------------------------------+
                                     |
                          Prisma Client (SQL queries & $transactions)
                                     v
+-----------------------------------------------------------------------------------+
|                           DATA TIER (PostgreSQL Database)                         |
|  - Relations & Referential Integrity (FKs, Cascade Delete)                        |
|  - Check Constraints (quantity > 0, stock >= 0, price >= 0)                       |
|  - Acid Transactions ($transaction for order placement & stock decrements)        |
+-----------------------------------------------------------------------------------+
```

### 1.2 Enforcement of Business Rules
A foundational design principle of the system is that **all business rules are strictly enforced on the server-side**. The frontend provides optimistic UX indicators and client-side pre-validation for responsive feedback, but the backend is the sole source of truth:
- **Pricing:** Line totals and order grand totals are computed authoritatively on the server from current catalog prices in the database; any client-provided price or total is ignored.
- **Stock & Atomicity:** Stock availability checks and stock decrements are executed within a single database transaction (`prisma.$transaction`) alongside order creation.
- **Authorization & Ownership:** Endpoint access controls (`requireAuth`, `requireRole`) and record ownership filters (`where: { customerId: session.userId }`) are enforced before any data manipulation.

---

## 2. Data Model & Persistence Architecture

### 2.1 Entity Relationship Model
The data model consists of five core entities in Sprint 1: `User`, `Session`, `Product`, `Order`, and `OrderItem`.

```mermaid
erDiagram
    USER ||--o{ SESSION : "has active"
    USER ||--o{ ORDER : "places (as Customer)"
    USER ||--o{ ORDER : "accepts (as Operator)"
    ORDER ||--|{ ORDER_ITEM : "contains lines"
    PRODUCT ||--o{ ORDER_ITEM : "referenced in"

    USER {
        int id PK
        string email UK
        string passwordHash
        string name
        enum role "CUSTOMER | OPERATOR"
        boolean isActive
        datetime createdAt
        datetime updatedAt
    }

    SESSION {
        string id PK
        int userId FK
        string tokenHash UK
        datetime expiresAt
        datetime createdAt
    }

    PRODUCT {
        int id PK
        string name
        string description
        int priceMinor "CHECK >= 0"
        int stockQuantity "CHECK >= 0"
        boolean isActive
        datetime createdAt
        datetime updatedAt
    }

    ORDER {
        int id PK
        int customerId FK
        enum status "PLACED | ACCEPTED"
        int totalMinor "CHECK >= 0"
        datetime createdAt
        datetime acceptedAt
        int acceptedByOperatorId FK
    }

    ORDER_ITEM {
        int id PK
        int orderId FK
        int productId FK
        int quantity "CHECK > 0 AND <= 10"
        int unitPriceAtOrder "CHECK >= 0"
    }
```

### 2.2 Entity Definitions & Field Constraints

#### Entity: `User`
- `id` (Int, Primary Key, Autoincrement)
- `email` (String, Unique, Not Null, Normalized to lowercase)
- `passwordHash` (String, Not Null — salted bcrypt hash, never exposed to API)
- `name` (String, Not Null)
- `role` (Enum: `CUSTOMER`, `OPERATOR`, Not Null)
- `isActive` (Boolean, Default: `true`, Not Null)
- `createdAt` (DateTime, Default: `now()`)
- `updatedAt` (DateTime, Auto-updated)

#### Entity: `Session`
- `id` (String, Primary Key, UUIDv4)
- `userId` (Int, Foreign Key referencing `User.id`, `onDelete: Cascade`, Not Null)
- `tokenHash` (String, Unique, Not Null — SHA-256 hash of the raw cookie token)
- `expiresAt` (DateTime, Not Null — absolute expiration timestamp, e.g. 8 hours)
- `createdAt` (DateTime, Default: `now()`)

#### Entity: `Product`
- `id` (Int, Primary Key, Autoincrement)
- `name` (String, Not Null)
- `description` (String, Nullable)
- `priceMinor` (Int, Not Null, CHECK `priceMinor >= 0` — unit price in satang/cents)
- `stockQuantity` (Int, Not Null, CHECK `stockQuantity >= 0` — physical inventory count)
- `isActive` (Boolean, Default: `true`, Not Null — catalog visibility flag)
- `createdAt` (DateTime, Default: `now()`)
- `updatedAt` (DateTime, Auto-updated)

#### Entity: `Order`
- `id` (Int, Primary Key, Autoincrement)
- `customerId` (Int, Foreign Key referencing `User.id`, Not Null — record owner)
- `status` (Enum: `PLACED`, `ACCEPTED`, Not Null, Default: `PLACED`)
- `totalMinor` (Int, Not Null, CHECK `totalMinor >= 0` — authoritative order total in minor units)
- `createdAt` (DateTime, Default: `now()`)
- `acceptedAt` (DateTime, Nullable — timestamp when operator accepted order)
- `acceptedByOperatorId` (Int, Foreign Key referencing `User.id`, Nullable — operator audit link)

#### Entity: `OrderItem`
- `id` (Int, Primary Key, Autoincrement)
- `orderId` (Int, Foreign Key referencing `Order.id`, `onDelete: Cascade`, Not Null)
- `productId` (Int, Foreign Key referencing `Product.id`, Not Null)
- `quantity` (Int, Not Null, CHECK `quantity > 0 AND quantity <= 10`)
- `unitPriceAtOrder` (Int, Not Null, CHECK `unitPriceAtOrder >= 0` — immutable price snapshot)

### 2.3 Database Setup, Migrations & Idempotent Seed
- **Migrations:** Managed with Prisma Migrate (`prisma migrate dev`). SQL migration scripts are versioned in `server/prisma/migrations/`.
- **Seed Procedure:** Script `server/prisma/seed.ts` is fully **idempotent** (utilizing Prisma `upsert`). Executing `npm run seed` repeatedly will not create duplicate entries or violate unique constraints.
- **Initial Seed Dataset:**
  - $\ge 3$ Customers: `customer1@example.com`, `customer2@example.com`, `customer3@example.com`
  - $\ge 2$ Operators: `operator1@example.com`, `operator2@example.com`
  - $\ge 8$ Products: Includes active in-stock merchandise (Hoodie, T-Shirt, Notebook, Mug, Water Bottle, Cap), $\ge 1$ item with `stockQuantity = 0` (Pen Set - Out of Stock), and $\ge 1$ item with `isActive = false` (Discontinued Tote Bag).
  - Pre-hashed passwords via bcrypt (work factor 10). Seed configuration is sourced from environment variables; zero plain secrets in Git.

---

## 3. UI Conventions & Navigation Structure

### 3.1 Role-Based Screen Navigation
The user interface displays an authenticated application shell that adapts its top navigation bar dynamically based on the current user's role:

| Route Path | Accessible Role(s) | Screen / Purpose |
|---|---|---|
| `/login` | Public (Unauthenticated) | Clean authentication form (email & password). Redirects authenticated users. |
| `/catalog` | `CUSTOMER` (and `OPERATOR` read-only) | Grid of merchandise items, price in THB, stock availability badges, and quantity selectors. |
| `/cart` | `CUSTOMER` only | Review selected line items, modify quantities, view estimated total, submit order. |
| `/my-orders` | `CUSTOMER` only | Table of the customer's personal orders with status badges and creation dates. |
| `/orders/:id` | `CUSTOMER` (own order) / `OPERATOR` | Detailed breakdown of items, price snapshots, totals, and current status. |
| `/operator/orders` | `OPERATOR` only | Chronological queue of incoming `PLACED` orders with one-click Accept action. |

### 3.2 Standard UI Component States
All data-fetching and mutating views implement four standard visual states:
- **Idle State:** Default populated state with clean typography and actionable buttons.
- **Loading State:** Disabled buttons with animated spinner / text ("Submitting order...", "Authenticating..."). Skeletons or spinners for data fetches.
- **Empty State:** Distinct, helpful message when no data exists (e.g., "You have not placed any orders yet. Visit the Catalog to get started.").
- **Error State:** User-friendly alert banner displaying actionable feedback (e.g., "Insufficient stock for UniMerch Hoodie. Available: 2"). Never reveals raw database or server error traces.

---

## 4. API Conventions & Error Handling

### 4.1 Request & Response Format
All API endpoints adhere to standard REST conventions over HTTP, exchanging JSON payloads:
- Headers: `Content-Type: application/json`, `Accept: application/json`
- Credentials: `credentials: "include"` for cross-origin browser requests with session cookies.

### 4.2 Standard Endpoints (Sprint 1)

| Method | Endpoint | Allowed Role | Purpose |
|---|---|---|---|
| `POST` | `/api/auth/login` | Public | Authenticate user, issue HttpOnly session cookie, return user profile. |
| `POST` | `/api/auth/logout` | Authenticated | Invalidate server session, clear session cookie. |
| `GET` | `/api/auth/me` | Authenticated | Retrieve current session user profile (`id`, `name`, `email`, `role`). |
| `GET` | `/api/products` | Authenticated | Retrieve active and available catalog items with prices and stock status. |
| `POST` | `/api/orders` | `CUSTOMER` | Submit new multi-line order with server pricing and atomic stock deduction. |
| `GET` | `/api/orders` | `CUSTOMER` | List historical orders owned by authenticated customer. |
| `GET` | `/api/orders/:id` | `CUSTOMER` (own) / `OPERATOR` | Retrieve full order details and line items. |
| `GET` | `/api/operator/orders` | `OPERATOR` | List incoming orders queue (`status = PLACED`), oldest first. |
| `POST` | `/api/operator/orders/:id/accept` | `OPERATOR` | Transition order status `PLACED -> ACCEPTED`. |

### 4.3 Safe Error Envelope & HTTP Status Codes
All failure responses return a uniform, safe JSON structure:
```json
{
  "error": "Short human-readable summary",
  "details": [
    { "field": "items[0].quantity", "message": "Quantity must be between 1 and 10" }
  ]
}
```

- `400 Bad Request`: Validation failure (syntax error, non-integer quantity, duplicate items, quantity out of range $[1, 10]$).
- `401 Unauthorized`: Missing, invalid, or expired session token; invalid login credentials (generic message to prevent user enumeration).
- `403 Forbidden`: Authenticated user lacks the required role for the operation (e.g. Customer calling operator routes).
- `404 Not Found`: Target record does not exist OR record belongs to another customer (prevents ID enumeration/data leakage).
- `409 Conflict`: Business rule violation (product out of stock, insufficient inventory, invalid state transition such as re-accepting an order).
- `500 Internal Server Error`: Unexpected unhandled error. Generic message returned to client; detailed error logged to server stderr.

---

## 5. Role and Permission Matrix

The following matrix defines the exact access rights for every operation across the entire product:

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

---

## 6. Authentication & Session Lifecycle

### 6.1 Credential Storage & Hashing
- When users are seeded or created, plain text passwords are immediately passed to `bcrypt.hash(password, 10)`.
- The salt is generated uniquely per password.
- Raw password strings are never stored in memory longer than necessary and are never persisted or returned in API responses.

### 6.2 Session Token Generation & Cookie Storage
1. On successful `POST /api/auth/login`:
   - A cryptographically strong pseudo-random 32-byte token is generated using Node.js `crypto.randomBytes(32).toString("hex")`.
   - The token hash is stored in the `Session` database table alongside `userId` and `expiresAt` ($t_{\text{now}} + 8\text{ hours}$).
   - The raw token is sent to the client via an HTTP `Set-Cookie` header:
     ```http
     Set-Cookie: session_token=<token>; Path=/; HttpOnly; SameSite=Lax; Max-Age=28800;
     ```
2. On every incoming authenticated request:
   - Middleware `requireAuth` reads `req.cookies.session_token`.
   - Hashes the token and looks up active session where `expiresAt > now()`.
   - If not found or expired, returns HTTP 401 without private data.
   - If valid, attaches user record (`req.user = { id, email, name, role }`) to request.
3. On `POST /api/auth/logout`:
   - The session row is deleted from the `Session` table in PostgreSQL.
   - The cookie is cleared on the client (`Max-Age=0`).
   - Any further attempt to reuse the token returns HTTP 401.

---

## 7. Configuration & Cloud Deployment Architecture

### 7.1 Environment Variables
All configuration is strictly externalized via environment variables (never committed to repository):

| Variable Name | Description | Example (Development) |
|---|---|---|
| `PORT` | Local HTTP port for Express server | `3000` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@localhost:5432/unimerch` |
| `SESSION_SECRET` | Secret key for cookie signing / token salting | `dev-secret-string-replace-in-prod` |
| `CORS_ORIGIN` | Allowed web client origin | `http://localhost:5173` |
| `NODE_ENV` | Runtime environment mode | `development` / `production` |

A clean `.env.example` file is provided in the repository with placeholder values and clear instructions.

### 7.2 Docker & Containerization Suitability
The application is structured for containerized environments:
- Multi-stage Dockerfile for Node.js API (build stage with TypeScript compilation, lightweight production runtime stage).
- Multi-stage Dockerfile or static build for Vite/React frontend.
- Healthcheck endpoint `GET /api/health` available for container orchestrators.

### 7.3 Planned GCP Deployment Architecture (Lab 5 Alignment)
For future deployment in Lab 5:
- **Compute:** Google Cloud Run (serverless container runtime) running the backend API container.
- **Database:** Google Cloud SQL for PostgreSQL (managed relational instance with persistent storage and automatic backups).
- **Secrets:** Google Cloud Secret Manager injecting `DATABASE_URL` and `SESSION_SECRET` securely into Cloud Run environment variables at runtime.
- **Static Hosting:** Cloud Storage + Cloud CDN (or direct static serving through Express) for the React frontend SPA.
