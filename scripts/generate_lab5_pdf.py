#!/usr/bin/env python3
"""
Generate the complete Lab 5 Deliverable PDF with all 12 evidence screenshots embedded,
following the clean, minimalist Lab 3 / Deliverable 1 design.
"""
import os
import pymupdf

OUTPUT = "docs/deliverable-2/lab5_sec1_AttalHaterAccount.pdf"

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @page {
    size: a4;
    margin: 20mm 16mm 20mm 16mm;
  }
  body {
    font-family: sans-serif;
    font-size: 9.5pt;
    color: #1a1a1a;
    line-height: 1.45;
    margin: 0;
  }
  .cover {
    text-align: center;
    padding-top: 26mm;
    page-break-after: always;
  }
  .cover-title {
    color: #1b5e20;
    font-size: 22pt;
    font-weight: bold;
    line-height: 1.3;
    margin-bottom: 8mm;
  }
  .cover-sub {
    font-size: 13pt;
    font-weight: bold;
    color: #222222;
    margin-bottom: 6mm;
  }
  .cover-names {
    font-size: 10.5pt;
    font-weight: bold;
    color: #333333;
    margin-bottom: 3mm;
  }
  .cover-meta {
    font-size: 9.5pt;
    color: #555555;
    margin-bottom: 2mm;
  }
  h1.part {
    color: #1b5e20;
    font-size: 14pt;
    font-weight: bold;
    border-bottom: 1.5pt solid #1b5e20;
    padding-bottom: 3pt;
    margin-top: 5mm;
    margin-bottom: 4mm;
    page-break-after: avoid;
  }
  .page-break {
    page-break-before: always;
  }
  .link-box {
    border: 1pt dashed #81c784;
    background-color: #f1f8e9;
    padding: 3mm 4mm;
    margin-bottom: 4mm;
    font-size: 9pt;
  }
  .link-line {
    margin: 1.5mm 0;
  }
  .link-line b {
    color: #1b5e20;
  }
  h2.sub {
    font-size: 10.5pt;
    font-weight: bold;
    color: #111111;
    margin-top: 5mm;
    margin-bottom: 2.5mm;
    page-break-after: avoid;
  }
  .screenshot-frame {
    border: 1pt dashed #9e9e9e;
    padding: 2.5mm;
    margin-top: 2mm;
    margin-bottom: 1.5mm;
    text-align: center;
    page-break-inside: avoid;
  }
  .screenshot-frame img {
    width: 100%;
    max-width: 530pt;
    height: auto;
    display: block;
    margin: 0 auto;
  }
  .caption {
    font-size: 8.5pt;
    font-style: italic;
    color: #555555;
    text-align: center;
    margin-bottom: 5mm;
    page-break-before: avoid;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 8.5pt;
    margin-top: 2mm;
    margin-bottom: 5mm;
    page-break-inside: avoid;
  }
  th, td {
    border: 0.5pt solid #cccccc;
    padding: 3pt 5pt;
    text-align: left;
  }
  th {
    background-color: #eef5ee;
    color: #1b5e20;
    font-weight: bold;
  }
</style>
</head>
<body>

<!-- Page 1: Cover -->
<div class="cover">
  <div class="cover-title">Project Deliverable 2 — UniMerch:<br>Cloud Deployment &amp; CI/CD on GCP</div>
  <div class="cover-sub">Engineering Baseline + Cloud Ready Operations (Lab 5 — Theme 4)</div>
  <div class="cover-names">Baptiste Carré — Student ID 69540460014 (@ShrekIsLife1)<br>Clément Dominique Delrieu — Student ID 69540460016 (@ClemDelGh)</div>
  <div class="cover-meta">GitHub repository: https://github.com/ShrekIsLife1/AttalHaterAccount · Tag: v0.2.0-lab5</div>
  <div class="cover-meta">Live Cloud Run URL: https://s3c35c9bd-4d7hbszvwq-as.a.run.app</div>
</div>

<!-- Part 0 -->
<h1 class="part">Answer Part 0 — Team &amp; Evidence Index</h1>
<div class="link-box">
  <div class="link-line"><b>Repository:</b> https://github.com/ShrekIsLife1/AttalHaterAccount</div>
  <div class="link-line"><b>Pull Requests:</b> https://github.com/ShrekIsLife1/AttalHaterAccount/pulls</div>
  <div class="link-line"><b>Deployment Documentation:</b> https://github.com/ShrekIsLife1/AttalHaterAccount/blob/main/docs/labs/lab05/deployment.md</div>
  <div class="link-line"><b>Traceability Test Matrix:</b> https://github.com/ShrekIsLife1/AttalHaterAccount/blob/main/docs/labs/lab05/tests.md</div>
</div>

<h2 class="sub">0.1 Lab 5 Pair Contributions (#16–#25)</h2>
<table>
  <tr><th>Issue</th><th>Title</th><th>Author</th><th>Reviewer</th><th>PR</th></tr>
  <tr><td>#16</td><td>GCP account, project, budget alert &amp; baseline</td><td>Ba</td><td>Cl</td><td>#44</td></tr>
  <tr><td>#17</td><td>Cloud-ready config, probes, .env.example</td><td>Cl</td><td>Ba</td><td>#45</td></tr>
  <tr><td>#18</td><td>Dockerize application &amp; container verification</td><td>Ba</td><td>Cl</td><td>#46</td></tr>
  <tr><td>#19</td><td>CI on Pull Requests (test-and-docker, C-01)</td><td>Cl</td><td>Ba</td><td>#47</td></tr>
  <tr><td>#20</td><td>First deployment to GCP &amp; domain journey (C-04)</td><td>Ba</td><td>Cl</td><td>#48</td></tr>
  <tr><td>#21</td><td>GitHub ↔ GCP (WIF) &amp; failing PR gate (C-02)</td><td>Cl</td><td>Ba</td><td>#50</td></tr>
  <tr><td>#22</td><td>Repeatable deploy pipeline &amp; release commit (C-06)</td><td>Ba</td><td>Cl</td><td>#51</td></tr>
  <tr><td>#23</td><td>Cloud persistence &amp; rollback verification (C-05)</td><td>Cl</td><td>Ba</td><td>#52</td></tr>
  <tr><td>#24</td><td>Cost control: pause/resume Cloud SQL &amp; quota audit</td><td>Ba</td><td>Cl</td><td>#49</td></tr>
  <tr><td>#25</td><td>Final deployment docs &amp; deliverable report</td><td>Cl</td><td>Ba</td><td>#53</td></tr>
</table>

<h2 class="sub">0.2 Commit History on main (feature branches → lab5-staging → main)</h2>
<div class="screenshot-frame">
  <img src="docs/deliverable-2/evidence/01_git_network.png" />
</div>
<div class="caption">Figure 0.1: Git Network Graph — bilateral pair review on lab5-staging before main CD cutover.</div>

<div class="page-break"></div>
<h2 class="sub">0.3 Public Repository Verified in Incognito Mode (R-12)</h2>
<div class="screenshot-frame">
  <img src="docs/deliverable-2/evidence/02_incognito_repo.png" />
</div>
<div class="caption">Figure 0.2: GitHub public repository verified in incognito mode (R-12 compliant).</div>

<!-- Part 1 -->
<div class="page-break"></div>
<h1 class="part">Answer Part 1 — CI and Quality Gate (C-01, C-02)</h1>
<div class="link-box">
  <div class="link-line"><b>CI Workflow:</b> https://github.com/ShrekIsLife1/AttalHaterAccount/blob/main/.github/workflows/ci-docker.yml</div>
</div>

<h2 class="sub">1.1 Check C-01 — Passing Pull Request Verification (test-and-docker)</h2>
<div class="screenshot-frame">
  <img src="docs/deliverable-2/evidence/03_ci_passing.png" />
</div>
<div class="caption">Screenshot 1.1: GitHub Actions CI workflow test-and-docker passing on pull request (C-01).</div>

<h2 class="sub">1.2 Check C-02 — Branch Protection Ruleset (R-09)</h2>
<div class="screenshot-frame">
  <img src="docs/deliverable-2/evidence/04_branch_protection.png" />
</div>
<div class="caption">Screenshot 1.2: Branch protection ruleset on lab5-staging &amp; main requiring test-and-docker.</div>

<div class="page-break"></div>
<h2 class="sub">1.3 Check C-02 — Failing Pull Request Blocked by Merge Gate</h2>
<div class="screenshot-frame">
  <img src="docs/deliverable-2/evidence/05_failing_pr_blocked.png" />
</div>
<div class="caption">Screenshot 1.3: Failing PR blocked by branch protection gate; merge button disabled (C-02).</div>

<h2 class="sub">1.4 Workload Identity Federation (R-06 — environment: demo)</h2>
<div class="screenshot-frame">
  <img src="docs/deliverable-2/evidence/06_wif_env.png" />
</div>
<div class="caption">Screenshot 1.4: Keyless Workload Identity Federation configuration in environment: demo (zero secret keys).</div>

<!-- Part 2 -->
<div class="page-break"></div>
<h1 class="part">Answer Part 2 — Docker and Reproducible Configuration (C-03)</h1>
<div class="link-box">
  <div class="link-line"><b>Dockerfile:</b> https://github.com/ShrekIsLife1/AttalHaterAccount/blob/main/Dockerfile</div>
  <div class="link-line"><b>docker-compose.yml:</b> https://github.com/ShrekIsLife1/AttalHaterAccount/blob/main/docker-compose.yml</div>
  <div class="link-line"><b>.env.example:</b> https://github.com/ShrekIsLife1/AttalHaterAccount/blob/main/.env.example</div>
</div>

<h2 class="sub">2.1 Check C-03 — Unified Production Container Verification (TEST-L5-10..14)</h2>
<div class="screenshot-frame">
  <img src="docs/deliverable-2/evidence/07_docker_container.png" />
</div>
<div class="caption">Screenshot 2.1: Automated container test suite test-container.sh all passing (C-03).</div>

<!-- Part 3 -->
<div class="page-break"></div>
<h1 class="part">Answer Part 3 — GCP Deployment and Persistence (C-04, C-05)</h1>
<div class="link-box">
  <div class="link-line"><b>Live Cloud Run URL:</b> https://s3c35c9bd-4d7hbszvwq-as.a.run.app</div>
</div>

<h2 class="sub">3.1 Check C-04 — Public Health, Readiness &amp; Version Endpoints</h2>
<div class="screenshot-frame">
  <img src="docs/deliverable-2/evidence/08_live_probes.png" />
</div>
<div class="caption">Screenshot 3.1: Live probes (/api/ready 200, /api/version commit SHA) on Cloud Run service.</div>

<div class="page-break"></div>
<h2 class="sub">3.2 Check C-04 — Live Domain Customer Purchasing Journey</h2>
<div class="screenshot-frame">
  <img src="docs/deliverable-2/evidence/09_live_customer_journey.png" />
</div>
<div class="caption">Screenshot 3.2: Customer cart checkout and authoritative pricing on Cloud Run live domain (TEST-L5-21).</div>

<h2 class="sub">3.3 Check C-04 — RBAC &amp; Business Rule Rejections on Live Service</h2>
<div class="screenshot-frame">
  <img src="docs/deliverable-2/evidence/10_live_rbac_rejection.png" />
</div>
<div class="caption">Screenshot 3.3: RBAC 403 Forbidden and business rule 400 Bad Request enforcement on live domain (TEST-L5-22, 23).</div>

<div class="page-break"></div>
<h2 class="sub">3.4 Check C-05 — Cloud Database Persistence &amp; Rollback Verification</h2>
<div class="screenshot-frame">
  <img src="docs/deliverable-2/evidence/11_cloud_persistence.png" />
</div>
<div class="caption">Screenshot 3.4: Order persistence in Cloud SQL across container restart and pause/resume lifecycle (C-05).</div>

<!-- Part 4 -->
<div class="page-break"></div>
<h1 class="part">Answer Part 4 — Repeatable Release Pipeline (C-06)</h1>
<div class="link-box">
  <div class="link-line"><b>CD Pipeline:</b> https://github.com/ShrekIsLife1/AttalHaterAccount/blob/main/.github/workflows/deploy.yml</div>
</div>

<h2 class="sub">4.1 Check C-06 — Automated Continuous Deployment on main (TEST-L5-32..42)</h2>
<div class="screenshot-frame">
  <img src="docs/deliverable-2/evidence/12_cd_deploy_demo.png" />
</div>
<div class="caption">Screenshot 4.1: Automated release pipeline deploy.yml executed on push to main with immutable digest pinning (C-06).</div>

</body>
</html>
"""

story = pymupdf.Story(html=HTML)
writer = pymupdf.DocumentWriter(OUTPUT)
mediabox = pymupdf.paper_rect("a4")
where = mediabox + (45, 45, -45, -45)

more = True
while more:
    dev = writer.begin_page(mediabox)
    more, _ = story.place(where)
    story.draw(dev, None)
    writer.end_page()
writer.close()

# Second pass: add header and Page X / Y footer
doc = pymupdf.open(OUTPUT)
total = len(doc)
for i, page in enumerate(doc, start=1):
    w = page.rect.width
    h = page.rect.height
    if i > 1:
        page.insert_text((w - 235, 28), "UniMerch — Lab 5 — AttalHaterAccount", fontsize=8, color=(0.45, 0.45, 0.45))
    page.insert_text((w / 2 - 22, h - 20), f"Page {i} / {total}", fontsize=8.5, color=(0.35, 0.35, 0.35))
doc.save(OUTPUT + ".tmp")
doc.close()

os.replace(OUTPUT + ".tmp", OUTPUT)
print(f"Generated {OUTPUT} ({total} pages) with all 12 evidence screenshots!")
