#!/usr/bin/env python3
"""
Script to generate and progressively update docs/deliverable-1/deliverable-1.odt
"""
import os
from odf.opendocument import OpenDocumentText
from odf.style import (
    Style, TextProperties, ParagraphProperties, TableCellProperties
)
from odf.text import P
from odf.table import Table, TableColumn, TableRow, TableCell

def create_deliverable_odt(output_path="docs/deliverable-1/deliverable-1.odt"):
    doc = OpenDocumentText()

    # --- Define Styles ---
    # Title style
    title_style = Style(name="DocTitle", family="paragraph")
    title_style.addElement(ParagraphProperties(textalign="center", marginbottom="15pt", margintop="10pt"))
    title_style.addElement(TextProperties(fontsize="22pt", fontweight="bold", fontfamily="Liberation Sans", color="#1b5e20"))
    doc.styles.addElement(title_style)

    # Subtitle style
    subtitle_style = Style(name="DocSubtitle", family="paragraph")
    subtitle_style.addElement(ParagraphProperties(textalign="center", marginbottom="12pt"))
    subtitle_style.addElement(TextProperties(fontsize="14pt", fontweight="bold", fontfamily="Liberation Sans", color="#333333"))
    doc.styles.addElement(subtitle_style)

    # Meta info style
    meta_style = Style(name="DocMeta", family="paragraph")
    meta_style.addElement(ParagraphProperties(textalign="center", marginbottom="20pt"))
    meta_style.addElement(TextProperties(fontsize="11pt", fontfamily="Liberation Sans", color="#555555"))
    doc.styles.addElement(meta_style)

    # Heading 1 style
    h1_style = Style(name="CustomH1", family="paragraph")
    h1_style.addElement(ParagraphProperties(margintop="16pt", marginbottom="8pt"))
    h1_style.addElement(TextProperties(fontsize="16pt", fontweight="bold", fontfamily="Liberation Sans", color="#1b5e20"))
    doc.styles.addElement(h1_style)

    # Heading 2 style
    h2_style = Style(name="CustomH2", family="paragraph")
    h2_style.addElement(ParagraphProperties(margintop="12pt", marginbottom="6pt"))
    h2_style.addElement(TextProperties(fontsize="13pt", fontweight="bold", fontfamily="Liberation Sans", color="#2e7d32"))
    doc.styles.addElement(h2_style)

    # Heading 3 style
    h3_style = Style(name="CustomH3", family="paragraph")
    h3_style.addElement(ParagraphProperties(margintop="10pt", marginbottom="4pt"))
    h3_style.addElement(TextProperties(fontsize="11pt", fontweight="bold", fontfamily="Liberation Sans", color="#333333"))
    doc.styles.addElement(h3_style)

    # Body paragraph
    body_style = Style(name="CustomBody", family="paragraph")
    body_style.addElement(ParagraphProperties(marginbottom="6pt"))
    body_style.addElement(TextProperties(fontsize="10.5pt", fontfamily="Liberation Sans", color="#222222"))
    doc.styles.addElement(body_style)

    # Bullet / List paragraph
    list_style = Style(name="CustomList", family="paragraph")
    list_style.addElement(ParagraphProperties(marginleft="15pt", marginbottom="4pt"))
    list_style.addElement(TextProperties(fontsize="10pt", fontfamily="Liberation Sans", color="#222222"))
    doc.styles.addElement(list_style)

    # Table Header Cell style
    th_cell_style = Style(name="THCell", family="table-cell")
    th_cell_style.addElement(TableCellProperties(
        backgroundcolor="#e8f5e9",
        padding="6pt",
        border="0.5pt solid #81c784"
    ))
    doc.styles.addElement(th_cell_style)

    th_para_style = Style(name="THPara", family="paragraph")
    th_para_style.addElement(ParagraphProperties(textalign="left"))
    th_para_style.addElement(TextProperties(fontsize="9.5pt", fontweight="bold", fontfamily="Liberation Sans", color="#1b5e20"))
    doc.styles.addElement(th_para_style)

    # Table Body Cell style
    td_cell_style = Style(name="TDCell", family="table-cell")
    td_cell_style.addElement(TableCellProperties(
        padding="5pt",
        border="0.5pt solid #cccccc"
    ))
    doc.styles.addElement(td_cell_style)

    td_para_style = Style(name="TDPara", family="paragraph")
    td_para_style.addElement(ParagraphProperties(marginbottom="0pt"))
    td_para_style.addElement(TextProperties(fontsize="9.5pt", fontfamily="Liberation Sans", color="#222222"))
    doc.styles.addElement(td_para_style)

    # Helper function to add table
    def add_table(headers, rows):
        table = Table()
        for _ in headers:
            col = TableColumn()
            table.addElement(col)
        
        # Header Row
        header_row = TableRow()
        for h_text in headers:
            cell = TableCell(stylename=th_cell_style)
            p = P(stylename=th_para_style, text=h_text)
            cell.addElement(p)
            header_row.addElement(cell)
        table.addElement(header_row)

        # Data Rows
        for r_data in rows:
            row = TableRow()
            for c_text in r_data:
                cell = TableCell(stylename=td_cell_style)
                lines = str(c_text).split("\n")
                for line in lines:
                    p = P(stylename=td_para_style, text=line)
                    cell.addElement(p)
                row.addElement(cell)
            table.addElement(row)
        doc.text.addElement(table)

    # --- COVER / FRONT PAGE ---
    doc.text.addElement(P(stylename=title_style, text="CPE 334 — Project Deliverable 1"))
    doc.text.addElement(P(stylename=subtitle_style, text="Engineering Baseline + Working Sprint 1\nTheme 4: E-Commerce or Ordering System (UniMerch Campus Store)"))

    meta_text = (
        "Team: Clément Dominique Delrieu (Student ID: 69540460016) & Ba (Student ID: ...)\n"
        "Repository: https://github.com/ShrekIsLife1/AttalHaterAccount\n"
        "Submitted Release: Tag <TAG> — Commit <RELEASE_COMMIT>\n"
        "Date: November 2026"
    )
    doc.text.addElement(P(stylename=meta_style, text=meta_text))

    # --- NAVIGATION TABLE ---
    doc.text.addElement(P(stylename=h1_style, text="Navigation Table"))
    nav_headers = ["Part", "Pages", "Main IDs", "Execution Evidence"]
    nav_rows = [
        ["Part A — SRS and Scope", "Pages 2–4", "FR-01…FR-13, BR-01…BR-08, NFR-01…NFR-06", "—"],
        ["Part B — Feature Inventory & Traceability", "Page 5", "F-01…F-10", "—"],
        ["Part C — System-Level SDS", "Pages 6–9", "Architecture, ER Diagram, Roles, API", "—"],
        ["Part D — Three-Sprint Plan", "Page 10", "Sprint 1/2/3 features & feasibility", "—"],
        ["Part E — Sprint 1 Contracts", "Pages 11–16", "F-01…F-05, AC-01…AC-20, STS (TEST-01…26)", "Part F"],
        ["Part F — Working Sprint 1 & Verification", "Pages 17–28", "Demos S1…S10, Test runs, PR history", "Evidence screenshots"]
    ]
    add_table(nav_headers, nav_rows)
    doc.text.addElement(P(stylename=body_style, text=""))

    # --- PART A: SRS AND PRODUCT SCOPE ---
    doc.text.addElement(P(stylename=h1_style, text="Part A — SRS and Product Scope"))

    doc.text.addElement(P(stylename=h2_style, text="A.1 Problem Statement & Context"))
    doc.text.addElement(P(
        stylename=body_style,
        text="The UniMerch Campus Store is an on-campus merchandise shop serving university students, faculty, alumni, and administrative staff. The shop offers branded merchandise, apparel (hoodies, t-shirts), stationery (notebooks, pens), and everyday campus accessories (water bottles, tote bags, mugs)."
    ))
    doc.text.addElement(P(
        stylename=body_style,
        text="Currently, the physical store suffers from substantial operational bottlenecks: (1) Long Counter Queues during semester openings and events; (2) Stock Inconsistencies due to untracked manual inventory; (3) Manual Order Processing on paper tickets; and (4) Pricing Discrepancies between printed tags and updated prices."
    ))
    doc.text.addElement(P(
        stylename=body_style,
        text="Solution Vision: A robust web-based ordering application that allows customers to view authoritative catalog items with live availability, place multi-item orders with server-validated pricing, and track their order status. Store operators manage an organized incoming queue, review order lines, and progress orders through transparent fulfillment stages."
    ))

    doc.text.addElement(P(stylename=h2_style, text="A.2 Actors and Responsibilities"))
    actor_headers = ["Actor", "Description", "Core Responsibilities"]
    actor_rows = [
        [
            "Customer",
            "Enrolled student or staff member purchasing merchandise",
            "- Authenticate securely via email and password.\n- Browse product catalog with authoritative prices and stock availability.\n- Assemble and submit multi-line orders.\n- View own order history and track order status.\n- Cannot modify catalog, cannot accept orders, cannot view other customers' orders."
        ],
        [
            "Operator",
            "Campus store staff member managing fulfillment and catalog",
            "- Authenticate securely via email and password.\n- View incoming orders queue (PLACED) sorted chronologically.\n- Accept incoming orders (PLACED -> ACCEPTED) with recorded timestamp and operator identity.\n- Progress order fulfillment in subsequent sprints (PREPARING -> READY -> COMPLETED).\n- Manage catalog items, pricing, and stock levels (Sprint 2).\n- Cannot place orders as an operator; accesses customer orders within store scope."
        ]
    ]
    add_table(actor_headers, actor_rows)
    doc.text.addElement(P(stylename=body_style, text=""))

    doc.text.addElement(P(stylename=h2_style, text="A.3 Product Scope and Explicit Exclusions"))
    doc.text.addElement(P(
        stylename=body_style,
        text="In Scope: Sprint 1 implements session-based authentication (CUSTOMER, OPERATOR roles), read-only product catalog with live availability badges, multi-line order placement with server-side authoritative pricing, inventory check and atomic decrement, customer order history and detail view, operator incoming queue and accept transition (PLACED -> ACCEPTED), and persistent PostgreSQL storage with idempotent seed data. Sprints 2 & 3 add catalog management, order cancellation/rejection, full fulfillment lifecycle, simulated payment, analytics, and search/filtering."
    ))
    doc.text.addElement(P(
        stylename=body_style,
        text="Explicit Exclusions: (1) No Real Payment Gateways — live payment providers (Stripe, PayPal, promptpay) are strictly excluded; simulated payment states are used. (2) No External Logistics APIs — pickup occurs on-site at the UniMerch counter. (3) No External Messaging Providers — no SMS/email gateways; all status updates remain in-app. (4) No Self-Registration or Password Recovery in Sprint 1 — seeded accounts with pre-hashed credentials are used."
    ))

    doc.text.addElement(P(stylename=h2_style, text="A.4 Functional Requirements (FR)"))
    fr_list = [
        "FR-01 (User Authentication): User logs in with email and password. System creates a secure session and returns profile (id, name, role). Password hash is never returned.",
        "FR-02 (User Logout): Authenticated user logs out. Session is invalidated server-side and cookie cleared. Old session is rejected on subsequent calls.",
        "FR-03 (Catalog Browsing): Authenticated users retrieve products with name, description, price (minor units), and availability (inStock / unavailable).",
        "FR-04 (Order Placement): Customer submits order (1 to N lines). Server authoritatively computes total, checks stock, snapshots prices, decrements stock, and saves order as PLACED atomically.",
        "FR-05 (Customer Order History & Detail): Customer lists their own placed orders and opens any of their own orders to inspect full details.",
        "FR-06 (Operator Incoming Orders): Operator lists all incoming orders with status = PLACED ordered chronologically (oldest first).",
        "FR-07 (Operator Order Acceptance): Operator accepts a PLACED order. Backend transitions status to ACCEPTED, recording acceptedAt and acceptedByOperatorId.",
        "FR-08 (Operator Catalog Management - Sprint 2): Operator creates, updates products, modifies stock, and toggles active status.",
        "FR-09 (Order Cancellation and Rejection - Sprint 2): Customer cancels PLACED order; operator rejects PLACED order with reason note.",
        "FR-10 (Extended Fulfillment Transitions - Sprint 2): Operator advances order: ACCEPTED -> PREPARING -> READY -> COMPLETED.",
        "FR-11 (Simulated Payment Processing - Sprint 2): Customer executes simulated payment; transitions payment status to PAID with synthetic reference.",
        "FR-12 (Sales and Order Analytics - Sprint 3): Operator views aggregate sales figures, revenue, status distribution, and item turnover.",
        "FR-13 (Order Search and Filtering - Sprint 3): Users search and filter orders by status, date range, or customer email."
    ]
    for fr in fr_list:
        doc.text.addElement(P(stylename=list_style, text="• " + fr))

    doc.text.addElement(P(stylename=h2_style, text="A.5 Business Rules (BR)"))
    br_list = [
        "BR-01 (Authoritative Server Pricing): Order totals and line totals are computed strictly on the backend from authoritative database prices. Client-sent totals/prices are completely ignored.",
        "BR-02 (Quantity Boundaries): Quantity per line must be an integer between 1 and MAX_QTY_PER_LINE (10). Values <= 0, non-integers, missing, or > 10 are rejected with HTTP 400.",
        "BR-03 (Inventory Availability & Atomicity): Product must be active (isActive=true) and stockQuantity >= quantity. Duplicate items in one order are rejected (HTTP 400). If any line fails, entire order fails, stock is unchanged (atomic transaction).",
        "BR-04 (Price Snapshot Immutability): OrderItem.unitPriceAtOrder stores unit price at order creation. Later catalog price updates never alter historical orders or totals.",
        "BR-05 (Customer Ownership & Privacy): Customer can only access their own orders (Order.customerId == session.userId). Cross-customer order access returns HTTP 404 without data leak.",
        "BR-06 (Strict State Transition Lifecycle): Sprint 1 allows only PLACED -> ACCEPTED by Operator. Accepting an already ACCEPTED order returns HTTP 409 Conflict with state unchanged.",
        "BR-07 (Secure Credential Storage): Passwords must never be stored in plaintext. They are hashed using salted bcrypt (work factor >= 10).",
        "BR-08 (Operator Scope and Role Restrictions): Only users with role OPERATOR can list incoming orders or accept them. Customers calling operator endpoints receive HTTP 403 Forbidden."
    ]
    for br in br_list:
        doc.text.addElement(P(stylename=list_style, text="• " + br))

    doc.text.addElement(P(stylename=h2_style, text="A.6 Non-Functional Requirements (NFR)"))
    nfr_headers = ["NFR ID", "Requirement Statement", "Measurable Target", "Verification Method", "Sprint"]
    nfr_rows = [
        ["NFR-01", "Authentication & Role Authorization Enforcement", "100% of protected routes reject unauth with 401; wrong role with 403; cross-user order with 404.", "Automated API tests (auth.api.test.ts, orders-access.api.test.ts)", "Sprint 1"],
        ["NFR-02", "Relational Data Persistence Across Restarts", "All records (users, products, orders, items, sessions) persist across application restart.", "Automated persistence test (persistence.api.test.ts)", "Sprint 1"],
        ["NFR-03", "Seed Reproducibility & Idempotence", "Consecutive seed executions create 0 duplicate records and 0 constraint errors.", "Scripted test running seed consecutively", "Sprint 1"],
        ["NFR-04", "Fresh Clone Reproducibility", "Fresh clone install, migrate, seed, test, and run succeeds in < 5 minutes following only README.", "Clean-room scripted check on fresh clone", "Sprint 1"],
        ["NFR-05", "Order Placement Latency", "Valid 10-line order creation responds with HTTP 201 in < 1000 ms on dev machine.", "Automated benchmark test under test DB", "Sprint 3"],
        ["NFR-06", "Responsive User Interface", "Web UI renders without horizontal scroll on screen widths from 375px to 1920px.", "Visual inspection & Playwright viewport checks", "Sprint 3"]
    ]
    add_table(nfr_headers, nfr_rows)
    doc.text.addElement(P(stylename=body_style, text=""))

    doc.text.addElement(P(stylename=h2_style, text="A.7 Assumptions, Frozen Design Decisions, and Open Questions"))
    dec_headers = ["Topic / Decision", "Chosen Resolution & Justification", "Status"]
    dec_rows = [
        ["Domain Context", "Campus merchandise store (UniMerch): single-store catalog, single fulfillment team, student/staff customers.", "Frozen"],
        ["User Roles", "Exactly two roles: CUSTOMER and OPERATOR (one role per account). Simplifies RBAC while fulfilling rubric.", "Frozen"],
        ["Monetary Representation", "All currency values (priceMinor, totalMinor, unitPriceAtOrder) stored as integers in minor units (satang/cents; 100 minor = 1 THB). Float arithmetic strictly prohibited.", "Frozen"],
        ["Sprint 1 Order Statuses", "Exactly two statuses in Sprint 1: PLACED and ACCEPTED. Later sprints introduce REJECTED, CANCELLED, PREPARING, READY, COMPLETED.", "Frozen"],
        ["Order Lines & Limits", "1 to N lines per order. quantity integer between 1 and MAX_QTY_PER_LINE = 10. Duplicate items in one order rejected (HTTP 400).", "Frozen"],
        ["Inventory Management", "Product.isActive (boolean) and stockQuantity (int >= 0). Decremented atomically in same DB transaction. If insufficient, whole order fails.", "Frozen"],
        ["Authoritative Pricing", "Server re-queries DB for prices at order creation. Client-sent prices/totals are discarded.", "Frozen"],
        ["Price Snapshot", "OrderItem.unitPriceAtOrder records unit price at order placement. Future catalog price changes never mutate historical orders.", "Frozen"],
        ["Authentication Mechanism", "Server-side Session table with secure random token in HttpOnly SameSite=Lax cookie. 8h expiry. Logout invalidates in DB.", "Frozen"],
        ["Error Handling Policy", "Generic HTTP 401 for invalid credentials/session/inactive user (no user enumeration). HTTP 403 for wrong role. HTTP 404 for cross-customer order. HTTP 400 for input errors. HTTP 409 for state conflicts.", "Frozen"],
        ["Seed Data Specification", "Idempotent seed: >=3 customers, >=2 operators, >=8 products (incl. >=1 inactive and >=1 with stock 0). Passwords loaded from env, never in Git.", "Frozen"]
    ]
    add_table(dec_headers, dec_rows)
    doc.text.addElement(P(stylename=body_style, text=""))

    # --- PLACEHOLDERS FOR PARTS B TO F ---
    doc.text.addElement(P(stylename=h1_style, text="Part B — Feature Inventory and Traceability (Issue #2)"))
    doc.text.addElement(P(stylename=body_style, text="[Will be filled by Issue #2: Feature inventory table, Requirement-to-feature-to-sprint traceability matrix, Gaps & approved changes section]"))

    doc.text.addElement(P(stylename=h1_style, text="Part C — System-Level SDS (Issue #3)"))
    doc.text.addElement(P(stylename=body_style, text="[Will be filled by Issue #3: Architecture diagram, Entity-Relationship (ER) diagram, UI/API conventions, Role/permission matrix, Configuration & deployment plan]"))

    doc.text.addElement(P(stylename=h1_style, text="Part D — Three-Sprint Plan (Issue #4)"))
    doc.text.addElement(P(stylename=body_style, text="[Will be filled by Issue #4: Three-sprint plan table, goals, feature allocations, dependencies, and Sprint 1 feasibility justification]"))

    doc.text.addElement(P(stylename=h1_style, text="Part E — Sprint 1 Engineering Contracts (Issue #5)"))
    doc.text.addElement(P(stylename=body_style, text="[Will be filled by Issue #5: Feature-level SDS, UI/API/Data contracts for F-01 to F-05, Acceptance Criteria, Software Test Specification (STS), and Definition of Done]"))

    doc.text.addElement(P(stylename=h1_style, text="Part F — Working Sprint 1 and Verification (Issues #6 to #15)"))
    doc.text.addElement(P(stylename=body_style, text="[Will be filled progressively by Issues #6 to #15: Program demonstrations S1 to S10 with screenshots, automated test results table, test excerpts, TDD evidence, Git history, contributions, and AI-use declaration]"))

    # Save document
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    print(f"Generated {output_path} successfully!")

if __name__ == "__main__":
    create_deliverable_odt()
