# UniMerch Campus Store — E-Commerce & Ordering System

[![Sprint 1 Staging](https://img.shields.io/badge/branch-sprint1--staging-blue.svg)](https://github.com/ShrekIsLife1/AttalHaterAccount/tree/sprint1-staging)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**UniMerch** is an authoritative on-campus merchandise e-commerce and ordering platform designed for university students, faculty, and campus store operators. It resolves physical store bottlenecks through live catalog availability, authoritative server-side pricing calculations, atomic stock decrements, customer order tracking, and an incoming order fulfillment queue for store operators.

---

## 👥 Team Information
- **Course:** CPE 334 — Introduction to Software Engineering in the Age of AI Agents (2026)
- **Theme 4:** E-Commerce or Ordering System
- **Authors:**
  - **Clément Dominique Delrieu** (Student ID: `69540460016`, GitHub: [@ClemDelGh](https://github.com/ClemDelGh))
  - **Baptiste Carré** (Student ID: `69540460014`, GitHub: [@ShrekIsLife1](https://github.com/ShrekIsLife1))
- **Repository:** [https://github.com/ShrekIsLife1/AttalHaterAccount](https://github.com/ShrekIsLife1/AttalHaterAccount)
- **Living Deliverable:** [`docs/deliverable-1/deliverable-1.odt`](docs/deliverable-1/deliverable-1.odt)

---

## 🏛️ System Architecture

The application implements a clean **Three-Tier Architecture**:
1. **Presentation Tier (`client/`):** React 18 SPA built with Vite, TypeScript, and Bootstrap 5. Features role-based views (`CUSTOMER` vs `OPERATOR`), real-time stock badges, and strict state handling (Idle, Loading, Empty, Error).
2. **Application / API Tier (`server/`):** Node.js 20 with Express, TypeScript, and Zod. Enforces domain pricing rules, transaction atomicity (`prisma.$transaction`), session-based authentication (`HttpOnly` cookies), and role-based access control (RBAC).
3. **Data Tier (PostgreSQL 16 via Prisma ORM):** Persistent relational database housing users, sessions, products, orders, and line items with strict foreign keys and constraints.

---

## 📋 Prerequisites

Before starting, ensure you have the following installed on your machine:
- **Node.js** >= 20.x (`node -v`)
- **npm** >= 10.x (`npm -v`)
- **PostgreSQL** 16+ running locally on port `5432`

---

## 🚀 Quick Setup & Installation

Follow these steps to set up the project locally on a fresh clone in less than 5 minutes.

### 1. Clone the Repository
```bash
git clone https://github.com/ShrekIsLife1/AttalHaterAccount.git
cd AttalHaterAccount
git checkout sprint1-staging
```

### 2. Configure Environment Variables
Copy the example environment configurations for both server and client:

```bash
# Server environment configuration
cp server/.env.example server/.env

# Client environment configuration
cp client/.env.example client/.env
```

Ensure `server/.env` points to your PostgreSQL instance:
```ini
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/unimerch?schema=public"
PORT=3000
SESSION_SECRET="unimerch-super-secret-session-key-change-in-production"
CORS_ORIGIN="http://localhost:5173"
NODE_ENV="development"
SEED_PASSWORD="password123"
```

### 3. Install Dependencies
Install dependencies in both server and client directories:

```bash
# Install backend dependencies
cd server
npm install

# Install frontend dependencies
cd ../client
npm install
cd ..
```

---

## 🗄️ Database Migration & Seeding

### 1. Apply Database Migrations
Run Prisma migrations to create the database schema:

```bash
cd server
npx prisma migrate deploy
```

### 2. Seed Database
Populate the database with demo users, roles, and catalog products:

```bash
npm run seed
```

> **Note on Idempotency:** The seed script uses `upsert` operations. You can run `npm run seed` repeatedly without producing duplicate records or constraint errors.

### 🔑 Seeded Demo Credentials

| Role | Email | Password | Permissions & Scope |
|---|---|---|---|
| **CUSTOMER** | `customer1@unimerch.ac.th` | `Password123!` | Browse catalog, place orders, view personal order history. |
| **CUSTOMER** | `customer2@unimerch.ac.th` | `Password123!` | Browse catalog, place orders, view personal order history. |
| **CUSTOMER** | `customer3@unimerch.ac.th` | `Password123!` | Browse catalog, place orders, view personal order history. |
| **OPERATOR** | `operator1@unimerch.ac.th` | `Operator123!` | View incoming queue, accept orders (`PLACED -> ACCEPTED`). |
| **OPERATOR** | `operator2@unimerch.ac.th` | `Operator123!` | View incoming queue, accept orders (`PLACED -> ACCEPTED`). |

---

## 💻 Running the Application

### Start Backend Server
```bash
cd server
npm run dev
```
The server will start at `http://localhost:3000`.

### Start Frontend Client
```bash
cd client
npm run dev
```
The client will start at `http://localhost:5173`. Open your browser and navigate to this URL.

---

## 🧪 Running Automated Tests

All tests are executed using **Vitest**:

```bash
# Run all backend tests
cd server
npm test

# Run specific persistence and seed verification tests (AC-17 / TEST-21)
npm test -- sprint-1/persistence

# Run client tests
cd ../client
npm test
```

---

## 📁 Engineering Documentation & Traceability

- **Part A — SRS & Product Scope:** [`docs/srs.md`](docs/srs.md)
- **Part B — Feature Inventory & Traceability:** [`docs/features.md`](docs/features.md) & [`docs/traceability.md`](docs/traceability.md)
- **Part C — System-Level SDS & Architecture:** [`docs/system-sds.md`](docs/system-sds.md)
- **Part D — Three-Sprint Roadmap & Plan:** [`docs/sprints/plan.md`](docs/sprints/plan.md)
- **Part E — Sprint 1 Engineering Contracts & STS:** [`docs/sprints/sprint-1/`](docs/sprints/sprint-1/)
- **Part F — Living Deliverable Document:** [`docs/deliverable-1/deliverable-1.odt`](docs/deliverable-1/deliverable-1.odt)
