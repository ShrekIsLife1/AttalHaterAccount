#!/usr/bin/env python3
"""
Build ultra-clean, minimalist Lab 5 Deliverable PDF matching strictly the Lab 3 / Deliverable 1 design:
- Crisp green headings (#0b6623) with underline rules
- Header with course/group name and footer with Page X / Y
- URLs in green-tinted dashed boxes
- All 12 screenshots embedded with dashed borders and italic captions
"""
import os
import pymupdf
from PIL import Image

OUTPUT = "docs/deliverable-2/lab5_sec1_AttalHaterAccount.pdf"
EVID_DIR = "docs/deliverable-2/evidence"

PAGE_W = 595.32  # A4 width in pt
PAGE_H = 841.92  # A4 height in pt
MARGIN_X = 42.0

COL_GREEN = (11/255, 102/255, 35/255)       # #0b6623 deep green
COL_LIGHT_GREEN = (238/255, 245/255, 238/255) # #eef5ee
COL_BORDER_GREEN = (129/255, 199/255, 132/255) # #81c784
COL_DARK = (26/255, 26/255, 26/255)         # #1a1a1a
COL_GRAY = (117/255, 117/255, 117/255)      # #757575
COL_LINE = (204/255, 204/255, 204/255)      # #cccccc

doc = pymupdf.open()

def add_header_footer(page, p_num, total):
    if p_num > 1:
        # Running top header
        page.insert_text((PAGE_W - 240, 26), "UniMerch — Lab 5 — AttalHaterAccount", fontsize=8, color=COL_GRAY)
        page.draw_line(pymupdf.Point(MARGIN_X, 32), pymupdf.Point(PAGE_W - MARGIN_X, 32), color=COL_LINE, width=0.5)
    # Footer
    page.draw_line(pymupdf.Point(MARGIN_X, PAGE_H - 30), pymupdf.Point(PAGE_W - MARGIN_X, PAGE_H - 30), color=COL_LINE, width=0.5)
    page.insert_text((PAGE_W / 2 - 20, PAGE_H - 16), f"Page {p_num} / {total}", fontsize=8.5, color=COL_GRAY)

def draw_part_header(page, y, title):
    page.insert_text((MARGIN_X, y), title, fontsize=13.5, fontname="helv", color=COL_GREEN)
    page.draw_line(pymupdf.Point(MARGIN_X, y + 4), pymupdf.Point(PAGE_W - MARGIN_X, y + 4), color=COL_GREEN, width=1.2)
    return y + 16

def draw_link_box(page, y, lines):
    box_h = 8 + len(lines) * 14
    rect = pymupdf.Rect(MARGIN_X, y, PAGE_W - MARGIN_X, y + box_h)
    page.draw_rect(rect, color=COL_BORDER_GREEN, fill=COL_LIGHT_GREEN, dashes="[2 2] 0", width=0.8)
    cur_y = y + 12
    for label, val in lines:
        page.insert_text((MARGIN_X + 10, cur_y), label, fontsize=8.5, fontname="hebo", color=COL_GREEN)
        lbl_w = pymupdf.get_text_length(label, fontname="hebo", fontsize=8.5)
        page.insert_text((MARGIN_X + 14 + lbl_w, cur_y), val, fontsize=8.5, fontname="helv", color=COL_DARK)
        cur_y += 14
    return y + box_h + 10

def draw_screenshot(page, y, img_name, caption, max_h=215):
    img_path = os.path.join(EVID_DIR, img_name)
    with Image.open(img_path) as im:
        orig_w, orig_h = im.size
    
    avail_w = PAGE_W - 2 * MARGIN_X
    scale = avail_w / orig_w
    img_h = orig_h * scale
    
    if img_h > max_h:
        scale = max_h / orig_h
        img_w = orig_w * scale
        img_h = max_h
        offset_x = (avail_w - img_w) / 2
    else:
        img_w = avail_w
        offset_x = 0
        
    frame_rect = pymupdf.Rect(MARGIN_X, y, PAGE_W - MARGIN_X, y + img_h + 8)
    page.draw_rect(frame_rect, color=COL_LINE, dashes="[3 3] 0", width=0.8)
    
    img_rect = pymupdf.Rect(MARGIN_X + offset_x, y + 4, MARGIN_X + offset_x + img_w, y + 4 + img_h)
    page.insert_image(img_rect, filename=img_path)
    
    cap_y = y + img_h + 18
    cap_w = pymupdf.get_text_length(caption, fontname="heit", fontsize=8)
    page.insert_text((PAGE_W / 2 - cap_w / 2, cap_y), caption, fontsize=8, fontname="heit", color=COL_GRAY)
    
    return cap_y + 12

# ==========================================
# PAGE 1: COVER
# ==========================================
p1 = doc.new_page(width=PAGE_W, height=PAGE_H)
p1.insert_text((PAGE_W / 2 - 180, 210), "Project Deliverable 2 — UniMerch:", fontsize=20, fontname="hebo", color=COL_GREEN)
p1.insert_text((PAGE_W / 2 - 195, 238), "Cloud Deployment & CI/CD on GCP", fontsize=20, fontname="hebo", color=COL_GREEN)

p1.insert_text((PAGE_W / 2 - 175, 280), "Engineering Baseline + Cloud Ready Operations (Theme 4)", fontsize=11, fontname="hebo", color=COL_DARK)
p1.insert_text((PAGE_W / 2 - 190, 312), "Clément Dominique Delrieu — Student ID 69540460016 (@ClemDelGh)", fontsize=9.5, fontname="hebo", color=(50/255, 50/255, 50/255))
p1.insert_text((PAGE_W / 2 - 170, 328), "Baptiste Carré — Student ID 69540460014 (@ShrekIsLife1)", fontsize=9.5, fontname="hebo", color=(50/255, 50/255, 50/255))

p1.insert_text((PAGE_W / 2 - 215, 360), "GitHub repository: https://github.com/ShrekIsLife1/AttalHaterAccount · Tag: v0.2.0-lab5", fontsize=9, fontname="heit", color=COL_GRAY)
p1.insert_text((PAGE_W / 2 - 145, 376), "Live Cloud Run URL: https://s3c35c9bd-4d7hbszvwq-as.a.run.app", fontsize=9, fontname="heit", color=COL_GRAY)

# ==========================================
# PAGE 2: PART 0 (Contribution table + Git Network)
# ==========================================
p2 = doc.new_page(width=PAGE_W, height=PAGE_H)
y = draw_part_header(p2, 50, "Answer Part 0 — Team & Evidence Index")
y = draw_link_box(p2, y, [
    ("Repository: ", "https://github.com/ShrekIsLife1/AttalHaterAccount"),
    ("Pull Requests: ", "https://github.com/ShrekIsLife1/AttalHaterAccount/pulls"),
    ("Deployment Docs: ", "https://github.com/ShrekIsLife1/AttalHaterAccount/blob/main/docs/labs/lab05/deployment.md"),
    ("Test Matrix: ", "https://github.com/ShrekIsLife1/AttalHaterAccount/blob/main/docs/labs/lab05/tests.md"),
])

p2.insert_text((MARGIN_X, y), "0.1 Lab 5 Pair Contributions (#16–#25)", fontsize=9.5, fontname="hebo", color=COL_DARK)
y += 8

# Draw table
table_data = [
    ("#16", "GCP account, project, budget alert & baseline", "Ba", "Cl", "#44"),
    ("#17", "Cloud-ready config, probes, .env.example", "Cl", "Ba", "#45"),
    ("#18", "Dockerize application & container verification", "Ba", "Cl", "#46"),
    ("#19", "CI on Pull Requests (test-and-docker, C-01)", "Cl", "Ba", "#47"),
    ("#20", "First deployment to GCP & domain journey (C-04)", "Ba", "Cl", "#48"),
    ("#21", "GitHub ↔ GCP (WIF) & failing PR gate (C-02)", "Cl", "Ba", "#50"),
    ("#22", "Repeatable deploy pipeline & release commit (C-06)", "Ba", "Cl", "#51"),
    ("#23", "Cloud persistence & rollback verification (C-05)", "Cl", "Ba", "#52"),
    ("#24", "Cost control: pause/resume Cloud SQL & quota audit", "Ba", "Cl", "#49"),
    ("#25", "Final deployment docs & deliverable report", "Cl", "Ba", "#53"),
]

col_w = [38, 290, 48, 55, 45]
row_h = 13.5
# Header row
p2.draw_rect(pymupdf.Rect(MARGIN_X, y, PAGE_W - MARGIN_X, y + row_h), fill=COL_LIGHT_GREEN, color=COL_LINE, width=0.5)
headers = ["Issue", "Title", "Author", "Reviewer", "PR"]
cx = MARGIN_X + 4
for i, h_txt in enumerate(headers):
    p2.insert_text((cx, y + 9.5), h_txt, fontsize=8, fontname="hebo", color=COL_GREEN)
    cx += col_w[i]
y += row_h

for row in table_data:
    p2.draw_rect(pymupdf.Rect(MARGIN_X, y, PAGE_W - MARGIN_X, y + row_h), color=COL_LINE, width=0.5)
    cx = MARGIN_X + 4
    for i, val in enumerate(row):
        fnt = "hebo" if i == 0 else "helv"
        p2.insert_text((cx, y + 9.5), val, fontsize=7.5, fontname=fnt, color=COL_DARK)
        cx += col_w[i]
    y += row_h
y += 12

p2.insert_text((MARGIN_X, y), "0.2 Commit History on main (feature branches → lab5-staging → main)", fontsize=9.5, fontname="hebo", color=COL_DARK)
y += 10
y = draw_screenshot(p2, y, "01_git_network.png", "Figure 0.1: Git Network Graph — bilateral pair review on lab5-staging before main CD cutover.", max_h=195)

# ==========================================
# PAGE 3: PART 0 (Incognito) + PART 1 (CI Passing)
# ==========================================
p3 = doc.new_page(width=PAGE_W, height=PAGE_H)
y = 50
p3.insert_text((MARGIN_X, y), "0.3 Public Repository Verified in Incognito Mode (R-12)", fontsize=9.5, fontname="hebo", color=COL_DARK)
y += 10
y = draw_screenshot(p3, y, "02_incognito_repo.png", "Figure 0.2: GitHub public repository verified in unauthenticated incognito mode (R-12 compliant).", max_h=225)
y += 15

y = draw_part_header(p3, y, "Answer Part 1 — CI and Quality Gate (C-01, C-02)")
y = draw_link_box(p3, y, [
    ("CI Workflow: ", "https://github.com/ShrekIsLife1/AttalHaterAccount/blob/main/.github/workflows/ci-docker.yml"),
])

p3.insert_text((MARGIN_X, y), "1.1 Check C-01 — Passing Pull Request Verification (test-and-docker)", fontsize=9.5, fontname="hebo", color=COL_DARK)
y += 10
y = draw_screenshot(p3, y, "03_ci_passing.png", "Screenshot 1.1: GitHub Actions CI workflow test-and-docker passing on pull request (C-01).", max_h=215)

# ==========================================
# PAGE 4: PART 1 (Branch Protection + Failing PR Blocked)
# ==========================================
p4 = doc.new_page(width=PAGE_W, height=PAGE_H)
y = 50
p4.insert_text((MARGIN_X, y), "1.2 Check C-02 — Branch Protection Ruleset (R-09)", fontsize=9.5, fontname="hebo", color=COL_DARK)
y += 10
y = draw_screenshot(p4, y, "04_branch_protection.png", "Screenshot 1.2: Branch protection ruleset on lab5-staging & main requiring test-and-docker status check.", max_h=220)
y += 18

p4.insert_text((MARGIN_X, y), "1.3 Check C-02 — Failing Pull Request Blocked by Merge Gate", fontsize=9.5, fontname="hebo", color=COL_DARK)
y += 10
y = draw_screenshot(p4, y, "05_failing_pr_blocked.png", "Screenshot 1.3: Failing PR blocked by branch protection gate; merge button disabled (C-02).", max_h=230)

# ==========================================
# PAGE 5: PART 1 (WIF) + PART 2 (Docker Container)
# ==========================================
p5 = doc.new_page(width=PAGE_W, height=PAGE_H)
y = 50
p5.insert_text((MARGIN_X, y), "1.4 Workload Identity Federation (R-06 — environment: demo)", fontsize=9.5, fontname="hebo", color=COL_DARK)
y += 10
y = draw_screenshot(p5, y, "06_wif_env.png", "Screenshot 1.4: Keyless Workload Identity Federation configuration in environment: demo (zero secret keys).", max_h=220)
y += 16

y = draw_part_header(p5, y, "Answer Part 2 — Docker and Reproducible Configuration (C-03)")
y = draw_link_box(p5, y, [
    ("Dockerfile: ", "https://github.com/ShrekIsLife1/AttalHaterAccount/blob/main/Dockerfile"),
    ("docker-compose.yml: ", "https://github.com/ShrekIsLife1/AttalHaterAccount/blob/main/docker-compose.yml"),
    (".env.example: ", "https://github.com/ShrekIsLife1/AttalHaterAccount/blob/main/.env.example"),
])

p5.insert_text((MARGIN_X, y), "2.1 Check C-03 — Unified Production Container Verification (TEST-L5-10..14)", fontsize=9.5, fontname="hebo", color=COL_DARK)
y += 10
y = draw_screenshot(p5, y, "07_docker_container.png", "Screenshot 2.1: Automated container test suite test-container.sh (TEST-L5-10..14) all passing (C-03).", max_h=225)

# ==========================================
# PAGE 6: PART 3 (Live Probes + Live Customer Journey)
# ==========================================
p6 = doc.new_page(width=PAGE_W, height=PAGE_H)
y = draw_part_header(p6, 50, "Answer Part 3 — GCP Deployment and Persistence (C-04, C-05)")
y = draw_link_box(p6, y, [
    ("Live Cloud Run URL: ", "https://s3c35c9bd-4d7hbszvwq-as.a.run.app"),
])

p6.insert_text((MARGIN_X, y), "3.1 Check C-04 — Public Health, Readiness & Version Probes", fontsize=9.5, fontname="hebo", color=COL_DARK)
y += 10
y = draw_screenshot(p6, y, "08_live_probes.png", "Screenshot 3.1: Live probes (/api/ready 200, /api/version commit SHA) on Cloud Run service.", max_h=215)
y += 16

p6.insert_text((MARGIN_X, y), "3.2 Check C-04 — Live Domain Customer Purchasing Journey (TEST-L5-21)", fontsize=9.5, fontname="hebo", color=COL_DARK)
y += 10
y = draw_screenshot(p6, y, "09_live_customer_journey.png", "Screenshot 3.2: Customer cart checkout and authoritative pricing on Cloud Run live domain (TEST-L5-21).", max_h=225)

# ==========================================
# PAGE 7: PART 3 (RBAC Rejection + Cloud Persistence)
# ==========================================
p7 = doc.new_page(width=PAGE_W, height=PAGE_H)
y = 50
p7.insert_text((MARGIN_X, y), "3.3 Check C-04 — RBAC & Business Rule Rejections on Live Service", fontsize=9.5, fontname="hebo", color=COL_DARK)
y += 10
y = draw_screenshot(p7, y, "10_live_rbac_rejection.png", "Screenshot 3.3: RBAC 403 Forbidden and business rule 400 Bad Request enforcement on live domain (TEST-L5-22, 23).", max_h=220)
y += 18

p7.insert_text((MARGIN_X, y), "3.4 Check C-05 — Cloud Database Persistence & Rollback Verification", fontsize=9.5, fontname="hebo", color=COL_DARK)
y += 10
y = draw_screenshot(p7, y, "11_cloud_persistence.png", "Screenshot 3.4: Order persistence in Cloud SQL across container restart and pause/resume lifecycle (C-05).", max_h=225)

# ==========================================
# PAGE 8: PART 4 (Repeatable Release Pipeline C-06)
# ==========================================
p8 = doc.new_page(width=PAGE_W, height=PAGE_H)
y = draw_part_header(p8, 50, "Answer Part 4 — Repeatable Release Pipeline (C-06)")
y = draw_link_box(p8, y, [
    ("CD Pipeline: ", "https://github.com/ShrekIsLife1/AttalHaterAccount/blob/main/.github/workflows/deploy.yml"),
])

p8.insert_text((MARGIN_X, y), "4.1 Check C-06 — Automated Continuous Deployment on main (TEST-L5-32..42)", fontsize=9.5, fontname="hebo", color=COL_DARK)
y += 10
y = draw_screenshot(p8, y, "12_cd_deploy_demo.png", "Screenshot 4.1: Automated release pipeline deploy.yml executed on push to main with immutable digest pinning (C-06).", max_h=250)
y += 18

p8.insert_text((MARGIN_X, y), "4.2 Release Revision Matches Commit SHA (R-08 Verification)", fontsize=9.5, fontname="hebo", color=COL_DARK)
y += 12
y = draw_link_box(p8, y, [
    ("Live /api/version verification: ", "curl -fsS https://s3c35c9bd-4d7hbszvwq-as.a.run.app/api/version"),
    ("Verified Output: ", '{"commit": "d833012a95c942918bb13b94e098a50f117bcde2"} (matches main release commit)'),
    ("Rollback Guarantee: ", "workflow_dispatch image_tag points Cloud Run to prior digest without DB migration loss."),
])

# Add header/footer to all pages
total_pages = len(doc)
for i, p in enumerate(doc, start=1):
    add_header_footer(p, i, total_pages)

doc.save(OUTPUT)
doc.close()
print(f"Generated {OUTPUT} ({total_pages} pages) successfully!")
