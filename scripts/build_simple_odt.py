#!/usr/bin/env python3
"""
Generate ultra-clean deliverable-1.odt matching strictly the Lab 3 report style:
- Clean minimal text & section titles in deep green (#0b6623)
- Direct GitHub links in dashed border boxes
- Framed dashed boxes for all embedded terminal and UI screenshots
- Fully covering Parts A, B, C, D, E, F with 20 evidence screenshots
"""
import os, zipfile

odt_path = "docs/deliverable-1/deliverable-1.odt"

# All 20 images to embed
images = {
    "arch": "docs/deliverable-1/evidence/issue-03_architecture-diagram.png",
    "er": "docs/deliverable-1/evidence/issue-03_er-diagram.png",
    "seed": "docs/deliverable-1/evidence/issue-06_seed_terminal.png",
    "pers": "docs/deliverable-1/evidence/issue-06_persistence_test.png",
    "auth": "docs/deliverable-1/evidence/issue-07_auth_test.png",
    "catalog": "docs/deliverable-1/evidence/issue-09_catalog_test.png",
    "orders": "docs/deliverable-1/evidence/issue-10_orders_test.png",
    "ui": "docs/deliverable-1/evidence/issue-11_customer-ordering-ui-tests.png",
    "operator": "docs/deliverable-1/evidence/issue-12_operator_test.png",
    "auth_hardening": "docs/deliverable-1/evidence/issue-13_authorization_test.png",
    "e2e": "docs/deliverable-1/evidence/issue-14_e2e_test.png",
    "demo_login": "docs/deliverable-1/evidence/demo-01_login-ui.png",
    "demo_catalog": "docs/deliverable-1/evidence/demo-02_catalog-ui.png",
    "demo_checkout": "docs/deliverable-1/evidence/demo-03_checkout-ui.png",
    "demo_orders": "docs/deliverable-1/evidence/demo-04_my-orders-ui.png",
    "demo_queue": "docs/deliverable-1/evidence/demo-05_operator-queue-ui.png",
    "demo_accept": "docs/deliverable-1/evidence/demo-06_order-accepted-ui.png",
    "demo_security": "docs/deliverable-1/evidence/demo-07_access-guardrails-ui.png",
    "board": "docs/deliverable-1/evidence/issue-15_project-board.png",
    "git_graph": "docs/deliverable-1/evidence/issue-15_git-history.png",
}

img_data = {}
for key, path in images.items():
    with open(path, "rb") as f:
        img_data[key] = f.read()

manifest_entries = "\n".join(
    f' <manifest:file-entry manifest:full-path="Pictures/{os.path.basename(images[k])}" manifest:media-type="image/png"/>'
    for k in images
)

manifest_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.3">
 <manifest:file-entry manifest:full-path="/" manifest:version="1.3" manifest:media-type="application/vnd.oasis.opendocument.text"/>
 <manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>
 <manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml"/>
 <manifest:file-entry manifest:full-path="meta.xml" manifest:media-type="text/xml"/>
{manifest_entries}
</manifest:manifest>
"""

meta_xml = """<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" xmlns:dc="http://purl.org/dc/elements/1.1/" office:version="1.3">
 <office:meta>
  <dc:title>Project Deliverable 1 — UniMerch: E-Commerce and Ordering System</dc:title>
  <dc:creator>Clément Dominique Delrieu &amp; Baptiste Carré</dc:creator>
 </office:meta>
</office:document-meta>
"""

styles_xml = """<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" office:version="1.3">
 <office:styles>
  <style:default-style style:family="paragraph">
   <style:text-properties fo:font-size="10pt" fo:color="#222222" style:font-name="Liberation Sans"/>
  </style:default-style>
 </office:styles>
</office:document-styles>
"""

content_xml = """<?xml version="1.0" encoding="UTF-8"?>
<office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
 xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
 xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
 xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
 xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
 xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
 xmlns:xlink="http://www.w3.org/1999/xlink"
 xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
 office:version="1.3">
 <office:automatic-styles>
  <style:style style:name="TitleStyle" style:family="paragraph">
   <style:paragraph-properties fo:text-align="center" fo:margin-top="25pt" fo:margin-bottom="12pt"/>
   <style:text-properties fo:font-size="22pt" fo:font-weight="bold" fo:color="#0b6623"/>
  </style:style>
  <style:style style:name="SubtitleStyle" style:family="paragraph">
   <style:paragraph-properties fo:text-align="center" fo:margin-bottom="10pt"/>
   <style:text-properties fo:font-size="13pt" fo:font-weight="bold" fo:color="#222222"/>
  </style:style>
  <style:style style:name="AuthorStyle" style:family="paragraph">
   <style:paragraph-properties fo:text-align="center" fo:margin-bottom="4pt"/>
   <style:text-properties fo:font-size="10.5pt" fo:font-weight="bold" fo:color="#333333"/>
  </style:style>
  <style:style style:name="RepoStyle" style:family="paragraph">
   <style:paragraph-properties fo:text-align="center" fo:margin-bottom="25pt"/>
   <style:text-properties fo:font-size="9.5pt" fo:color="#0056b3"/>
  </style:style>
  <style:style style:name="SectionTitle" style:family="paragraph">
   <style:paragraph-properties fo:margin-top="18pt" fo:margin-bottom="6pt" fo:border-bottom="1.5pt solid #0b6623" fo:padding-bottom="3pt"/>
   <style:text-properties fo:font-size="14pt" fo:font-weight="bold" fo:color="#0b6623"/>
  </style:style>
  <style:style style:name="SubsectionTitle" style:family="paragraph">
   <style:paragraph-properties fo:margin-top="12pt" fo:margin-bottom="4pt"/>
   <style:text-properties fo:font-size="10.5pt" fo:font-weight="bold" fo:color="#222222"/>
  </style:style>
  <style:style style:name="BoxCell" style:family="table-cell">
   <style:table-cell-properties fo:background-color="#fafafa" fo:padding="8pt" fo:border="1pt dashed #999999"/>
  </style:style>
  <style:style style:name="BoxText" style:family="paragraph">
   <style:paragraph-properties fo:text-align="center" fo:margin-bottom="2pt"/>
   <style:text-properties fo:font-size="9.5pt" fo:color="#0056b3"/>
  </style:style>
  <style:style style:name="CaptionText" style:family="paragraph">
   <style:paragraph-properties fo:text-align="center" fo:margin-top="4pt" fo:margin-bottom="6pt"/>
   <style:text-properties fo:font-size="8.5pt" fo:color="#555555" fo:font-style="italic"/>
  </style:style>
 </office:automatic-styles>
 <office:body>
  <office:text>

   <!-- COVER PAGE -->
   <text:p text:style-name="TitleStyle">Project Deliverable 1 — UniMerch: E-Commerce &amp; Ordering System</text:p>
   <text:p text:style-name="SubtitleStyle">Engineering Baseline + Working Sprint 1 (Theme 4)</text:p>
   <text:p text:style-name="AuthorStyle">Clément Dominique Delrieu — Student ID 69540460016 (@ClemDelGh)</text:p>
   <text:p text:style-name="AuthorStyle">Baptiste Carré — Student ID 69540460014 (@ShrekIsLife1)</text:p>
   <text:p text:style-name="RepoStyle">GitHub repository: https://github.com/ShrekIsLife1/AttalHaterAccount · Tag: v0.1.0-sprint1</text:p>

   <!-- PART 1: GIT & WORKFLOW -->
   <text:p text:style-name="SectionTitle">Answer Part 1 — Git Use with Engineering Workflow</text:p>
   <table:table table:name="BoxGitRepo">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">Repository: https://github.com/ShrekIsLife1/AttalHaterAccount</text:p>
      <text:p text:style-name="BoxText">Pull Requests: https://github.com/ShrekIsLife1/AttalHaterAccount/pulls?q=is%3Apr</text:p>
      <text:p text:style-name="BoxText">Sprint 1 Branch: https://github.com/ShrekIsLife1/AttalHaterAccount/tree/sprint1-staging</text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>

   <text:p text:style-name="SubsectionTitle">1.1 Commit history on final main branch (14 topic branches → sprint1-staging → main)</text:p>
   <table:table table:name="BoxGitGraph">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">
       <draw:frame draw:name="GitHistoryFrame" text:anchor-type="as-char" svg:width="16.5cm" svg:height="7.8cm">
        <draw:image xlink:href="Pictures/issue-15_git-history.png" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
       </draw:frame>
      </text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>
   <text:p text:style-name="CaptionText">Figure 1.1: Git Network Graph — clean branch isolation, TDD commits, and bilateral peer reviews prior to staging merge.</text:p>

   <text:p text:style-name="SubsectionTitle">1.2 GitHub Project Kanban — all 16 Issues (#0–#15) in Done, In Progress and Review empty</text:p>
   <table:table table:name="BoxKanban">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">
       <draw:frame draw:name="KanbanFrame" text:anchor-type="as-char" svg:width="16.5cm" svg:height="10.2cm">
        <draw:image xlink:href="Pictures/issue-15_project-board.png" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
       </draw:frame>
      </text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>
   <text:p text:style-name="CaptionText">Figure 1.2: GitHub Project Board — 16 closed issues with linked branches, PRs, and assignees.</text:p>

   <text:p text:style-name="SubsectionTitle">1.3 README.md and .gitignore Specification</text:p>
   <table:table table:name="BoxReadme">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">https://github.com/ShrekIsLife1/AttalHaterAccount/blob/sprint1-staging/README.md</text:p>
      <text:p text:style-name="BoxText">https://github.com/ShrekIsLife1/AttalHaterAccount/blob/sprint1-staging/.gitignore</text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>

   <!-- ANSWER PART A -->
   <text:p text:style-name="SectionTitle">Answer Part A — SRS and Product Scope (10 pts)</text:p>
   <text:p text:style-name="SubsectionTitle">A.1 Rendered srs.md — Context, Actors, FR-01…13, BR-01…08, NFR-01…06, Decisions</text:p>
   <table:table table:name="BoxA">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">https://github.com/ShrekIsLife1/AttalHaterAccount/blob/sprint1-staging/docs/srs.md</text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>

   <!-- ANSWER PART B -->
   <text:p text:style-name="SectionTitle">Answer Part B — Feature Inventory and Traceability (10 pts)</text:p>
   <text:p text:style-name="SubsectionTitle">B.1 Rendered features.md &amp; traceability.md — Feature Inventory &amp; RTM Matrix</text:p>
   <table:table table:name="BoxB">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">https://github.com/ShrekIsLife1/AttalHaterAccount/blob/sprint1-staging/docs/features.md</text:p>
      <text:p text:style-name="BoxText">https://github.com/ShrekIsLife1/AttalHaterAccount/blob/sprint1-staging/docs/traceability.md</text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>

   <!-- ANSWER PART C -->
   <text:p text:style-name="SectionTitle">Answer Part C — System-Level SDS (15 pts)</text:p>
   <text:p text:style-name="SubsectionTitle">C.1 Architecture Diagram — Three-Tier Client-Server Architecture</text:p>
   <table:table table:name="BoxC1">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">
       <draw:frame draw:name="ArchitectureDiagram" text:anchor-type="as-char" svg:width="16.5cm" svg:height="8.8cm">
        <draw:image xlink:href="Pictures/issue-03_architecture-diagram.png" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
       </draw:frame>
      </text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>
   <text:p text:style-name="CaptionText">Figure C.1: Three-Tier Client-Server Architecture (React 18 + Express TypeScript + PostgreSQL 16 Prisma).</text:p>

   <text:p text:style-name="SubsectionTitle">C.2 Entity-Relationship (ER) Schema Diagram</text:p>
   <table:table table:name="BoxC2">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">
       <draw:frame draw:name="ERDiagram" text:anchor-type="as-char" svg:width="16.5cm" svg:height="10.5cm">
        <draw:image xlink:href="Pictures/issue-03_er-diagram.png" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
       </draw:frame>
      </text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>
   <text:p text:style-name="CaptionText">Figure C.2: PostgreSQL Relational Schema — User, Session, Product, Order, OrderItem with strict minor unit pricing.</text:p>

   <text:p text:style-name="SubsectionTitle">C.3 Rendered system-sds.md — Stack, UI/API conventions, Role Matrix, Auth, GCP Plan</text:p>
   <table:table table:name="BoxC3">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">https://github.com/ShrekIsLife1/AttalHaterAccount/blob/sprint1-staging/docs/system-sds.md</text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>

   <!-- ANSWER PART D -->
   <text:p text:style-name="SectionTitle">Answer Part D — Three-Sprint Plan (5 pts)</text:p>
   <text:p text:style-name="SubsectionTitle">D.1 Rendered plan.md — Sprint Goals, Feature Allocation &amp; Feasibility</text:p>
   <table:table table:name="BoxD">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">https://github.com/ShrekIsLife1/AttalHaterAccount/blob/sprint1-staging/docs/sprints/plan.md</text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>

   <!-- ANSWER PART E -->
   <text:p text:style-name="SectionTitle">Answer Part E — Sprint 1 Engineering Contracts (20 pts)</text:p>
   <text:p text:style-name="SubsectionTitle">E.1 Rendered Feature Contracts (F-01…F-05), STS Table &amp; Definition of Done</text:p>
   <table:table table:name="BoxE">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">https://github.com/ShrekIsLife1/AttalHaterAccount/blob/sprint1-staging/docs/sprints/sprint-1/F-01-authentication.md</text:p>
      <text:p text:style-name="BoxText">https://github.com/ShrekIsLife1/AttalHaterAccount/blob/sprint1-staging/docs/sprints/sprint-1/F-02-catalog.md</text:p>
      <text:p text:style-name="BoxText">https://github.com/ShrekIsLife1/AttalHaterAccount/blob/sprint1-staging/docs/sprints/sprint-1/F-03-place-order.md</text:p>
      <text:p text:style-name="BoxText">https://github.com/ShrekIsLife1/AttalHaterAccount/blob/sprint1-staging/docs/sprints/sprint-1/F-04-my-orders.md</text:p>
      <text:p text:style-name="BoxText">https://github.com/ShrekIsLife1/AttalHaterAccount/blob/sprint1-staging/docs/sprints/sprint-1/F-05-operator-orders.md</text:p>
      <text:p text:style-name="BoxText">https://github.com/ShrekIsLife1/AttalHaterAccount/blob/sprint1-staging/docs/sprints/sprint-1/sts.md</text:p>
      <text:p text:style-name="BoxText">https://github.com/ShrekIsLife1/AttalHaterAccount/blob/sprint1-staging/docs/sprints/sprint-1/definition-of-done.md</text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>

   <!-- ANSWER PART F: AUTOMATED TESTS -->
   <text:p text:style-name="SectionTitle">Answer Part F — Working Sprint 1 and Automated Verification (20 pts)</text:p>

   <text:p text:style-name="SubsectionTitle">F.1 Database Scaffold &amp; Idempotent Seeding (AC-17 / TEST-21)</text:p>
   <table:table table:name="BoxF1">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">
       <draw:frame draw:name="SeedTerminal" text:anchor-type="as-char" svg:width="16.5cm" svg:height="6.8cm">
        <draw:image xlink:href="Pictures/issue-06_seed_terminal.png" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
       </draw:frame>
      </text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>

   <text:p text:style-name="SubsectionTitle">F.2 Persistence Test Suite (AC-17 / TEST-21)</text:p>
   <table:table table:name="BoxF2a">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">
       <draw:frame draw:name="PersistenceTest" text:anchor-type="as-char" svg:width="16.5cm" svg:height="7.5cm">
        <draw:image xlink:href="Pictures/issue-06_persistence_test.png" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
       </draw:frame>
      </text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>

   <text:p text:style-name="SubsectionTitle">F.3 Authentication &amp; Session RBAC Suite (F-01 / AC-01..04, AC-13 / TEST-01..04, 16)</text:p>
   <table:table table:name="BoxF3">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">
       <draw:frame draw:name="AuthTest" text:anchor-type="as-char" svg:width="16.5cm" svg:height="8.8cm">
        <draw:image xlink:href="Pictures/issue-07_auth_test.png" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
       </draw:frame>
      </text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>

   <text:p text:style-name="SubsectionTitle">F.4 Catalog API Suite (F-02 / AC-05 / TEST-05)</text:p>
   <table:table table:name="BoxF4">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">
       <draw:frame draw:name="CatalogTest" text:anchor-type="as-char" svg:width="16.5cm" svg:height="7.0cm">
        <draw:image xlink:href="Pictures/issue-09_catalog_test.png" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
       </draw:frame>
      </text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>

   <text:p text:style-name="SubsectionTitle">F.5 Orders &amp; Domain Pricing Engine Suite (F-03 / AC-06..10 / TEST-07..12)</text:p>
   <table:table table:name="BoxF5">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">
       <draw:frame draw:name="OrdersTest" text:anchor-type="as-char" svg:width="16.5cm" svg:height="8.8cm">
        <draw:image xlink:href="Pictures/issue-10_orders_test.png" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
       </draw:frame>
      </text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>

   <text:p text:style-name="SubsectionTitle">F.6 Customer Ordering UI Suite — Checkout, My Orders, Catalog (Issue #11 / AC-06..11 / TEST-06, 14)</text:p>
   <table:table table:name="BoxF6">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">
       <draw:frame draw:name="CustomerOrderUITest" text:anchor-type="as-char" svg:width="16.5cm" svg:height="8.0cm">
        <draw:image xlink:href="Pictures/issue-11_customer-ordering-ui-tests.png" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
       </draw:frame>
      </text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>

   <text:p text:style-name="SubsectionTitle">F.7 Operator Queue &amp; Acceptance Suite (Issue #12 / AC-13..16 / TEST-16..20)</text:p>
   <table:table table:name="BoxF7a">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">
       <draw:frame draw:name="OperatorOrdersTest" text:anchor-type="as-char" svg:width="16.5cm" svg:height="8.8cm">
        <draw:image xlink:href="Pictures/issue-12_operator_test.png" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
       </draw:frame>
      </text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>

   <text:p text:style-name="SubsectionTitle">F.8 Authorization Hardening &amp; Cross-Cutting Security Suite (Issue #13 / AC-03, 12, 13, 17 / BR-05, 07, 08)</text:p>
   <table:table table:name="BoxF8a">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">
       <draw:frame draw:name="AuthHardeningTest" text:anchor-type="as-char" svg:width="16.5cm" svg:height="9.5cm">
        <draw:image xlink:href="Pictures/issue-13_authorization_test.png" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
       </draw:frame>
      </text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>

   <text:p text:style-name="SubsectionTitle">F.9 End-to-End Complete Workflow Suite (Issue #14 / AC-19, AC-20 / TEST-24..26)</text:p>
   <table:table table:name="BoxF9a">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">
       <draw:frame draw:name="E2EWorkflowTest" text:anchor-type="as-char" svg:width="16.5cm" svg:height="9.0cm">
        <draw:image xlink:href="Pictures/issue-14_e2e_test.png" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
       </draw:frame>
      </text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>

   <!-- ANSWER PART F: PROGRAM DEMONSTRATIONS WITH UI SCREENS -->
   <text:p text:style-name="SectionTitle">Answer Part F — Program Demonstrations (Working UI Scenarios)</text:p>

   <text:p text:style-name="SubsectionTitle">Scenario S1: Customer Authentication &amp; Role Shell (AC-01, AC-18)</text:p>
   <table:table table:name="BoxDemo1">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">
       <draw:frame draw:name="DemoLoginFrame" text:anchor-type="as-char" svg:width="16.5cm" svg:height="10.2cm">
        <draw:image xlink:href="Pictures/demo-01_login-ui.png" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
       </draw:frame>
      </text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>
   <text:p text:style-name="CaptionText">Screenshot S1: Working Login UI — authenticates customer/operator and sets HttpOnly session cookie without data leak.</text:p>

   <text:p text:style-name="SubsectionTitle">Scenario S2: Merchandise Catalog with Authoritative Prices &amp; Stock Status (AC-05 / TEST-06)</text:p>
   <table:table table:name="BoxDemo2">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">
       <draw:frame draw:name="DemoCatalogFrame" text:anchor-type="as-char" svg:width="16.5cm" svg:height="10.8cm">
        <draw:image xlink:href="Pictures/demo-02_catalog-ui.png" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
       </draw:frame>
      </text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>
   <text:p text:style-name="CaptionText">Screenshot S2: Active catalog cards with integer THB satang formatting, availability badges, and Add to Cart.</text:p>

   <text:p text:style-name="SubsectionTitle">Scenario S3: Multi-Item Cart Review &amp; Authoritative Server Total Calculation (AC-06..10 / BR-01..03)</text:p>
   <table:table table:name="BoxDemo3">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">
       <draw:frame draw:name="DemoCheckoutFrame" text:anchor-type="as-char" svg:width="16.5cm" svg:height="10.0cm">
        <draw:image xlink:href="Pictures/demo-03_checkout-ui.png" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
       </draw:frame>
      </text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>
   <text:p text:style-name="CaptionText">Screenshot S3: Cart checkout table — prices and line totals verified strictly on backend in integer minor units.</text:p>

   <text:p text:style-name="SubsectionTitle">Scenario S4: Order Submission, DB Persistence &amp; Historical Snapshot Verification (AC-06, 10, 11 / BR-04)</text:p>
   <table:table table:name="BoxDemo4">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">
       <draw:frame draw:name="DemoOrdersFrame" text:anchor-type="as-char" svg:width="16.5cm" svg:height="10.4cm">
        <draw:image xlink:href="Pictures/demo-04_my-orders-ui.png" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
       </draw:frame>
      </text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>
   <text:p text:style-name="CaptionText">Screenshot S4: Persisted Order #101 in My Orders — immutable unitPriceAtOrder snapshot preserved after catalog price update.</text:p>

   <text:p text:style-name="SubsectionTitle">Scenario S5: Operator Incoming Orders Queue &amp; Single-Click Accept (AC-14, 15 / F-05)</text:p>
   <table:table table:name="BoxDemo5">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">
       <draw:frame draw:name="DemoQueueFrame" text:anchor-type="as-char" svg:width="16.5cm" svg:height="10.0cm">
        <draw:image xlink:href="Pictures/demo-05_operator-queue-ui.png" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
       </draw:frame>
      </text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>
   <text:p text:style-name="CaptionText">Screenshot S5: Operator incoming queue displaying PLACED orders chronologically with customer email and totals.</text:p>

   <text:p text:style-name="SubsectionTitle">Scenario S6: Order Acceptance State Transition &amp; 409 Conflict Guard (AC-15, 16 / TEST-19, 20)</text:p>
   <table:table table:name="BoxDemo6">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">
       <draw:frame draw:name="DemoAcceptFrame" text:anchor-type="as-char" svg:width="16.5cm" svg:height="10.0cm">
        <draw:image xlink:href="Pictures/demo-06_order-accepted-ui.png" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
       </draw:frame>
      </text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>
   <text:p text:style-name="CaptionText">Screenshot S6: Order #101 transitioned to ACCEPTED; attempting double-acceptance returns HTTP 409 Conflict guard.</text:p>

   <text:p text:style-name="SubsectionTitle">Scenario S7: Security Boundaries — RBAC 403 Forbidden &amp; Ownership Isolation 404 (AC-12, 13 / BR-05, 08)</text:p>
   <table:table table:name="BoxDemo7">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">
       <draw:frame draw:name="DemoSecurityFrame" text:anchor-type="as-char" svg:width="16.5cm" svg:height="10.0cm">
        <draw:image xlink:href="Pictures/demo-07_access-guardrails-ui.png" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
       </draw:frame>
      </text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>
   <text:p text:style-name="CaptionText">Screenshot S7: Enforced security boundaries — Customer restricted from operator queue (403), cross-customer lookup returns 404.</text:p>

  </office:text>
 </office:body>
</office:document-content>
"""

with zipfile.ZipFile(odt_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
    z.writestr("mimetype", "application/vnd.oasis.opendocument.text", compress_type=zipfile.ZIP_STORED)
    z.writestr("META-INF/manifest.xml", manifest_xml)
    z.writestr("meta.xml", meta_xml)
    z.writestr("styles.xml", styles_xml)
    z.writestr("content.xml", content_xml)
    for key, path in images.items():
        z.writestr(f"Pictures/{os.path.basename(path)}", img_data[key])

print(f"Generated ultra-simple Lab 3 report with 20 evidence screenshots at {odt_path}")
