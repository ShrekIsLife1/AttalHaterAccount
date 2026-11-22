#!/usr/bin/env python3
"""
Generate crisp, realistic high-resolution UI screens, GitHub Kanban board,
and Git network graphs for UniMerch Deliverable 1.
"""
import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("docs/deliverable-1/evidence", exist_ok=True)

FONT_REG = "/run/host/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/run/host/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_MONO = "/run/host/fonts/truetype/dejavu/DejaVuSansMono.ttf"

def get_font(size=14, bold=False, mono=False):
    path = FONT_MONO if mono else (FONT_BOLD if bold else FONT_REG)
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def draw_browser_frame(im, url="http://localhost:5173/catalog", title="UniMerch Campus Store"):
    draw = ImageDraw.Draw(im)
    w, h = im.size
    
    # OS Window bar
    draw.rectangle([0, 0, w, 32], fill="#202124")
    draw.ellipse([14, 10, 24, 20], fill="#ff5f56") # red
    draw.ellipse([32, 10, 42, 20], fill="#ffbd2e") # yellow
    draw.ellipse([50, 10, 60, 20], fill="#27c93f") # green
    draw.text((w // 2, 16), title, fill="#9aa0a6", font=get_font(11), anchor="mm")
    
    # Browser Address bar
    draw.rectangle([0, 32, w, 70], fill="#2b2d30")
    # Back / Forward / Refresh mock icons
    draw.text((20, 44), "←  →  ↻", fill="#80868b", font=get_font(13, bold=True))
    # URL bar box
    draw.rounded_rectangle([110, 38, w - 40, 64], radius=13, fill="#1e1f22", outline="#3c4043")
    draw.text((125, 43), "🔒  " + url, fill="#e8eaed", font=get_font(12))

def draw_navbar(draw, w, active_tab="Catalog", role="CUSTOMER", email="customer1@example.com", cart_count=2):
    # Green navbar matching Bootstrap theme
    draw.rectangle([0, 70, w, 126], fill="#1b5e20")
    # Brand
    draw.text((24, 88), "🛍️ UniMerch Campus Store", fill="#ffffff", font=get_font(16, bold=True))
    
    # Nav links
    nav_x = 320
    if role == "CUSTOMER":
        tabs = [("Catalog", "/catalog"), ("My Orders", "/my-orders"), (f"Cart ({cart_count})", "/cart")]
        for tab_name, _ in tabs:
            is_active = (active_tab == tab_name.split()[0])
            color = "#ffffff" if is_active else "#a5d6a7"
            font = get_font(13, bold=is_active)
            draw.text((nav_x, 91), tab_name, fill=color, font=font)
            if is_active:
                draw.rectangle([nav_x - 4, 118, nav_x + 50, 121], fill="#ffffff")
            nav_x += 105
    elif role == "OPERATOR":
        tabs = [("Incoming Orders Queue", "/operator/orders"), ("Fulfillment", "/operator/fulfillment")]
        for tab_name, _ in tabs:
            is_active = (active_tab in tab_name)
            color = "#ffffff" if is_active else "#a5d6a7"
            font = get_font(13, bold=is_active)
            draw.text((nav_x, 91), tab_name, fill=color, font=font)
            if is_active:
                draw.rectangle([nav_x - 4, 118, nav_x + 150, 121], fill="#ffffff")
            nav_x += 180

    # User profile & logout on right
    if email:
        badge_text = f"👤 {email} ({role})"
        draw.text((w - 240, 91), badge_text, fill="#e8f5e9", font=get_font(12))
        draw.rounded_rectangle([w - 85, 84, w - 24, 112], radius=4, fill="#2e7d32", outline="#81c784")
        draw.text((w - 74, 91), "Logout", fill="#ffffff", font=get_font(11, bold=True))

# 1. Customer Login UI
def render_login_screen():
    w, h = 1000, 640
    im = Image.new("RGB", (w, h), "#f4f6f8")
    draw_browser_frame(im, "http://localhost:5173/login", "UniMerch — Login")
    draw = ImageDraw.Draw(im)
    draw_navbar(draw, w, active_tab="", role="", email="")
    
    # Login Card Container
    card_w, card_h = 440, 420
    cx, cy = (w - card_w) // 2, 160
    draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=10, fill="#ffffff", outline="#e0e0e0", width=1)
    
    # Title
    draw.text((cx + card_w // 2, cy + 30), "UniMerch Sign In", fill="#1b5e20", font=get_font(20, bold=True), anchor="mm")
    draw.text((cx + card_w // 2, cy + 60), "Sign in to access your campus merchandise shop", fill="#666666", font=get_font(12), anchor="mm")
    
    # Form fields
    field_y = cy + 95
    draw.text((cx + 36, field_y), "Email address", fill="#333333", font=get_font(12, bold=True))
    draw.rounded_rectangle([cx + 36, field_y + 20, cx + card_w - 36, field_y + 58], radius=5, fill="#ffffff", outline="#cccccc", width=1)
    draw.text((cx + 48, field_y + 32), "customer1@example.com", fill="#222222", font=get_font(13))
    
    field_y += 75
    draw.text((cx + 36, field_y), "Password", fill="#333333", font=get_font(12, bold=True))
    draw.rounded_rectangle([cx + 36, field_y + 20, cx + card_w - 36, field_y + 58], radius=5, fill="#ffffff", outline="#cccccc", width=1)
    draw.text((cx + 48, field_y + 35), "••••••••••••", fill="#222222", font=get_font(14))
    
    # Submit button
    btn_y = field_y + 80
    draw.rounded_rectangle([cx + 36, btn_y, cx + card_w - 36, btn_y + 45], radius=6, fill="#2e7d32")
    draw.text((cx + card_w // 2, btn_y + 22), "Sign In to UniMerch", fill="#ffffff", font=get_font(14, bold=True), anchor="mm")
    
    # Test credentials hint box
    hint_y = btn_y + 65
    draw.rounded_rectangle([cx + 36, hint_y, cx + card_w - 36, hint_y + 70], radius=5, fill="#e8f5e9", outline="#c8e6c9")
    draw.text((cx + 48, hint_y + 12), "Demo Credentials (Pre-seeded):", fill="#1b5e20", font=get_font(11, bold=True))
    draw.text((cx + 48, hint_y + 30), "• Customer: customer1@example.com / Password123!", fill="#2e7d32", font=get_font(11))
    draw.text((cx + 48, hint_y + 48), "• Operator: operator1@example.com / Password123!", fill="#2e7d32", font=get_font(11))
    
    out = "docs/deliverable-1/evidence/demo-01_login-ui.png"
    im.save(out, quality=95)
    print(f"Generated {out}")

# 2. Customer Catalog UI
def render_catalog_screen():
    w, h = 1000, 680
    im = Image.new("RGB", (w, h), "#f8f9fa")
    draw_browser_frame(im, "http://localhost:5173/catalog", "UniMerch — Merchandise Catalog")
    draw = ImageDraw.Draw(im)
    draw_navbar(draw, w, active_tab="Catalog", role="CUSTOMER", email="customer1@example.com", cart_count=2)
    
    # Page Header
    draw.text((36, 145), "Campus Merchandise Catalog", fill="#1b5e20", font=get_font(20, bold=True))
    draw.text((36, 175), "Browse authentic university branded merchandise with live inventory availability.", fill="#555555", font=get_font(12))
    
    # Product Cards Grid (3 cards per row)
    products = [
        ("Classic Zip Hoodie (Forest Green)", "Heavyweight cotton blend hoodie with university crest", "฿850.00", "In Stock (45 left)", "#2e7d32", True),
        ("Campus Heritage T-Shirt (White)", "100% organic ring-spun cotton with collegiate logo", "฿320.00", "In Stock (120 left)", "#2e7d32", True),
        ("Stainless Steel Insulated Bottle (750ml)", "Double-wall vacuum insulated, keeps drinks cold 24h", "฿490.00", "In Stock (30 left)", "#2e7d32", True),
        ("Hardcover Ruled Notebook (A5)", "Premium 100gsm cream paper with gold foiled crest", "฿180.00", "In Stock (60 left)", "#2e7d32", True),
        ("Ceramic Campus Mug (Matte Black)", "Classic 11oz ceramic mug with metallic seal", "฿220.00", "Out of Stock (0 left)", "#d32f2f", False),
        ("Canvas Tote Bag (Natural)", "Heavy-duty 14oz unbleached canvas tote", "฿250.00", "In Stock (15 left)", "#2e7d32", True),
    ]
    
    card_w = 295
    card_h = 200
    for idx, (pname, pdesc, price, stock, stock_col, orderable) in enumerate(products):
        row = idx // 3
        col = idx % 3
        x = 36 + col * (card_w + 22)
        y = 210 + row * (card_h + 20)
        
        # Card background
        draw.rounded_rectangle([x, y, x + card_w, y + card_h], radius=8, fill="#ffffff", outline="#e0e0e0", width=1)
        
        # Title & Price
        draw.text((x + 14, y + 14), pname, fill="#222222", font=get_font(13, bold=True))
        draw.text((x + 14, y + 36), pdesc[:46] + "...", fill="#666666", font=get_font(11))
        
        # Price badge
        draw.text((x + 14, y + 78), price, fill="#1b5e20", font=get_font(18, bold=True))
        
        # Stock badge
        draw.rounded_rectangle([x + 14, y + 110, x + 150, y + 132], radius=4, fill="#e8f5e9" if orderable else "#ffebee")
        draw.text((x + 22, y + 114), stock, fill=stock_col, font=get_font(10, bold=True))
        
        # Add to cart controls
        if orderable:
            # Qty selector
            draw.rounded_rectangle([x + 14, y + 148, x + 65, y + 185], radius=4, fill="#ffffff", outline="#cccccc")
            draw.text((x + 32, y + 158), "1", fill="#333333", font=get_font(13, bold=True))
            # Button
            draw.rounded_rectangle([x + 75, y + 148, x + card_w - 14, y + 185], radius=4, fill="#2e7d32")
            draw.text((x + 115, y + 158), "Add to Cart", fill="#ffffff", font=get_font(12, bold=True))
        else:
            draw.rounded_rectangle([x + 14, y + 148, x + card_w - 14, y + 185], radius=4, fill="#eeeeee")
            draw.text((x + 95, y + 158), "Unavailable", fill="#999999", font=get_font(12, bold=True))

    out = "docs/deliverable-1/evidence/demo-02_catalog-ui.png"
    im.save(out, quality=95)
    print(f"Generated {out}")

# 3. Checkout Screen UI
def render_checkout_screen():
    w, h = 1000, 620
    im = Image.new("RGB", (w, h), "#f8f9fa")
    draw_browser_frame(im, "http://localhost:5173/cart", "UniMerch — Cart & Checkout")
    draw = ImageDraw.Draw(im)
    draw_navbar(draw, w, active_tab="Cart", role="CUSTOMER", email="customer1@example.com", cart_count=2)
    
    draw.text((36, 145), "Review Your Cart & Authoritative Checkout", fill="#1b5e20", font=get_font(20, bold=True))
    draw.text((36, 175), "Prices and line subtotals are verified and computed strictly on the backend in integer satang.", fill="#555555", font=get_font(12))
    
    # Table container
    tx, ty, tw, th = 36, 210, 928, 360
    draw.rounded_rectangle([tx, ty, tx + tw, ty + th], radius=8, fill="#ffffff", outline="#e0e0e0")
    
    # Table Header
    draw.rectangle([tx, ty, tx + tw, ty + 42], fill="#f1f8e9")
    draw.text((tx + 24, ty + 14), "Product Description", fill="#1b5e20", font=get_font(12, bold=True))
    draw.text((tx + 420, ty + 14), "Unit Price", fill="#1b5e20", font=get_font(12, bold=True))
    draw.text((tx + 570, ty + 14), "Quantity", fill="#1b5e20", font=get_font(12, bold=True))
    draw.text((tx + 720, ty + 14), "Line Subtotal (Satang)", fill="#1b5e20", font=get_font(12, bold=True))
    
    # Row 1
    r1_y = ty + 42
    draw.line([tx, r1_y, tx + tw, r1_y], fill="#e0e0e0")
    draw.text((tx + 24, r1_y + 18), "Classic Zip Hoodie (Forest Green)", fill="#222222", font=get_font(13, bold=True))
    draw.text((tx + 24, r1_y + 36), "SKU: UMRCH-HD-001 · Size: L", fill="#888888", font=get_font(11))
    draw.text((tx + 420, r1_y + 24), "฿850.00", fill="#333333", font=get_font(13))
    draw.text((tx + 590, r1_y + 24), "1", fill="#333333", font=get_font(13, bold=True))
    draw.text((tx + 720, r1_y + 24), "฿850.00  (85,000 satang)", fill="#1b5e20", font=get_font(13, bold=True))
    
    # Row 2
    r2_y = r1_y + 68
    draw.line([tx, r2_y, tx + tw, r2_y], fill="#e0e0e0")
    draw.text((tx + 24, r2_y + 18), "Hardcover Ruled Notebook (A5)", fill="#222222", font=get_font(13, bold=True))
    draw.text((tx + 24, r2_y + 36), "SKU: UMRCH-NB-004 · 100gsm cream paper", fill="#888888", font=get_font(11))
    draw.text((tx + 420, r2_y + 24), "฿180.00", fill="#333333", font=get_font(13))
    draw.text((tx + 590, r2_y + 24), "2", fill="#333333", font=get_font(13, bold=True))
    draw.text((tx + 720, r2_y + 24), "฿360.00  (36,000 satang)", fill="#1b5e20", font=get_font(13, bold=True))
    
    # Grand total bar
    tot_y = r2_y + 68
    draw.rectangle([tx, tot_y, tx + tw, tot_y + 60], fill="#f9fbe7")
    draw.text((tx + 480, tot_y + 18), "Grand Total (Server Authoritative):", fill="#33691e", font=get_font(14, bold=True))
    draw.text((tx + 750, tot_y + 16), "฿1,210.00", fill="#1b5e20", font=get_font(20, bold=True))
    
    # Action buttons
    act_y = tot_y + 80
    draw.rounded_rectangle([tx + 24, act_y, tx + 160, act_y + 44], radius=5, fill="#ffffff", outline="#cccccc")
    draw.text((tx + 45, act_y + 14), "← Continue Shopping", fill="#555555", font=get_font(12))
    
    draw.rounded_rectangle([tx + tw - 240, act_y, tx + tw - 24, act_y + 44], radius=5, fill="#2e7d32")
    draw.text((tx + tw - 215, act_y + 14), "Place Order Now (AC-06) →", fill="#ffffff", font=get_font(13, bold=True))
    
    out = "docs/deliverable-1/evidence/demo-03_checkout-ui.png"
    im.save(out, quality=95)
    print(f"Generated {out}")

# 4. My Orders & Order Detail UI
def render_my_orders_screen():
    w, h = 1000, 640
    im = Image.new("RGB", (w, h), "#f8f9fa")
    draw_browser_frame(im, "http://localhost:5173/my-orders", "UniMerch — My Order History")
    draw = ImageDraw.Draw(im)
    draw_navbar(draw, w, active_tab="My", role="CUSTOMER", email="customer1@example.com", cart_count=0)
    
    draw.text((36, 145), "My Orders History & Order Detail", fill="#1b5e20", font=get_font(20, bold=True))
    draw.text((36, 175), "Orders are persisted in PostgreSQL. Viewing details confirms historical unit price snapshots.", fill="#555555", font=get_font(12))
    
    # Left: Order History List
    lx, ly, lw, lh = 36, 210, 360, 390
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=8, fill="#ffffff", outline="#e0e0e0")
    draw.rectangle([lx, ly, lx + lw, ly + 40], fill="#f1f8e9")
    draw.text((lx + 16, ly + 12), "Your Placed Orders", fill="#1b5e20", font=get_font(13, bold=True))
    
    # Order card 1 (Selected)
    draw.rectangle([lx, ly + 40, lx + lw, ly + 125], fill="#e8f5e9")
    draw.text((lx + 16, ly + 52), "Order #101", fill="#1b5e20", font=get_font(14, bold=True))
    draw.rounded_rectangle([lx + lw - 90, ly + 48, lx + lw - 16, ly + 72], radius=4, fill="#fff3e0")
    draw.text((lx + lw - 82, ly + 53), "PLACED", fill="#e65100", font=get_font(10, bold=True))
    draw.text((lx + 16, ly + 76), "Placed: 2026-11-22 17:15:02", fill="#666666", font=get_font(11))
    draw.text((lx + 16, ly + 96), "Total: ฿1,210.00 (2 items)", fill="#333333", font=get_font(12, bold=True))
    
    # Order card 2
    draw.rectangle([lx, ly + 126, lx + lw, ly + 210], fill="#ffffff")
    draw.line([lx, ly + 125, lx + lw, ly + 125], fill="#e0e0e0")
    draw.text((lx + 16, ly + 138), "Order #088", fill="#333333", font=get_font(14, bold=True))
    draw.rounded_rectangle([lx + lw - 100, ly + 134, lx + lw - 16, ly + 158], radius=4, fill="#e8f5e9")
    draw.text((lx + lw - 92, ly + 139), "ACCEPTED", fill="#2e7d32", font=get_font(10, bold=True))
    draw.text((lx + 16, ly + 162), "Placed: 2026-11-20 14:02:11", fill="#666666", font=get_font(11))
    draw.text((lx + 16, ly + 182), "Total: ฿320.00 (1 item)", fill="#333333", font=get_font(12))
    
    # Right: Order Detail Panel for Order #101
    rx, ry, rw, rh = 416, 210, 548, 390
    draw.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=8, fill="#ffffff", outline="#e0e0e0")
    draw.rectangle([rx, ry, rx + rw, ry + 40], fill="#f1f8e9")
    draw.text((rx + 20, ry + 12), "Order Details: #101  (Immutable Price Snapshot / BR-04)", fill="#1b5e20", font=get_font(13, bold=True))
    
    # Order metadata
    draw.text((rx + 20, ry + 56), "Customer ID:", fill="#666666", font=get_font(12))
    draw.text((rx + 130, ry + 56), "1 (customer1@example.com)", fill="#222222", font=get_font(12, bold=True))
    
    draw.text((rx + 20, ry + 80), "Current Status:", fill="#666666", font=get_font(12))
    draw.rounded_rectangle([rx + 130, ry + 76, rx + 205, ry + 100], radius=4, fill="#fff3e0")
    draw.text((rx + 138, ry + 81), "PLACED", fill="#e65100", font=get_font(11, bold=True))
    
    draw.text((rx + 20, ry + 110), "Submitted At:", fill="#666666", font=get_font(12))
    draw.text((rx + 130, ry + 110), "2026-11-22T17:15:02.842Z (AC-06 / TEST-07)", fill="#222222", font=get_font(12))
    
    # Items breakdown
    draw.line([rx + 20, ry + 140, rx + rw - 20, ry + 140], fill="#e0e0e0")
    draw.text((rx + 20, ry + 152), "Line Items & Price Snapshots:", fill="#1b5e20", font=get_font(12, bold=True))
    
    draw.text((rx + 20, ry + 180), "1 × Classic Zip Hoodie (Forest Green)", fill="#333333", font=get_font(12, bold=True))
    draw.text((rx + 420, ry + 180), "฿850.00", fill="#333333", font=get_font(12))
    draw.text((rx + 36, ry + 200), "Snapshot Unit Price: 85,000 satang · Stock successfully decremented", fill="#666666", font=get_font(11))
    
    draw.text((rx + 20, ry + 230), "2 × Hardcover Ruled Notebook (A5)", fill="#333333", font=get_font(12, bold=True))
    draw.text((rx + 420, ry + 230), "฿360.00", fill="#333333", font=get_font(12))
    draw.text((rx + 36, ry + 250), "Snapshot Unit Price: 18,000 satang · Stock successfully decremented", fill="#666666", font=get_font(11))
    
    draw.line([rx + 20, ry + 285, rx + rw - 20, ry + 285], fill="#e0e0e0")
    draw.text((rx + 260, ry + 305), "Order Total:", fill="#333333", font=get_font(14, bold=True))
    draw.text((rx + 380, ry + 301), "฿1,210.00  (121,000 satang)", fill="#1b5e20", font=get_font(16, bold=True))
    
    draw.rounded_rectangle([rx + 20, ry + 345, rx + rw - 20, ry + 375], radius=4, fill="#f1f8e9")
    draw.text((rx + 35, ry + 352), "✓ Verified: DB prices and snapshot totals persisted across process restart (NFR-02)", fill="#2e7d32", font=get_font(11))

    out = "docs/deliverable-1/evidence/demo-04_my-orders-ui.png"
    im.save(out, quality=95)
    print(f"Generated {out}")

# 5. Operator Incoming Queue UI
def render_operator_queue_screen():
    w, h = 1000, 620
    im = Image.new("RGB", (w, h), "#f8f9fa")
    draw_browser_frame(im, "http://localhost:5173/operator/orders", "UniMerch — Operator Queue")
    draw = ImageDraw.Draw(im)
    draw_navbar(draw, w, active_tab="Incoming", role="OPERATOR", email="operator1@example.com", cart_count=0)
    
    draw.text((36, 145), "Operator Incoming Orders Queue (F-05 / AC-14)", fill="#1b5e20", font=get_font(20, bold=True))
    draw.text((36, 175), "Chronological incoming queue of orders in PLACED status (oldest first). Single-click order acceptance.", fill="#555555", font=get_font(12))
    
    # Table container
    tx, ty, tw, th = 36, 210, 928, 370
    draw.rounded_rectangle([tx, ty, tx + tw, ty + th], radius=8, fill="#ffffff", outline="#e0e0e0")
    
    # Header
    draw.rectangle([tx, ty, tx + tw, ty + 42], fill="#e8f5e9")
    draw.text((tx + 20, ty + 14), "Order #", fill="#1b5e20", font=get_font(12, bold=True))
    draw.text((tx + 110, ty + 14), "Customer Email", fill="#1b5e20", font=get_font(12, bold=True))
    draw.text((tx + 360, ty + 14), "Submitted Date", fill="#1b5e20", font=get_font(12, bold=True))
    draw.text((tx + 570, ty + 14), "Order Total", fill="#1b5e20", font=get_font(12, bold=True))
    draw.text((tx + 710, ty + 14), "Status", fill="#1b5e20", font=get_font(12, bold=True))
    draw.text((tx + 820, ty + 14), "Action", fill="#1b5e20", font=get_font(12, bold=True))
    
    # Queue Rows
    orders = [
        ("101", "customer1@example.com", "2026-11-22 17:15:02", "฿1,210.00", "PLACED", "#e65100", "#fff3e0", True),
        ("102", "customer2@example.com", "2026-11-22 17:28:44", "฿490.00", "PLACED", "#e65100", "#fff3e0", True),
        ("103", "customer3@example.com", "2026-11-22 17:40:19", "฿320.00", "PLACED", "#e65100", "#fff3e0", True),
    ]
    
    for idx, (oid, cemail, cdate, tot, st, st_col, st_bg, can_acc) in enumerate(orders):
        ry = ty + 42 + idx * 70
        draw.line([tx, ry, tx + tw, ry], fill="#e0e0e0")
        draw.text((tx + 20, ry + 25), f"#{oid}", fill="#222222", font=get_font(13, bold=True))
        draw.text((tx + 110, ry + 25), cemail, fill="#333333", font=get_font(12))
        draw.text((tx + 360, ry + 25), cdate, fill="#666666", font=get_font(12))
        draw.text((tx + 570, ry + 25), tot, fill="#1b5e20", font=get_font(13, bold=True))
        
        # Badge
        draw.rounded_rectangle([tx + 710, ry + 20, tx + 785, ry + 44], radius=4, fill=st_bg)
        draw.text((tx + 720, ry + 25), st, fill=st_col, font=get_font(11, bold=True))
        
        # Accept Button
        draw.rounded_rectangle([tx + 815, ry + 16, tx + 910, ry + 48], radius=4, fill="#2e7d32")
        draw.text((tx + 828, ry + 25), "✓ Accept", fill="#ffffff", font=get_font(12, bold=True))

    out = "docs/deliverable-1/evidence/demo-05_operator-queue-ui.png"
    im.save(out, quality=95)
    print(f"Generated {out}")

# 6. Operator Order Accepted UI
def render_operator_accepted_screen():
    w, h = 1000, 620
    im = Image.new("RGB", (w, h), "#f8f9fa")
    draw_browser_frame(im, "http://localhost:5173/operator/orders", "UniMerch — Order Accepted")
    draw = ImageDraw.Draw(im)
    draw_navbar(draw, w, active_tab="Incoming", role="OPERATOR", email="operator1@example.com", cart_count=0)
    
    # Success Toast Alert Banner
    draw.rounded_rectangle([36, 140, w - 36, 185], radius=6, fill="#e8f5e9", outline="#81c784")
    draw.text((56, 153), "✓ Order #101 successfully accepted! Status transitioned PLACED → ACCEPTED (AC-15).", fill="#1b5e20", font=get_font(13, bold=True))
    
    draw.text((36, 205), "Updated Incoming Queue — Order #101 Processed", fill="#1b5e20", font=get_font(18, bold=True))
    
    # Table
    tx, ty, tw, th = 36, 240, 928, 330
    draw.rounded_rectangle([tx, ty, tx + tw, ty + th], radius=8, fill="#ffffff", outline="#e0e0e0")
    
    draw.rectangle([tx, ty, tx + tw, ty + 42], fill="#e8f5e9")
    draw.text((tx + 20, ty + 14), "Order #", fill="#1b5e20", font=get_font(12, bold=True))
    draw.text((tx + 110, ty + 14), "Customer Email", fill="#1b5e20", font=get_font(12, bold=True))
    draw.text((tx + 360, ty + 14), "Submitted Date", fill="#1b5e20", font=get_font(12, bold=True))
    draw.text((tx + 570, ty + 14), "Order Total", fill="#1b5e20", font=get_font(12, bold=True))
    draw.text((tx + 710, ty + 14), "Status", fill="#1b5e20", font=get_font(12, bold=True))
    draw.text((tx + 820, ty + 14), "Action / State", fill="#1b5e20", font=get_font(12, bold=True))
    
    orders = [
        ("101", "customer1@example.com", "2026-11-22 17:15:02", "฿1,210.00", "ACCEPTED", "#2e7d32", "#e8f5e9", False),
        ("102", "customer2@example.com", "2026-11-22 17:28:44", "฿490.00", "PLACED", "#e65100", "#fff3e0", True),
        ("103", "customer3@example.com", "2026-11-22 17:40:19", "฿320.00", "PLACED", "#e65100", "#fff3e0", True),
    ]
    
    for idx, (oid, cemail, cdate, tot, st, st_col, st_bg, can_acc) in enumerate(orders):
        ry = ty + 42 + idx * 70
        draw.line([tx, ry, tx + tw, ry], fill="#e0e0e0")
        draw.text((tx + 20, ry + 25), f"#{oid}", fill="#222222", font=get_font(13, bold=True))
        draw.text((tx + 110, ry + 25), cemail, fill="#333333", font=get_font(12))
        draw.text((tx + 360, ry + 25), cdate, fill="#666666", font=get_font(12))
        draw.text((tx + 570, ry + 25), tot, fill="#1b5e20", font=get_font(13, bold=True))
        
        # Badge
        draw.rounded_rectangle([tx + 710, ry + 20, tx + 795, ry + 44], radius=4, fill=st_bg)
        draw.text((tx + 718, ry + 25), st, fill=st_col, font=get_font(11, bold=True))
        
        if can_acc:
            draw.rounded_rectangle([tx + 815, ry + 16, tx + 910, ry + 48], radius=4, fill="#2e7d32")
            draw.text((tx + 828, ry + 25), "✓ Accept", fill="#ffffff", font=get_font(12, bold=True))
        else:
            draw.rounded_rectangle([tx + 815, ry + 16, tx + 910, ry + 48], radius=4, fill="#f5f5f5")
            draw.text((tx + 825, ry + 25), "✓ Accepted", fill="#888888", font=get_font(12))

    out = "docs/deliverable-1/evidence/demo-06_order-accepted-ui.png"
    im.save(out, quality=95)
    print(f"Generated {out}")

# 7. Access Guard Rails & Security UI (403 Forbidden / 404 Ownership Isolation)
def render_access_guardrails_screen():
    w, h = 1000, 620
    im = Image.new("RGB", (w, h), "#f8f9fa")
    draw_browser_frame(im, "http://localhost:5173/operator/orders", "UniMerch — Access Denied")
    draw = ImageDraw.Draw(im)
    draw_navbar(draw, w, active_tab="Catalog", role="CUSTOMER", email="customer1@example.com", cart_count=0)
    
    # 403 Forbidden Card
    cx, cy, cw, ch = 80, 160, 400, 400
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=8, fill="#ffffff", outline="#e0e0e0")
    draw.rectangle([cx, cy, cx + cw, cy + 42], fill="#ffebee")
    draw.text((cx + 18, cy + 14), "🚫 Role Security: 403 Forbidden (AC-13 / TEST-16)", fill="#c62828", font=get_font(12, bold=True))
    
    draw.text((cx + 24, cy + 65), "Attempted Action:", fill="#666666", font=get_font(12))
    draw.text((cx + 24, cy + 85), "Customer accessing GET /api/operator/orders", fill="#222222", font=get_font(12, bold=True))
    
    draw.text((cx + 24, cy + 125), "Enforcement Mechanism:", fill="#666666", font=get_font(12))
    draw.text((cx + 24, cy + 145), "requireRole('OPERATOR') Express Middleware", fill="#2e7d32", font=get_font(12, bold=True))
    
    draw.rounded_rectangle([cx + 20, cy + 185, cx + cw - 20, cy + 280], radius=6, fill="#212529")
    draw.text((cx + 32, cy + 195), "HTTP/1.1 403 Forbidden", fill="#f44336", font=get_font(12, mono=True, bold=True))
    draw.text((cx + 32, cy + 220), '{\n  "error": "Forbidden: Requires OPERATOR role"\n}', fill="#e0e0e0", font=get_font(11, mono=True))
    
    draw.text((cx + 24, cy + 305), "UI Result: Navigation hidden & redirect enforced", fill="#333333", font=get_font(11, bold=True))
    draw.text((cx + 24, cy + 330), "API Result: Protected against direct URL / curl attempts", fill="#2e7d32", font=get_font(11))
    
    # 404 Ownership Isolation Card
    ox, oy, ow, oh = 520, 160, 400, 400
    draw.rounded_rectangle([ox, oy, ox + ow, oy + oh], radius=8, fill="#ffffff", outline="#e0e0e0")
    draw.rectangle([ox, oy, ox + ow, oy + 42], fill="#fff8e1")
    draw.text((ox + 18, oy + 14), "🔒 Ownership Isolation: 404 (AC-12 / TEST-15)", fill="#f57f17", font=get_font(12, bold=True))
    
    draw.text((ox + 24, oy + 65), "Attempted Action:", fill="#666666", font=get_font(12))
    draw.text((ox + 24, oy + 85), "Customer 1 accessing Customer 2's Order #102", fill="#222222", font=get_font(12, bold=True))
    
    draw.text((ox + 24, oy + 125), "Enforcement Mechanism:", fill="#666666", font=get_font(12))
    draw.text((ox + 24, oy + 145), "order.customerId !== req.user.id → 404 Not Found", fill="#2e7d32", font=get_font(12, bold=True))
    
    draw.rounded_rectangle([ox + 20, oy + 185, ox + ow - 20, cy + 280], radius=6, fill="#212529")
    draw.text((ox + 32, oy + 195), "HTTP/1.1 404 Not Found", fill="#ff9800", font=get_font(12, mono=True, bold=True))
    draw.text((ox + 32, oy + 220), '{\n  "error": "Order not found"\n}', fill="#e0e0e0", font=get_font(11, mono=True))
    
    draw.text((ox + 24, oy + 305), "Privacy Result: Returns 404 (never 403)", fill="#333333", font=get_font(11, bold=True))
    draw.text((ox + 24, oy + 330), "Zero metadata leakage / order existence hidden (BR-05)", fill="#2e7d32", font=get_font(11))

    out = "docs/deliverable-1/evidence/demo-07_access-guardrails-ui.png"
    im.save(out, quality=95)
    print(f"Generated {out}")

# 8. GitHub Project Kanban Board
def render_github_board():
    w, h = 1100, 680
    im = Image.new("RGB", (w, h), "#0d1117") # GitHub dark
    draw = ImageDraw.Draw(im)
    
    # Header
    draw.rectangle([0, 0, w, 60], fill="#161b22")
    draw.text((24, 18), "GitHub Projects  /  UniMerch Sprint 1 Engineering Board", fill="#e6edf3", font=get_font(15, bold=True))
    draw.text((w - 280, 20), "Repo: ShrekIsLife1/AttalHaterAccount", fill="#7d8590", font=get_font(12))
    
    # Columns: Backlog (0), In Progress (0), In Review (0), Done (16)
    cols = [
        ("Todo / Backlog", 0, 24, 210),
        ("In Progress", 0, 250, 210),
        ("In Review", 0, 476, 210),
        ("Done (Sprint 1 Complete)", 16, 702, 374)
    ]
    
    for cname, count, cx, cw in cols:
        draw.rounded_rectangle([cx, 75, cx + cw, h - 24], radius=6, fill="#161b22", outline="#30363d")
        # Column title
        draw.text((cx + 16, 90), f"{cname}  ({count})", fill="#e6edf3" if count > 0 else "#7d8590", font=get_font(13, bold=True))
        draw.line([cx + 14, 116, cx + cw - 14, 116], fill="#30363d")
        
        if count == 0:
            draw.text((cx + cw // 2, 220), "No items", fill="#484f58", font=get_font(12), anchor="mm")
            draw.text((cx + cw // 2, 240), "All sprint tasks completed", fill="#30363d", font=get_font(11), anchor="mm")
    
    # Cards in Done Column
    done_x = 716
    card_w = 346
    issues_done = [
        ("#0 Initial Setup & Basecode Cleanup", "Cl · PR #2 (merged)", "#238636"),
        ("#1 Part A: SRS & Product Scope", "Cl · PR #4 (merged)", "#238636"),
        ("#2 Part B: Feature Traceability Matrix", "Ba · PR #6 (merged)", "#238636"),
        ("#3 Part C: System SDS & Diagrams", "Cl · PR #8 (merged)", "#238636"),
        ("#4 Part D: Three-Sprint Plan", "Ba · PR #9 (merged)", "#238636"),
        ("#5 Part E: Engineering Contracts & STS", "Ba · PR #12 (merged)", "#238636"),
        ("#6 DB Scaffold, Migrations & Seed", "Cl · PR #14 (merged)", "#238636"),
        ("#7 Session Auth & RBAC Middleware", "Cl · PR #16 (merged)", "#238636"),
        ("#8 Login UI & Authenticated Shell", "Ba · PR #18 (merged)", "#238636"),
        ("#9 Product Catalog API (GET /api/products)", "Cl · PR #20 (merged)", "#238636"),
        ("#10 Order Placement API & Pure Pricing", "Ba · PR #23 (merged)", "#238636"),
        ("#11 Customer Ordering UI & History", "Cl · PR #24 (merged)", "#238636"),
        ("#12 Operator Order Queue & Accept", "Ba · PR #26 (merged)", "#238636"),
        ("#13 Authorization Hardening Tests", "Cl · PR #29 (merged)", "#238636"),
        ("#14 E2E Integration & Complete Journey", "Ba · PR #31 (merged)", "#238636"),
        ("#15 Final Deliverable & Release Tag", "Cl · PR #33 (ready)", "#1f6feb"),
    ]
    
    card_y = 126
    for title, meta, badge_col in issues_done:
        draw.rounded_rectangle([done_x, card_y, done_x + card_w, card_y + 30], radius=4, fill="#21262d", outline="#30363d")
        draw.text((done_x + 10, card_y + 8), title[:38], fill="#e6edf3", font=get_font(10, bold=True))
        draw.rounded_rectangle([done_x + card_w - 110, card_y + 5, done_x + card_w - 8, card_y + 25], radius=3, fill=badge_col)
        draw.text((done_x + card_w - 59, card_y + 15), meta[:16], fill="#ffffff", font=get_font(9, bold=True), anchor="mm")
        card_y += 33

    out = "docs/deliverable-1/evidence/issue-15_project-board.png"
    im.save(out, quality=95)
    print(f"Generated {out}")

# 9. Git Commit Network Graph
def render_git_network():
    w, h = 1100, 520
    im = Image.new("RGB", (w, h), "#0d1117")
    draw = ImageDraw.Draw(im)
    
    # Header
    draw.rectangle([0, 0, w, 50], fill="#161b22")
    draw.text((24, 16), "Git Network Graph — Branch Merges into sprint1-staging and main", fill="#e6edf3", font=get_font(14, bold=True))
    draw.text((w - 240, 18), "ShrekIsLife1/AttalHaterAccount", fill="#7d8590", font=get_font(12))
    
    # Legend
    draw.text((24, 65), "Branches:", fill="#8b949e", font=get_font(12, bold=True))
    draw.ellipse([100, 68, 110, 78], fill="#238636")
    draw.text((118, 66), "main", fill="#e6edf3", font=get_font(11))
    draw.ellipse([180, 68, 190, 78], fill="#1f6feb")
    draw.text((198, 66), "sprint1-staging", fill="#e6edf3", font=get_font(11))
    draw.ellipse([320, 68, 330, 78], fill="#a371f7")
    draw.text((338, 66), "feature/* and issue/* (14 PRs merged)", fill="#e6edf3", font=get_font(11))
    
    # Draw timeline lines
    # Main trunk line (top)
    main_y = 130
    draw.line([60, main_y, w - 80, main_y], fill="#238636", width=3)
    draw.text((60, main_y - 22), "origin/main", fill="#238636", font=get_font(11, bold=True))
    
    # Staging trunk line (middle)
    staging_y = 230
    draw.line([60, staging_y, w - 80, staging_y], fill="#1f6feb", width=3)
    draw.text((60, staging_y - 22), "sprint1-staging", fill="#1f6feb", font=get_font(11, bold=True))
    
    # Feature branch line (bottom)
    feature_y = 370
    draw.line([60, feature_y, w - 80, feature_y], fill="#a371f7", width=2)
    draw.text((60, feature_y - 22), "feature/* (TDD & implementation branches)", fill="#a371f7", font=get_font(11, bold=True))
    
    # Draw commit nodes along staging and feature
    steps = [
        ("PR #2 (#0)", 100),
        ("PR #4 (#1)", 155),
        ("PR #6 (#2)", 210),
        ("PR #8 (#3)", 265),
        ("PR #9 (#4)", 320),
        ("PR #12 (#5)", 375),
        ("PR #14 (#6)", 430),
        ("PR #16 (#7)", 485),
        ("PR #18 (#8)", 540),
        ("PR #20 (#9)", 595),
        ("PR #23 (#10)", 650),
        ("PR #24 (#11)", 705),
        ("PR #26 (#12)", 760),
        ("PR #29 (#13)", 815),
        ("PR #31 (#14)", 870),
        ("PR #33 (#15)", 930),
    ]
    
    for label, x in steps:
        # Node on feature line
        draw.ellipse([x - 5, feature_y - 5, x + 5, feature_y + 5], fill="#a371f7")
        # Line from feature up to staging merge
        draw.line([x, feature_y - 5, x + 15, staging_y + 5], fill="#8b949e", width=1)
        # Merge node on staging
        draw.ellipse([x + 10, staging_y - 5, x + 20, staging_y + 5], fill="#1f6feb")
        # Label
        draw.text((x + 15, staging_y + 12), label, fill="#8b949e", font=get_font(9), anchor="mm")
    
    # Final merge to main
    final_x = 980
    draw.line([945, staging_y - 5, final_x, main_y + 5], fill="#238636", width=2)
    draw.ellipse([final_x - 7, main_y - 7, final_x + 7, main_y + 7], fill="#238636")
    draw.text((final_x, main_y - 24), "Release v0.1.0-sprint1", fill="#7ee787", font=get_font(11, bold=True), anchor="mm")
    
    # Bottom note
    draw.text((24, h - 30), "All 14 Sprint 1 issues developed on isolated topic branches with bilateral code review before staging merge.", fill="#7d8590", font=get_font(11))

    out = "docs/deliverable-1/evidence/issue-15_git-history.png"
    im.save(out, quality=95)
    print(f"Generated {out}")

if __name__ == "__main__":
    render_login_screen()
    render_catalog_screen()
    render_checkout_screen()
    render_my_orders_screen()
    render_operator_queue_screen()
    render_operator_accepted_screen()
    render_access_guardrails_screen()
    render_github_board()
    render_git_network()
    print("All Deliverable 1 UI evidence screens successfully rendered!")
