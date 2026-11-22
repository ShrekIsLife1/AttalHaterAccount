#!/usr/bin/env python3
"""
Generate ultra-simple deliverable-1.odt matching strictly the Lab 3 report style:
- Clean minimal text
- Direct GitHub links
- Framed dashed boxes for links and embedded screenshots
"""
import os, zipfile

odt_path = "docs/deliverable-1/deliverable-1.odt"

# Images to embed
img_arch = "docs/deliverable-1/evidence/issue-03_architecture-diagram.png"
img_er = "docs/deliverable-1/evidence/issue-03_er-diagram.png"
img_seed = "docs/deliverable-1/evidence/issue-06_seed_terminal.png"
img_pers = "docs/deliverable-1/evidence/issue-06_persistence_test.png"

with open(img_arch, "rb") as f:
    arch_bytes = f.read()

with open(img_er, "rb") as f:
    er_bytes = f.read()

with open(img_seed, "rb") as f:
    seed_bytes = f.read()

with open(img_pers, "rb") as f:
    pers_bytes = f.read()

manifest_xml = """<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.3">
 <manifest:file-entry manifest:full-path="/" manifest:version="1.3" manifest:media-type="application/vnd.oasis.opendocument.text"/>
 <manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>
 <manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml"/>
 <manifest:file-entry manifest:full-path="meta.xml" manifest:media-type="text/xml"/>
 <manifest:file-entry manifest:full-path="Pictures/issue-03_architecture-diagram.png" manifest:media-type="image/png"/>
 <manifest:file-entry manifest:full-path="Pictures/issue-03_er-diagram.png" manifest:media-type="image/png"/>
 <manifest:file-entry manifest:full-path="Pictures/issue-06_seed_terminal.png" manifest:media-type="image/png"/>
 <manifest:file-entry manifest:full-path="Pictures/issue-06_persistence_test.png" manifest:media-type="image/png"/>
</manifest:manifest>
"""

meta_xml = """<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" xmlns:dc="http://purl.org/dc/elements/1.1/" office:version="1.3">
 <office:meta>
  <dc:title>Project Deliverable 1 — UniMerch Store</dc:title>
  <dc:creator>Clément Dominique Delrieu &amp; Baptiste Carré</dc:creator>
 </office:meta>
</office:document-meta>
"""

styles_xml = """<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" office:version="1.3">
 <office:styles>
  <style:default-style style:family="paragraph">
   <style:text-properties fo:font-size="10.5pt" fo:color="#222222" style:font-name="Liberation Sans"/>
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
   <style:paragraph-properties fo:text-align="center" fo:margin-top="35pt" fo:margin-bottom="15pt"/>
   <style:text-properties fo:font-size="24pt" fo:font-weight="bold" fo:color="#0b6623"/>
  </style:style>
  <style:style style:name="SubtitleStyle" style:family="paragraph">
   <style:paragraph-properties fo:text-align="center" fo:margin-bottom="12pt"/>
   <style:text-properties fo:font-size="14pt" fo:font-weight="bold" fo:color="#222222"/>
  </style:style>
  <style:style style:name="AuthorStyle" style:family="paragraph">
   <style:paragraph-properties fo:text-align="center" fo:margin-bottom="6pt"/>
   <style:text-properties fo:font-size="11pt" fo:font-weight="bold" fo:color="#333333"/>
  </style:style>
  <style:style style:name="RepoStyle" style:family="paragraph">
   <style:paragraph-properties fo:text-align="center" fo:margin-bottom="40pt"/>
   <style:text-properties fo:font-size="10pt" fo:color="#0056b3"/>
  </style:style>
  <style:style style:name="SectionTitle" style:family="paragraph">
   <style:paragraph-properties fo:margin-top="22pt" fo:margin-bottom="6pt" fo:border-bottom="1.5pt solid #0b6623" fo:padding-bottom="3pt"/>
   <style:text-properties fo:font-size="15pt" fo:font-weight="bold" fo:color="#0b6623"/>
  </style:style>
  <style:style style:name="SubsectionTitle" style:family="paragraph">
   <style:paragraph-properties fo:margin-top="14pt" fo:margin-bottom="4pt"/>
   <style:text-properties fo:font-size="11pt" fo:font-weight="bold" fo:color="#222222"/>
  </style:style>
  <style:style style:name="LinkLabel" style:family="paragraph">
   <style:paragraph-properties fo:margin-bottom="6pt"/>
   <style:text-properties fo:font-size="10pt" fo:font-weight="bold" fo:color="#222222"/>
  </style:style>
  <style:style style:name="BoxCell" style:family="table-cell">
   <style:table-cell-properties fo:background-color="#fafafa" fo:padding="12pt" fo:border="1pt dashed #999999"/>
  </style:style>
  <style:style style:name="BoxText" style:family="paragraph">
   <style:paragraph-properties fo:text-align="center" fo:margin-bottom="4pt"/>
   <style:text-properties fo:font-size="9.5pt" fo:color="#0056b3"/>
  </style:style>
 </office:automatic-styles>
 <office:body>
  <office:text>

   <!-- COVER PAGE -->
   <text:p text:style-name="TitleStyle">Project Deliverable 1 — UniMerch: E-Commerce &amp; Ordering System</text:p>
   <text:p text:style-name="SubtitleStyle">Engineering Baseline + Working Sprint 1</text:p>
   <text:p text:style-name="AuthorStyle">Clément Dominique Delrieu — Student ID 69540460016</text:p>
   <text:p text:style-name="AuthorStyle">Baptiste Carré — Student ID 69540460014</text:p>
   <text:p text:style-name="RepoStyle">GitHub repository: https://github.com/ShrekIsLife1/AttalHaterAccount</text:p>

   <!-- ANSWER PART A -->
   <text:p text:style-name="SectionTitle">Answer Part A — SRS and Product Scope (10 pts)</text:p>
   <text:p text:style-name="LinkLabel">Link to docs/srs.md: _______________________________________________________</text:p>
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
   <text:p text:style-name="LinkLabel">Link to docs/features.md: _______________________________________________________</text:p>
   <text:p text:style-name="LinkLabel">Link to docs/traceability.md: ___________________________________________________</text:p>
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
   <text:p text:style-name="LinkLabel">Link to docs/system-sds.md: ___________________________________________________</text:p>
   <text:p text:style-name="SubsectionTitle">C.1 Architecture Diagram — Three-Tier Client-Server Architecture</text:p>
   <table:table table:name="BoxC1">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">
       <draw:frame draw:name="ArchitectureDiagram" text:anchor-type="as-char" svg:width="16.5cm" svg:height="9.0cm">
        <draw:image xlink:href="Pictures/issue-03_architecture-diagram.png" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
       </draw:frame>
      </text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>

   <text:p text:style-name="SubsectionTitle">C.2 Entity-Relationship (ER) Schema Diagram — PostgreSQL Entities &amp; Relations</text:p>
   <table:table table:name="BoxC2">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">
       <draw:frame draw:name="ERDiagram" text:anchor-type="as-char" svg:width="16.5cm" svg:height="10.8cm">
        <draw:image xlink:href="Pictures/issue-03_er-diagram.png" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
       </draw:frame>
      </text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>

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
   <text:p text:style-name="LinkLabel">Link to docs/sprints/plan.md: ___________________________________________________</text:p>
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
   <text:p text:style-name="LinkLabel">Link to docs/sprints/sprint-1/: _________________________________________________</text:p>
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

   <!-- ANSWER PART F -->
   <text:p text:style-name="SectionTitle">Answer Part F — Working Sprint 1 and Verification (20 pts)</text:p>
   <text:p text:style-name="LinkLabel">Link to README.md setup guide: __________________________________________________</text:p>
   
   <text:p text:style-name="SubsectionTitle">F.1 Database Scaffold &amp; Idempotent Seeding Execution (Issue #6 / AC-17)</text:p>
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

   <text:p text:style-name="SubsectionTitle">F.2 Automated Persistence &amp; Database Integrity Suite (AC-17 / TEST-21)</text:p>
   <table:table table:name="BoxF2">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">
       <draw:frame draw:name="PersistenceTestTerminal" text:anchor-type="as-char" svg:width="16.5cm" svg:height="8.4cm">
        <draw:image xlink:href="Pictures/issue-06_persistence_test.png" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
       </draw:frame>
      </text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>

   <text:p text:style-name="SubsectionTitle">F.3 Program Demonstrations (Screenshots S1 to S10)</text:p>
   <table:table table:name="BoxF3">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">[Working UI Scenarios S1 to S10: Login, Catalog, Cart/Checkout, My Orders, Operator Queue, Order Accept, 409 guard, 403/404 restrictions]</text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>

   <text:p text:style-name="SubsectionTitle">F.4 Engineering Workflow &amp; Contribution History</text:p>
   <table:table table:name="BoxF4">
    <table:table-column/>
    <table:table-row>
     <table:table-cell table:style-name="BoxCell">
      <text:p text:style-name="BoxText">https://github.com/ShrekIsLife1/AttalHaterAccount/pulls?q=is%3Apr</text:p>
      <text:p text:style-name="BoxText">https://github.com/ShrekIsLife1/AttalHaterAccount/commits/sprint1-staging</text:p>
     </table:table-cell>
    </table:table-row>
   </table:table>

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
    z.writestr("Pictures/issue-03_architecture-diagram.png", arch_bytes)
    z.writestr("Pictures/issue-03_er-diagram.png", er_bytes)
    z.writestr("Pictures/issue-06_seed_terminal.png", seed_bytes)
    z.writestr("Pictures/issue-06_persistence_test.png", pers_bytes)

print(f"Generated ultra-simple Lab 3 report at {odt_path}")
