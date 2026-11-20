#!/usr/bin/env python3
"""
Generate docs/deliverable-1/deliverable-1.odt
Matching the clean, visual, evidence-index style from Lab 3 report:
- Concise text and clear section headers
- Direct links to repository docs
- Framed placeholder boxes for screenshots and execution outputs
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

    # --- Styles (inspired by TokTickIT Lab 3 Report) ---
    # Title style
    title_style = Style(name="CoverTitle", family="paragraph")
    title_style.addElement(ParagraphProperties(textalign="center", margintop="40pt", marginbottom="15pt"))
    title_style.addElement(TextProperties(fontsize="24pt", fontweight="bold", fontfamily="Liberation Sans", color="#0b6623"))
    doc.styles.addElement(title_style)

    subtitle_style = Style(name="CoverSubtitle", family="paragraph")
    subtitle_style.addElement(ParagraphProperties(textalign="center", marginbottom="20pt"))
    subtitle_style.addElement(TextProperties(fontsize="15pt", fontweight="bold", fontfamily="Liberation Sans", color="#222222"))
    doc.styles.addElement(subtitle_style)

    author_style = Style(name="CoverAuthor", family="paragraph")
    author_style.addElement(ParagraphProperties(textalign="center", marginbottom="6pt"))
    author_style.addElement(TextProperties(fontsize="11pt", fontweight="bold", fontfamily="Liberation Sans", color="#333333"))
    doc.styles.addElement(author_style)

    repo_style = Style(name="CoverRepo", family="paragraph")
    repo_style.addElement(ParagraphProperties(textalign="center", marginbottom="30pt"))
    repo_style.addElement(TextProperties(fontsize="10pt", fontfamily="Liberation Sans", color="#0056b3"))
    doc.styles.addElement(repo_style)

    # Section Title (e.g. "Answer Part A — SRS and Scope")
    part_title_style = Style(name="PartTitle", family="paragraph")
    part_title_style.addElement(ParagraphProperties(margintop="20pt", marginbottom="6pt", borderbottom="1.5pt solid #0b6623", padding="2pt"))
    part_title_style.addElement(TextProperties(fontsize="15pt", fontweight="bold", fontfamily="Liberation Sans", color="#0b6623"))
    doc.styles.addElement(part_title_style)

    # Subsection Title (e.g. "A.1 Rendered docs/srs.md")
    sub_title_style = Style(name="SubTitle", family="paragraph")
    sub_title_style.addElement(ParagraphProperties(margintop="12pt", marginbottom="4pt"))
    sub_title_style.addElement(TextProperties(fontsize="11pt", fontweight="bold", fontfamily="Liberation Sans", color="#222222"))
    doc.styles.addElement(sub_title_style)

    # Link / Metadata line
    link_style = Style(name="MetaLink", family="paragraph")
    link_style.addElement(ParagraphProperties(marginbottom="8pt"))
    link_style.addElement(TextProperties(fontsize="10pt", fontfamily="Liberation Sans", color="#333333"))
    doc.styles.addElement(link_style)

    # Body paragraph
    body_style = Style(name="SimpleBody", family="paragraph")
    body_style.addElement(ParagraphProperties(marginbottom="6pt"))
    body_style.addElement(TextProperties(fontsize="10pt", fontfamily="Liberation Sans", color="#333333"))
    doc.styles.addElement(body_style)

    # Screenshot / Evidence Container Box (dashed border like Lab 3)
    box_cell_style = Style(name="EvidenceBoxCell", family="table-cell")
    box_cell_style.addElement(TableCellProperties(
        backgroundcolor="#fafafa",
        padding="15pt",
        border="1pt dashed #999999"
    ))
    doc.styles.addElement(box_cell_style)

    box_para_style = Style(name="EvidenceBoxPara", family="paragraph")
    box_para_style.addElement(ParagraphProperties(textalign="center", marginbottom="0pt"))
    box_para_style.addElement(TextProperties(fontsize="10pt", fontfamily="Liberation Sans", color="#0056b3"))
    doc.styles.addElement(box_para_style)

    def add_evidence_box(content_text):
        table = Table()
        table.addElement(TableColumn())
        row = TableRow()
        cell = TableCell(stylename=box_cell_style)
        cell.addElement(P(stylename=box_para_style, text=content_text))
        row.addElement(cell)
        table.addElement(row)
        doc.text.addElement(table)
        doc.text.addElement(P(stylename=body_style, text=""))

    # ================= PAGE 1 : COVER =================
    doc.text.addElement(P(stylename=title_style, text="Project Deliverable 1 — UniMerch Campus Store\nOrdering System & Engineering Baseline"))
    doc.text.addElement(P(stylename=subtitle_style, text="CPE 334 — Introduction to Software Engineering in the Age of AI Agents\nSemester 1/2026 — Theme 4: E-Commerce or Ordering System"))
    doc.text.addElement(P(stylename=author_style, text="Clément Dominique Delrieu — Student ID 69540460016\nPartner: Ba — Student ID: ..."))
    doc.text.addElement(P(stylename=repo_style, text="GitHub repository: https://github.com/ShrekIsLife1/AttalHaterAccount\nSprint Staging: https://github.com/ShrekIsLife1/AttalHaterAccount/tree/sprint1-staging"))

    # ================= NAVIGATION TABLE =================
    doc.text.addElement(P(stylename=part_title_style, text="Navigation Index"))
    doc.text.addElement(P(stylename=link_style, text="Repository: https://github.com/ShrekIsLife1/AttalHaterAccount"))
    doc.text.addElement(P(stylename=link_style, text="Project Board: https://github.com/ShrekIsLife1/AttalHaterAccount/projects"))
    doc.text.addElement(P(stylename=link_style, text="Sprint 1 Staging Branch: https://github.com/ShrekIsLife1/AttalHaterAccount/tree/sprint1-staging"))
    doc.text.addElement(P(stylename=body_style, text=""))

    # ================= PART A =================
    doc.text.addElement(P(stylename=part_title_style, text="Answer Part A — SRS and Product Scope (10 pts)"))
    doc.text.addElement(P(stylename=link_style, text="Link to docs/srs.md: https://github.com/ShrekIsLife1/AttalHaterAccount/blob/sprint1-staging/docs/srs.md"))

    doc.text.addElement(P(stylename=sub_title_style, text="A.1 Chosen Context & Problem Statement"))
    doc.text.addElement(P(
        stylename=body_style,
        text="Context: UniMerch Campus Store (on-campus official merchandise shop for university students and staff).\n"
             "Problem: Counter congestion during peak periods, untracked inventory leading to stockout rejections, manual paper orders, and price tag discrepancies.\n"
             "Scope: S1 Auth & baseline ordering; S2 Catalog management & fulfillment; S3 Analytics & hardening. Real payment gateways and external courier APIs are strictly excluded."
    ))

    doc.text.addElement(P(stylename=sub_title_style, text="A.2 Rendered docs/srs.md — Actors, FR-01…13, BR-01…08, NFR-01…06, Decisions"))
    add_evidence_box("https://github.com/ShrekIsLife1/AttalHaterAccount/blob/sprint1-staging/docs/srs.md")

    # ================= PART B (Placeholder for #2) =================
    doc.text.addElement(P(stylename=part_title_style, text="Answer Part B — Feature Inventory and Traceability (10 pts)"))
    doc.text.addElement(P(stylename=link_style, text="Link to docs/features.md & docs/traceability.md: [Issue #2]"))
    doc.text.addElement(P(stylename=sub_title_style, text="B.1 Rendered Traceability Matrix (FR/BR/NFR -> Features -> Sprint 1/2/3)"))
    add_evidence_box("[Placeholder: Link to docs/traceability.md + Coverage table]")

    # ================= PART C (Placeholder for #3) =================
    doc.text.addElement(P(stylename=part_title_style, text="Answer Part C — System-Level SDS (15 pts)"))
    doc.text.addElement(P(stylename=link_style, text="Link to docs/system-sds.md: [Issue #3]"))
    doc.text.addElement(P(stylename=sub_title_style, text="C.1 Architecture & ER Diagrams"))
    add_evidence_box("[Placeholder: Architecture diagram & ER schema screenshot]")
    doc.text.addElement(P(stylename=sub_title_style, text="C.2 Role / Permission Matrix & Security Lifecycle"))
    add_evidence_box("[Placeholder: Permission matrix & Auth lifecycle]")

    # ================= PART D (Placeholder for #4) =================
    doc.text.addElement(P(stylename=part_title_style, text="Answer Part D — Three-Sprint Plan (5 pts)"))
    doc.text.addElement(P(stylename=link_style, text="Link to docs/sprints/plan.md: [Issue #4]"))
    doc.text.addElement(P(stylename=sub_title_style, text="D.1 Sprint Allocation & Feasibility"))
    add_evidence_box("[Placeholder: Three-sprint roadmap table & Sprint 1 scope justification]")

    # ================= PART E (Placeholder for #5) =================
    doc.text.addElement(P(stylename=part_title_style, text="Answer Part E — Sprint 1 Engineering Contracts (20 pts)"))
    doc.text.addElement(P(stylename=link_style, text="Link to docs/sprints/sprint-1/: [Issue #5]"))
    doc.text.addElement(P(stylename=sub_title_style, text="E.1 Sprint 1 Feature Contracts (F-01…F-05) & STS Table (TEST-01…26)"))
    add_evidence_box("[Placeholder: Contracts link & Complete Software Test Specification mapping]")

    # ================= PART F (Placeholder for #6 to #15) =================
    doc.text.addElement(P(stylename=part_title_style, text="Answer Part F — Working Sprint 1 and Verification (20 pts)"))
    doc.text.addElement(P(stylename=sub_title_style, text="F.1 Program Demonstrations & Test Outputs (Screenshots S1 to S10)"))
    add_evidence_box("[Placeholder: Screenshots S1 to S10 with dashed borders + test runner outputs]")

    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    print(f"Generated clean Lab 3 style {output_path} successfully!")

if __name__ == "__main__":
    create_deliverable_odt()
