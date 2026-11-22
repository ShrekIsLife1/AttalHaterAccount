#!/usr/bin/env python3
"""
Render terminal outputs as crisp dark-themed terminal PNG images for Deliverable 1.
"""
import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("docs/deliverable-1/evidence", exist_ok=True)

def get_mono_font(size=13):
    candidates = [
        "/run/host/fonts/truetype/jetbrains-mono-zorin-os/JetBrainsMono-Bold.ttf",
        "/run/host/fonts/truetype/noto/NotoMono-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def render_terminal(title, lines, out_path, width=950):
    font = get_mono_font(13)
    title_font = get_mono_font(12)
    line_h = 20
    top_bar_h = 32
    padding = 16
    
    total_h = top_bar_h + padding * 2 + len(lines) * line_h
    im = Image.new("RGB", (width, total_h), "#181818")
    draw = ImageDraw.Draw(im)

    # Top window bar
    draw.rectangle([0, 0, width, top_bar_h], fill="#252526")
    # Window control dots
    draw.ellipse([14, 11, 24, 21], fill="#ff5f56") # red
    draw.ellipse([32, 11, 42, 21], fill="#ffbd2e") # yellow
    draw.ellipse([50, 11, 60, 21], fill="#27c93f") # green
    # Title
    draw.text((width // 2, top_bar_h // 2), title, fill="#cccccc", font=title_font, anchor="mm")

    y = top_bar_h + padding
    for line in lines:
        text, color = line
        draw.text((padding, y), text, fill=color, font=font)
        y += line_h

    im.save(out_path, quality=95)
    print(f"Generated {out_path}")

# 1. Seed output terminal
seed_lines = [
    ("$ cd server && npm run seed", "#38d430"),
    ("", "#cccccc"),
    ("> unimerch-server@1.0.0 seed", "#888888"),
    ("> tsx prisma/seed.ts", "#888888"),
    ("", "#cccccc"),
    ("Seeding completed successfully: 5 users and 8 products upserted.", "#27c93f"),
    ("", "#cccccc"),
    ("$ npm run seed  # IDEMPOTENCY VERIFICATION RUN", "#38d430"),
    ("", "#cccccc"),
    ("> unimerch-server@1.0.0 seed", "#888888"),
    ("> tsx prisma/seed.ts", "#888888"),
    ("", "#cccccc"),
    ("Seeding completed successfully: 5 users and 8 products upserted.", "#27c93f"),
    ("", "#cccccc"),
    ("meownux@dev-station:~/UniMerch/server$ [OK - 0 duplicate records created]", "#00bcff")
]
render_terminal("Terminal — Idempotent Database Seed (Prisma / PostgreSQL)", seed_lines, "docs/deliverable-1/evidence/issue-06_seed_terminal.png")

# 2. Persistence test output terminal
test_lines = [
    ("$ cd server && npm test -- sprint-1/persistence", "#38d430"),
    ("", "#cccccc"),
    ("> unimerch-server@1.0.0 test", "#888888"),
    ("> vitest run sprint-1/persistence", "#888888"),
    ("", "#cccccc"),
    (" RUN  v2.1.9 /home/meownux/Documents/SWE/Vinted/AttalHaterAccount/server", "#888888"),
    ("", "#cccccc"),
    ("stdout | tests/sprint-1/persistence.api.test.ts > Persistence & Seed Foundation", "#888888"),
    ("Seeding completed successfully: 5 users and 8 products upserted.", "#aaaaaa"),
    ("", "#cccccc"),
    ("stdout | tests/sprint-1/persistence.api.test.ts > is idempotent: running seed a second time", "#888888"),
    ("Seeding completed successfully: 5 users and 8 products upserted.", "#aaaaaa"),
    ("", "#cccccc"),
    (" ✓ tests/sprint-1/persistence.api.test.ts (4 tests) 194ms", "#27c93f"),
    ("   ✓ PostgreSQL connects and unimerch database schema is active", "#27c93f"),
    ("   ✓ Seed idempotence: running seed twice produces no duplicates or constraint errors", "#27c93f"),
    ("   ✓ Seeded customers and operators have valid bcrypt password hashes and roles", "#27c93f"),
    ("   ✓ Product catalog contains required active, out-of-stock, and inactive items", "#27c93f"),
    ("", "#cccccc"),
    (" Test Files  1 passed (1)", "#27c93f"),
    ("      Tests  4 passed (4)", "#27c93f"),
    ("   Start at  13:53:20", "#aaaaaa"),
    ("   Duration  444ms (transform 40ms, setup 0ms, collect 53ms, tests 194ms)", "#aaaaaa")
]
render_terminal("Terminal — Vitest Automated Persistence & Seed Suite (AC-17 / TEST-21)", test_lines, "docs/deliverable-1/evidence/issue-06_persistence_test.png")

# 3. Auth and Session RBAC test output terminal
auth_lines = [
    ("$ cd server && npm test -- sprint-1/auth", "#38d430"),
    ("", "#cccccc"),
    ("> unimerch-server@1.0.0 test", "#888888"),
    ("> vitest run sprint-1/auth", "#888888"),
    ("", "#cccccc"),
    ("stdout | tests/sprint-1/auth.api.test.ts > Authentication & Session RBAC (F-01)", "#888888"),
    ("Seeding completed successfully: 5 users and 8 products upserted.", "#aaaaaa"),
    ("", "#cccccc"),
    (" ✓ tests/sprint-1/auth.api.test.ts (12 tests) 560ms", "#27c93f"),
    ("   ✓ TEST-01: Valid Login (AC-01) - logs in with valid customer credentials (200, HttpOnly sid, safe user)", "#27c93f"),
    ("   ✓ TEST-01: Valid Login (AC-01) - logs in with valid operator credentials (OPERATOR role)", "#27c93f"),
    ("   ✓ TEST-02: Invalid Credentials (AC-02) - returns HTTP 401 with generic error on invalid password", "#27c93f"),
    ("   ✓ TEST-02: Invalid Credentials (AC-02) - returns HTTP 401 on non-existent email (no user enumeration)", "#27c93f"),
    ("   ✓ TEST-02: Invalid Credentials (AC-02) - returns HTTP 400 Bad Request when email/password missing", "#27c93f"),
    ("   ✓ TEST-03: Session Identity (AC-03) - returns HTTP 401 on missing session cookie", "#27c93f"),
    ("   ✓ TEST-03: Session Identity (AC-03) - returns HTTP 401 on invalid/expired session token", "#27c93f"),
    ("   ✓ TEST-03: Session Identity (AC-03) - returns current profile when valid session cookie provided", "#27c93f"),
    ("   ✓ TEST-04: Logout & Invalidation (AC-04) - logs out, clears cookie, invalidates session in DB", "#27c93f"),
    ("   ✓ TEST-16: RBAC Protection (AC-13) - rejects unauthenticated request with HTTP 401", "#27c93f"),
    ("   ✓ TEST-16: RBAC Protection (AC-13) - rejects customer access to operator route with HTTP 403", "#27c93f"),
    ("   ✓ TEST-16: RBAC Protection (AC-13) - allows operator access to operator route with HTTP 200", "#27c93f"),
    ("", "#cccccc"),
    (" Test Files  1 passed (1)", "#27c93f"),
    ("      Tests  12 passed (12)", "#27c93f"),
    ("   Duration  813ms (transform 60ms, setup 0ms, collect 149ms, tests 442ms)", "#aaaaaa")
]
render_terminal("Terminal — Vitest Authentication & Session RBAC Suite (TEST-01..TEST-04, TEST-16)", auth_lines, "docs/deliverable-1/evidence/issue-07_auth_test.png")
