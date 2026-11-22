#!/usr/bin/env python3
"""
Update docs/deliverable-1/deliverable-1.odt with Part C content (Issue #3)
"""
import zipfile, io, os

odt_path = "docs/deliverable-1/deliverable-1.odt"

# Read existing ODT
with zipfile.ZipFile(odt_path, 'r') as z:
    file_map = {name: z.read(name) for name in z.namelist()}

content_xml = file_map['content.xml'].decode('utf-8')

# Part C XML replacement snippet
part_c_target = '<text:h text:style-name="Heading_20_2" text:outline-level="2"><text:bookmark-start text:name="part-c-system-level-sds-3" />Part C — System-Level SDS ⬜ (#3)<text:bookmark-end text:name="part-c-system-level-sds-3" /></text:h>'

part_c_replacement = """<text:h text:style-name="Heading_20_2" text:outline-level="2"><text:bookmark-start text:name="part-c-system-level-sds-3" />Part C — System-Level SDS ✅ (#3)<text:bookmark-end text:name="part-c-system-level-sds-3" /></text:h>
<text:p text:style-name="Text_20_body">Link to docs/system-sds.md: https://github.com/ShrekIsLife1/AttalHaterAccount/blob/sprint1-staging/docs/system-sds.md</text:p>

<text:h text:style-name="Heading_20_3" text:outline-level="3">C.1 System Architecture &amp; Technology Stack</text:h>
<text:p text:style-name="Text_20_body">Three-tier modular architecture: (1) Presentation Tier: React 18 SPA + TypeScript + Vite + Bootstrap 5; (2) API Tier: Node.js 20 Express modular server + Zod validation; (3) Data Tier: PostgreSQL 16 + Prisma ORM 5.</text:p>
<text:p text:style-name="Text_20_body">Business Rule Enforcement: Strictly enforced on server-side. Client-sent totals/prices are discarded. Orders and stock decrements run inside atomic Prisma $transaction.</text:p>
<text:p text:style-name="Text_20_body">Architecture Diagram: docs/deliverable-1/evidence/issue-03_architecture-diagram.png</text:p>

<text:h text:style-name="Heading_20_3" text:outline-level="3">C.2 Data Model &amp; Persistence Architecture</text:h>
<text:p text:style-name="Text_20_body">Core Entities: User (id, email UK, passwordHash, role, isActive), Session (id UUID, userId FK, tokenHash UK, expiresAt), Product (id, name, priceMinor, stockQuantity, isActive), Order (id, customerId FK, status, totalMinor, createdAt, acceptedAt, acceptedByOperatorId FK), OrderItem (id, orderId FK, productId FK, quantity 1..10, unitPriceAtOrder snapshot).</text:p>
<text:p text:style-name="Text_20_body">Integrity: Foreign keys with cascade deletion on Sessions &amp; OrderItems. CHECK constraints: quantity 1..10, stock &gt;= 0, prices in minor units (integer satang).</text:p>
<text:p text:style-name="Text_20_body">Idempotent Seed: Seed script populates &gt;=3 customers, &gt;=2 operators, &gt;=8 products (incl. out-of-stock and inactive). Multiple runs produce 0 duplicates.</text:p>
<text:p text:style-name="Text_20_body">ER Diagram: docs/deliverable-1/evidence/issue-03_er-diagram.png</text:p>

<text:h text:style-name="Heading_20_3" text:outline-level="3">C.3 UI Conventions &amp; Role-Aware Navigation</text:h>
<text:p text:style-name="Text_20_body">Routes: Public: /login. Customer: /catalog (cards with availability badges), /cart (review &amp; checkout), /my-orders (personal history), /orders/:id (detail). Operator: /operator/orders (chronological queue with Accept action).</text:p>
<text:p text:style-name="Text_20_body">Interactive States: Idle, Loading (spinners/disabled buttons), Empty (friendly guidance), Error (actionable alerts without internal traces).</text:p>

<text:h text:style-name="Heading_20_3" text:outline-level="3">C.4 API Conventions &amp; Safe Error Handling</text:h>
<text:p text:style-name="Text_20_body">RESTful JSON over HTTPS. Cookies: session_token HttpOnly SameSite=Lax. Safe status codes: 200/201 (success), 400 (validation), 401 (unauth/invalid creds), 403 (forbidden role), 404 (non-existent or other customer's order without leak), 409 (conflict/out of stock/invalid transition), 500 (internal error).</text:p>

<text:h text:style-name="Heading_20_3" text:outline-level="3">C.5 Role &amp; Permission Matrix</text:h>
<text:p text:style-name="Text_20_body">• Login/Catalog: Accessible by Customer &amp; Operator.</text:p>
<text:p text:style-name="Text_20_body">• Place Order / My Orders: Customer only (403 for Operator). Customer accesses own orders only (404 for cross-customer access).</text:p>
<text:p text:style-name="Text_20_body">• Operator Incoming Queue &amp; Accept: Operator only (403 for Customer). Only PLACED -&gt; ACCEPTED allowed (409 if already accepted).</text:p>

<text:h text:style-name="Heading_20_3" text:outline-level="3">C.6 Authentication &amp; Session Lifecycle</text:h>
<text:p text:style-name="Text_20_body">Password security via salted bcrypt (work factor 10). Cryptographic 32-byte session tokens hashed in database with 8-hour expiry. Revocation on logout deletes session row from DB and clears client cookie.</text:p>

<text:h text:style-name="Heading_20_3" text:outline-level="3">C.7 Configuration &amp; Cloud Deployment (Docker &amp; GCP)</text:h>
<text:p text:style-name="Text_20_body">Environment variables externalized (.env.example). Multi-stage Dockerfile packaging Node/Express API. Planned GCP architecture for Lab 5: Cloud Run (stateless container) + Cloud SQL (managed PostgreSQL) + Secret Manager (secrets injection).</text:p>"""

if part_c_target in content_xml:
    content_xml = content_xml.replace(part_c_target, part_c_replacement)
    print("Part C inserted successfully into content.xml!")
else:
    print("WARNING: part_c_target not found in content.xml!")

file_map['content.xml'] = content_xml.encode('utf-8')

# Write updated ODT
with zipfile.ZipFile(odt_path, 'w', compression=zipfile.ZIP_DEFLATED) as z_out:
    for name, data in file_map.items():
        z_out.writestr(name, data)

print(f"Updated {odt_path} successfully!")
