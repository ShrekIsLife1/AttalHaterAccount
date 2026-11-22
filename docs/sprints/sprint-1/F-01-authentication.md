# Feature Contract: F-01 — Session Authentication and Role-Based Access Control

**Sprint:** Sprint 1 Baseline  
**Feature ID:** F-01  
**Primary Actors:** Customer, Operator  
**Linked Requirements:** `FR-01`, `FR-02`, `FR-03`, `BR-07`, `BR-08`, `NFR-01`  
**Planned Acceptance Criteria:** `AC-01`, `AC-02`, `AC-03`, `AC-04`, `AC-13`, `AC-17`, `AC-18`  
**STS Test Mappings:** `TEST-01`, `TEST-02`, `TEST-03`, `TEST-04`, `TEST-16`, `TEST-21`, `TEST-22`  

---

## 1. Overview & Business Workflow

`F-01` provides secure, stateful authentication and role segregation across the UniMerch Campus Store platform. The system employs server-side session management backed by PostgreSQL and delivered via cryptographically secure `HttpOnly` session cookies.

### Authentication Lifecycle Flow
1. **Login:** User submits `email` and `password`. The server normalizes the email, retrieves the active user, verifies the password against the bcrypt hash (`saltRounds >= 10`), generates a secure random 32-byte session token, stores the `Session` record in the database with an 8-hour expiration timestamp, and sets an `HttpOnly`, `SameSite=Lax` cookie.
2. **Current Identity (`/me`):** Authenticated requests include the session cookie. Middleware queries the session store, extracts the authenticated `User` record, and returns safe identity fields (`id`, `name`, `email`, `role`). Password hashes and raw tokens are never exposed.
3. **Route Protection (RBAC Middleware):**
   - Requests without a valid, unexpired session cookie to protected routes are rejected immediately with HTTP 401.
   - Requests by authenticated users lacking the required role (e.g. `CUSTOMER` accessing `/api/operator/*`) are rejected with HTTP 403 Forbidden.
4. **Logout:** User submits logout. The server invalidates the session record in PostgreSQL, expires the client cookie, and returns HTTP 200.

---

## 2. Dependencies & Enforced Business Rules

- **Dependencies:** Base schema scaffold and PostgreSQL database connection (`User` and `Session` tables).
- **Enforced Business Rules:**
  - `BR-07` (Secure Credential Storage): Passwords hashed with bcrypt (salt factor $\ge 10$). Plaintext passwords never stored or logged.
  - `BR-08` (Operator Scope and Role Restrictions): Only accounts with role `OPERATOR` can access operator queues and fulfillment actions. Customers calling operator endpoints receive HTTP 403.
  - `NFR-01` (Security & RBAC Enforcement): 100% of protected routes enforce authentication; role violations return HTTP 403; bad credentials return generic HTTP 401 without user enumeration.

---

## 3. Boundary, Negative & Failure Cases

- **Unknown Email / Wrong Password:** Returns identical generic error `HTTP 401 Unauthorized` with `{ "error": "Invalid email or password" }`. No user enumeration possible.
- **Inactive Account:** If `User.isActive = false`, login fails with the same generic HTTP 401.
- **Malformed Input:** Missing email or password returns `HTTP 400 Bad Request` with field validation errors.
- **Expired Session:** If `expiresAt < now()`, the session is treated as non-existent; endpoint returns `HTTP 401`.
- **Session Replay After Logout:** Once logged out, previous cookie tokens return `HTTP 401`.

---

## 4. UI Behavior & View States

- **Login Screen (`/login`):**
  - Email and password input fields with client-side format validation.
  - Loading spinner upon form submission; input disabled during network request.
  - Error alert displaying generic error message on HTTP 401.
- **Authenticated Shell / Navigation Bar:**
  - Displays user name, email, and role badge (`Customer` or `Operator`).
  - Navigation links filtered strictly by role:
    - `CUSTOMER`: "Catalog", "My Orders", "Logout".
    - `OPERATOR`: "Incoming Orders", "Logout".
  - Logout button triggers `POST /api/auth/logout`, redirects to `/login`, and clears cached user context.

---

## 5. API Specification

### 5.1 POST `/api/auth/login`
- **Access:** Public (Unauthenticated)
- **Request Body:**
  ```json
  {
    "email": "customer1@example.com",
    "password": "ValidPassword123!"
  }
  ```
- **Response `200 OK`:** Sets cookie `sid=<token>; HttpOnly; Path=/; SameSite=Lax; Max-Age=28800`.
  ```json
  {
    "user": {
      "id": "usr_c1a2b3c4d5",
      "name": "Jane Doe",
      "email": "customer1@example.com",
      "role": "CUSTOMER"
    }
  }
  ```
- **Error Responses:**
  - `400 Bad Request`: `{ "error": "Validation error", "details": ["Email is required"] }`
  - `401 Unauthorized`: `{ "error": "Invalid email or password" }`

### 5.2 GET `/api/auth/me`
- **Access:** Authenticated (`CUSTOMER` or `OPERATOR`)
- **Headers / Cookie:** `Cookie: sid=<token>`
- **Response `200 OK`:**
  ```json
  {
    "user": {
      "id": "usr_c1a2b3c4d5",
      "name": "Jane Doe",
      "email": "customer1@example.com",
      "role": "CUSTOMER"
    }
  }
  ```
- **Error Response:**
  - `401 Unauthorized`: `{ "error": "Authentication required" }`

### 5.3 POST `/api/auth/logout`
- **Access:** Authenticated
- **Response `200 OK`:** Clears `sid` cookie.
  ```json
  {
    "message": "Logged out successfully"
  }
  ```

---

## 6. Data Model & Database Constraints

```prisma
model User {
  id           String    @id @default(cuid())
  email        String    @unique
  passwordHash String
  name         String
  role         Role      @default(CUSTOMER)
  isActive     Boolean   @default(true)
  createdAt    DateTime  @default(now())
  updatedAt    DateTime  @updatedAt
  sessions     Session[]
  orders       Order[]   @relation("CustomerOrders")
}

model Session {
  id        String   @id @default(cuid())
  token     String   @unique
  userId    String
  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  expiresAt DateTime
  createdAt DateTime @default(now())

  @@index([token])
  @@index([userId])
}

enum Role {
  CUSTOMER
  OPERATOR
}
```

---

## 7. Acceptance Criteria (AC)

- **AC-01:** Valid login credentials return HTTP 200, user profile without password hash, and set an `HttpOnly` session cookie.
- **AC-02:** Unknown email or wrong password returns generic HTTP 401 without leaking user existence.
- **AC-03:** Protected routes invoked without a session or with an invalid token return HTTP 401.
- **AC-04:** Calling logout invalidates the session in the database and subsequent calls to `/api/auth/me` return HTTP 401.
- **AC-13:** A user authenticated with `CUSTOMER` role calling operator endpoints receives HTTP 403 Forbidden.
- **AC-17:** A user authenticated with `OPERATOR` role attempting customer-only order creation receives HTTP 403 Forbidden.
- **AC-18:** Deterministic seed populates $\ge 3$ customers and $\ge 2$ operators with bcrypt hashes; password values are never committed to Git.
