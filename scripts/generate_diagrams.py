#!/usr/bin/env python3
"""
Generate Architecture and ER diagrams as crisp PNG images in docs/deliverable-1/evidence/
"""
import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("docs/deliverable-1/evidence", exist_ok=True)

def get_font(size=14, bold=False):
    # Try standard system fonts
    font_paths = [
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in font_paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def draw_architecture_diagram():
    w, h = 950, 520
    im = Image.new("RGB", (w, h), "#fcfcfc")
    draw = ImageDraw.Draw(im)

    f_title = get_font(18, bold=True)
    f_box_title = get_font(15, bold=True)
    f_body = get_font(12, bold=False)
    f_sub = get_font(11, bold=False)

    # Title Banner
    draw.rectangle([20, 15, w - 20, 60], fill="#e8f5e9", outline="#2e7d32", width=2)
    draw.text((w // 2, 37), "UniMerch Campus Store — Three-Tier System Architecture", fill="#1b5e20", font=f_title, anchor="mm")

    # Tier 1: Client
    draw.rounded_rectangle([40, 85, w - 40, 175], radius=8, fill="#e3f2fd", outline="#1976d2", width=2)
    draw.text((60, 100), "Presentation Tier (Web Client)", fill="#0d47a1", font=f_box_title)
    draw.text((60, 125), "• React 18 SPA + Vite + TypeScript | Bootstrap 5 Responsive Layout", fill="#333333", font=f_body)
    draw.text((60, 145), "• Role-based Navigation (Customer: Catalog, Cart, My Orders | Operator: Incoming Queue, Accept)", fill="#555555", font=f_sub)

    # Arrow 1: Client -> Server
    draw.line([(w // 2, 175), (w // 2, 225)], fill="#1976d2", width=3)
    draw.polygon([(w // 2 - 6, 220), (w // 2 + 6, 220), (w // 2, 228)], fill="#1976d2")
    draw.text((w // 2 + 15, 200), "HTTPS / REST JSON (HttpOnly SameSite Session Cookie)", fill="#1565c0", font=f_body)

    # Tier 2: Server
    draw.rounded_rectangle([40, 230, w - 40, 345], radius=8, fill="#f1f8e9", outline="#388e3c", width=2)
    draw.text((60, 245), "Application & API Tier (Node.js / Express)", fill="#1b5e20", font=f_box_title)
    draw.text((60, 270), "• Security Middleware: requireAuth, requireRole (CUSTOMER / OPERATOR RBAC)", fill="#333333", font=f_body)
    draw.text((60, 290), "• Domain Engine: Authoritative server pricing, stock verification, atomic state transitions", fill="#333333", font=f_body)
    draw.text((60, 310), "• Zod Input Validation & Error Normalization (Standard safe error envelope: 400/401/403/404/409)", fill="#555555", font=f_sub)

    # Arrow 2: Server -> DB
    draw.line([(w // 2, 345), (w // 2, 395)], fill="#388e3c", width=3)
    draw.polygon([(w // 2 - 6, 390), (w // 2 + 6, 390), (w // 2, 398)], fill="#388e3c")
    draw.text((w // 2 + 15, 370), "Prisma ORM (SQL Queries & ACID $transactions)", fill="#2e7d32", font=f_body)

    # Tier 3: Database
    draw.rounded_rectangle([40, 400, w - 40, 495], radius=8, fill="#fff3e0", outline="#f57c00", width=2)
    draw.text((60, 415), "Data Tier (PostgreSQL 16 Database)", fill="#e65100", font=f_box_title)
    draw.text((60, 440), "• Relational Persistence: User, Session, Product, Order, OrderItem tables", fill="#333333", font=f_body)
    draw.text((60, 460), "• Constraints: Unique email, foreign keys, CHECK quantity > 0, CHECK stock >= 0, minor units", fill="#555555", font=f_sub)

    out_path = "docs/deliverable-1/evidence/issue-03_architecture-diagram.png"
    im.save(out_path, quality=95)
    print(f"Saved {out_path}")

def draw_er_diagram():
    w, h = 950, 620
    im = Image.new("RGB", (w, h), "#fcfcfc")
    draw = ImageDraw.Draw(im)

    f_title = get_font(18, bold=True)
    f_box_title = get_font(13, bold=True)
    f_body = get_font(11, bold=False)

    # Title
    draw.rectangle([20, 15, w - 20, 55], fill="#e8f5e9", outline="#2e7d32", width=2)
    draw.text((w // 2, 35), "UniMerch Campus Store — Entity-Relationship (ER) Schema", fill="#1b5e20", font=f_title, anchor="mm")

    # Entity Boxes:
    # 1. User
    draw.rounded_rectangle([30, 80, 280, 280], radius=6, fill="#ffffff", outline="#1976d2", width=2)
    draw.rectangle([30, 80, 280, 110], fill="#e3f2fd")
    draw.text((40, 95), "User", fill="#0d47a1", font=f_box_title, anchor="lm")
    user_fields = [
        "+ id: Int (PK)",
        "+ email: String (Unique)",
        "- passwordHash: String",
        "+ name: String",
        "+ role: Role (CUSTOMER|OPERATOR)",
        "+ isActive: Boolean",
        "+ createdAt: DateTime",
        "+ updatedAt: DateTime"
    ]
    y = 125
    for f in user_fields:
        draw.text((40, y), f, fill="#333333", font=f_body)
        y += 18

    # 2. Session
    draw.rounded_rectangle([30, 330, 280, 490], radius=6, fill="#ffffff", outline="#7b1fa2", width=2)
    draw.rectangle([30, 330, 280, 360], fill="#f3e5f5")
    draw.text((40, 345), "Session", fill="#4a148c", font=f_box_title, anchor="lm")
    session_fields = [
        "+ id: String (PK, UUID)",
        "+ userId: Int (FK -> User.id)",
        "+ tokenHash: String (Unique)",
        "+ expiresAt: DateTime",
        "+ createdAt: DateTime"
    ]
    y = 375
    for f in session_fields:
        draw.text((40, y), f, fill="#333333", font=f_body)
        y += 18

    # 3. Product
    draw.rounded_rectangle([670, 80, 920, 280], radius=6, fill="#ffffff", outline="#388e3c", width=2)
    draw.rectangle([670, 80, 920, 110], fill="#e8f5e9")
    draw.text((680, 95), "Product", fill="#1b5e20", font=f_box_title, anchor="lm")
    prod_fields = [
        "+ id: Int (PK)",
        "+ name: String",
        "+ description: String?",
        "+ priceMinor: Int (CHECK >= 0)",
        "+ stockQuantity: Int (CHECK >= 0)",
        "+ isActive: Boolean",
        "+ createdAt: DateTime",
        "+ updatedAt: DateTime"
    ]
    y = 125
    for f in prod_fields:
        draw.text((680, y), f, fill="#333333", font=f_body)
        y += 18

    # 4. Order
    draw.rounded_rectangle([350, 80, 600, 290], radius=6, fill="#ffffff", outline="#d32f2f", width=2)
    draw.rectangle([350, 80, 600, 110], fill="#ffebee")
    draw.text((360, 95), "Order", fill="#b71c1c", font=f_box_title, anchor="lm")
    order_fields = [
        "+ id: Int (PK)",
        "+ customerId: Int (FK -> User.id)",
        "+ status: OrderStatus (PLACED|...)",
        "+ totalMinor: Int (CHECK >= 0)",
        "+ createdAt: DateTime",
        "+ acceptedAt: DateTime?",
        "+ acceptedByOperatorId: Int? (FK)"
    ]
    y = 125
    for f in order_fields:
        draw.text((360, y), f, fill="#333333", font=f_body)
        y += 18

    # 5. OrderItem
    draw.rounded_rectangle([350, 360, 600, 530], radius=6, fill="#ffffff", outline="#f57c00", width=2)
    draw.rectangle([350, 360, 600, 390], fill="#fff3e0")
    draw.text((360, 375), "OrderItem", fill="#e65100", font=f_box_title, anchor="lm")
    item_fields = [
        "+ id: Int (PK)",
        "+ orderId: Int (FK -> Order.id)",
        "+ productId: Int (FK -> Product.id)",
        "+ quantity: Int (CHECK 1..10)",
        "+ unitPriceAtOrder: Int (Snapshot)"
    ]
    y = 405
    for f in item_fields:
        draw.text((360, y), f, fill="#333333", font=f_body)
        y += 18

    # Relationships Lines & Text
    # User -> Session (1:N)
    draw.line([(155, 280), (155, 330)], fill="#7b1fa2", width=2)
    draw.text((165, 305), "1 : N (Cascade)", fill="#7b1fa2", font=f_body, anchor="lm")

    # User -> Order (1:N customerId)
    draw.line([(280, 140), (350, 140)], fill="#1976d2", width=2)
    draw.text((315, 125), "1 : N", fill="#1976d2", font=f_body, anchor="mm")

    # Order -> OrderItem (1:N)
    draw.line([(475, 290), (475, 360)], fill="#d32f2f", width=2)
    draw.text((485, 325), "1 : N (Cascade)", fill="#d32f2f", font=f_body, anchor="lm")

    # Product -> OrderItem (1:N)
    draw.line([(670, 200), (630, 200), (630, 440), (600, 440)], fill="#388e3c", width=2)
    draw.text((635, 320), "1 : N", fill="#388e3c", font=f_body, anchor="lm")

    # Summary note
    draw.rectangle([30, 560, w - 30, 605], fill="#fafafa", outline="#cccccc", width=1)
    draw.text((w // 2, 582), "Integrity: Foreign keys enforced with Prisma Cascade Deletes on Sessions & Items. CHECK constraints on stocks & quantities.", fill="#555555", font=f_body, anchor="mm")

    out_path = "docs/deliverable-1/evidence/issue-03_er-diagram.png"
    im.save(out_path, quality=95)
    print(f"Saved {out_path}")

if __name__ == "__main__":
    draw_architecture_diagram()
    draw_er_diagram()
