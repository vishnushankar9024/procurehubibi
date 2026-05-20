#!/usr/bin/env python3
"""
Generate DAMAC PMWeb AI Governance & Intelligence Layer executive deck.
Premium consulting style — black & red CMCS brand theme.
"""

from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE, MSO_CONNECTOR_TYPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

# ── Brand palette (CMCS: black + red) ──────────────────────────────────────
BLACK = RGBColor(0x0A, 0x0A, 0x0A)
CHARCOAL = RGBColor(0x1A, 0x1A, 0x1A)
CARD = RGBColor(0x22, 0x22, 0x22)
CARD_LIGHT = RGBColor(0x2E, 0x2E, 0x2E)
RED = RGBColor(0xE3, 0x18, 0x37)
RED_DARK = RGBColor(0xB0, 0x12, 0x28)
RED_SOFT = RGBColor(0xFF, 0x4D, 0x6A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
SILVER = RGBColor(0xC8, 0xC8, 0xC8)
MUTED = RGBColor(0x9A, 0x9A, 0x9A)
GOLD = RGBColor(0xD4, 0xAF, 0x37)

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
MARGIN = Inches(0.55)


def prs_blank() -> Presentation:
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    return prs


def add_blank_slide(prs: Presentation):
    return prs.slides.add_slide(prs.slide_layouts[6])


def fill_bg(slide, color: RGBColor = BLACK):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def rect(slide, left, top, width, height, fill: RGBColor, line: RGBColor | None = None, radius=False):
    shape_type = MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE if radius else MSO_AUTO_SHAPE_TYPE.RECTANGLE
    s = slide.shapes.add_shape(shape_type, left, top, width, height)
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    if line:
        s.line.color.rgb = line
        s.line.width = Pt(1)
    else:
        s.line.fill.background()
    return s


def accent_bar(slide, top=Inches(0), height=Inches(0.06)):
    rect(slide, Inches(0), top, SLIDE_W, height, RED)


def red_swoosh(slide, left, top, width, height):
    """Decorative CMCS-style arc accent."""
    s = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.OVAL, left, top, width, height)
    s.fill.background()
    s.line.color.rgb = RED
    s.line.width = Pt(2.5)
    return s


def textbox(slide, left, top, width, height, text: str, size=14, bold=False,
            color=WHITE, align=PP_ALIGN.LEFT, font="Calibri"):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.name = font
    p.font.color.rgb = color
    p.alignment = align
    return tb


def bullets(slide, left, top, width, height, items: list[str], size=13, color=SILVER, spacing=1.15):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = item
        p.level = 0
        p.font.size = Pt(size)
        p.font.name = "Calibri"
        p.font.color.rgb = color
        p.space_after = Pt(6)
        p.line_spacing = spacing
    return tb


def section_header(slide, section_num: str, title: str, subtitle: str = ""):
    fill_bg(slide)
    accent_bar(slide)
    red_swoosh(slide, Inches(11.2), Inches(0.3), Inches(1.8), Inches(1.2))
    textbox(slide, MARGIN, Inches(0.35), Inches(3), Inches(0.4), section_num, 11, True, RED)
    textbox(slide, MARGIN, Inches(1.1), Inches(11), Inches(0.9), title, 36, True, WHITE)
    if subtitle:
        textbox(slide, MARGIN, Inches(2.0), Inches(10), Inches(0.6), subtitle, 16, False, MUTED)


def footer(slide, label: str = "DAMAC | Enterprise AI Governance & Intelligence Layer for PMWeb"):
    rect(slide, Inches(0), Inches(7.05), SLIDE_W, Inches(0.45), CHARCOAL)
    textbox(slide, MARGIN, Inches(7.12), Inches(8), Inches(0.3), label, 9, False, MUTED)
    textbox(slide, Inches(10.5), Inches(7.12), Inches(2.5), Inches(0.3), "CONFIDENTIAL", 9, True, RED, PP_ALIGN.RIGHT)


def card(slide, left, top, w, h, title: str, body: list[str], icon: str = ""):
    rect(slide, left, top, w, h, CARD, RED, radius=True)
    rect(slide, left, top, Inches(0.08), h, RED)
    y = top + Inches(0.2)
    if icon:
        textbox(slide, left + Inches(0.25), y, Inches(0.5), Inches(0.4), icon, 20, False, RED)
        y += Inches(0.35)
    textbox(slide, left + Inches(0.25), y, w - Inches(0.4), Inches(0.45), title, 14, True, WHITE)
    bullets(slide, left + Inches(0.25), y + Inches(0.5), w - Inches(0.4), h - Inches(0.7), body, 11, SILVER)


def add_table(slide, left, top, width, height, headers: list[str], rows: list[list[str]],
              header_fill=RED, row_fill=CARD, alt_fill=CARD_LIGHT, font_size=9):
    n_rows = len(rows) + 1
    n_cols = len(headers)
    tbl = slide.shapes.add_table(n_rows, n_cols, left, top, width, height).table

    col_w = int(width / n_cols)
    for c in range(n_cols):
        tbl.columns[c].width = col_w

    for c, h in enumerate(headers):
        cell = tbl.cell(0, c)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = header_fill
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(font_size)
            p.font.bold = True
            p.font.color.rgb = WHITE
            p.font.name = "Calibri"
            p.alignment = PP_ALIGN.CENTER

    for r, row in enumerate(rows):
        fill = row_fill if r % 2 == 0 else alt_fill
        for c, val in enumerate(row):
            cell = tbl.cell(r + 1, c)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = fill
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(font_size - 1)
                p.font.color.rgb = SILVER
                p.font.name = "Calibri"
    return tbl


def arrow_down(slide, cx, y1, y2):
    slide.shapes.add_connector(
        MSO_CONNECTOR_TYPE.STRAIGHT, cx, y1, cx, y2
    ).line.color.rgb = RED


def arch_box(slide, left, top, w, h, label: str, sub: str = ""):
    rect(slide, left, top, w, h, CARD, RED, radius=True)
    textbox(slide, left + Inches(0.1), top + Inches(0.15), w - Inches(0.2), Inches(0.35),
             label, 12, True, WHITE, PP_ALIGN.CENTER)
    if sub:
        textbox(slide, left + Inches(0.05), top + Inches(0.5), w - Inches(0.1), h - Inches(0.55),
                sub, 9, False, MUTED, PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE BUILDERS
# ═══════════════════════════════════════════════════════════════════════════

def slide_title(prs):
    s = add_blank_slide(prs)
    fill_bg(s)
    accent_bar(s, Inches(0), Inches(0.08))
    red_swoosh(s, Inches(-0.3), Inches(1.5), Inches(4), Inches(3.5))
    red_swoosh(s, Inches(9.5), Inches(4.5), Inches(4), Inches(2.5))
    rect(s, MARGIN, Inches(2.2), Inches(0.12), Inches(2.8), RED)
    textbox(s, Inches(0.85), Inches(2.0), Inches(11), Inches(1.2),
            "Enterprise AI Governance &\nIntelligence Layer for PMWeb", 40, True, WHITE)
    textbox(s, Inches(0.85), Inches(4.0), Inches(10), Inches(0.6),
            "Governed AI Orchestration — Not Direct AI-to-Database Connectivity", 18, False, RED_SOFT)
    textbox(s, Inches(0.85), Inches(4.8), Inches(10), Inches(0.5),
            "Executive Proposal for DAMAC Leadership & Technology Stakeholders", 14, False, MUTED)
    textbox(s, Inches(0.85), Inches(6.2), Inches(4), Inches(0.4), "Prepared for: DAMAC", 12, False, SILVER)
    textbox(s, Inches(5.5), Inches(6.2), Inches(4), Inches(0.4), "CMCS | May 2026", 12, False, SILVER, PP_ALIGN.RIGHT)
    footer(s, "CMCS | DAMAC AI Transformation Proposal")


def slide_agenda(prs):
    s = add_blank_slide(prs)
    section_header(s, "OVERVIEW", "Agenda", "Boardroom executive briefing structure")
    items = [
        ("01", "Executive Summary & Current vs Future State"),
        ("02", "DAMAC PMWeb Use Cases"),
        ("03", "Why Direct AI-to-PMWeb Is Risky"),
        ("04", "Recommended Enterprise Architecture"),
        ("05", "AI Model Comparison & Recommendation"),
        ("06", "Enterprise Pricing & Cost Optimization"),
        ("07", "Phased Implementation Strategy"),
        ("08", "Security, Governance & Controls"),
        ("09", "Future Vision — DAMAC AI Governance Platform"),
        ("10", "Final Recommendation"),
    ]
    y = Inches(2.5)
    for num, title in items:
        rect(s, MARGIN, y, Inches(0.55), Inches(0.42), RED, radius=True)
        textbox(s, MARGIN + Inches(0.12), y + Inches(0.05), Inches(0.4), Inches(0.35), num, 12, True, WHITE, PP_ALIGN.CENTER)
        textbox(s, MARGIN + Inches(0.75), y + Inches(0.06), Inches(9), Inches(0.35), title, 13, False, SILVER)
        y += Inches(0.48)
    footer(s)


def slide_exec_summary(prs):
    s = add_blank_slide(prs)
    section_header(s, "SECTION 01", "Executive Summary",
                   "Transforming PMWeb with governed enterprise AI — not uncontrolled connectivity")
    bullets(s, MARGIN, Inches(2.6), Inches(11.5), Inches(4.2), [
        "DAMAC's procurement and commercial workflows on PMWeb generate high-value data trapped in documents, tenders, and contracts.",
        "Manual summarization, tender analysis, and executive reporting create bottlenecks and visibility gaps.",
        "AI can accelerate decisions — but only when deployed as a governed intelligence layer over enterprise truth.",
        "Recommended path: Enterprise AI Orchestration Layer between PMWeb APIs and Claude/OpenAI models.",
        "Start with contract intelligence POC; scale to DAMAC AI Governance Platform.",
    ], 14, SILVER)
    rect(s, Inches(9.5), Inches(2.8), Inches(3.2), Inches(3.5), CARD, RED, radius=True)
    textbox(s, Inches(9.7), Inches(3.0), Inches(2.8), Inches(0.5), "Strategic Thesis", 14, True, RED)
    textbox(s, Inches(9.7), Inches(3.6), Inches(2.8), Inches(2.5),
            '"AI should explain enterprise truth,\nnot derive uncontrolled truth."', 13, True, WHITE, PP_ALIGN.CENTER)
    footer(s)


def slide_challenges(prs):
    s = add_blank_slide(prs)
    section_header(s, "SECTION 01", "Current Challenges", "Operational friction across procurement & commercial management")
    challenges = [
        ("Manual Effort", "Heavy manual work in procurement/commercial workflows — bid packs, BAFO comparisons, CO approvals."),
        ("No Executive Summaries", "Leadership lacks concise, trusted summaries of tenders, contracts, and commitments."),
        ("Slow Tender Cycles", "Tender decision cycles delayed by document review, vendor comparison, and deviation analysis."),
        ("Limited Visibility", "Management cannot query project/package status, unit mix, or vendor insights on demand."),
        ("Governance Gap", "No enterprise AI layer — risk of shadow AI tools and ungoverned database access."),
    ]
    positions = [
        (MARGIN, Inches(2.5)), (Inches(4.6), Inches(2.5)), (Inches(8.7), Inches(2.5)),
        (MARGIN, Inches(4.6)), (Inches(4.6), Inches(4.6)),
    ]
    icons = ["⚙", "📊", "⏱", "👁", "⚠"]
    for (left, top), (title, body), icon in zip(positions, challenges, icons):
        card(s, left, top, Inches(3.7), Inches(1.85), title, [body], icon)
    footer(s)


def slide_current_vs_future(prs):
    s = add_blank_slide(prs)
    section_header(s, "SECTION 01", "Current State vs Future State",
                   "Visual transformation narrative for boardroom stakeholders")
    # Current
    rect(s, MARGIN, Inches(2.4), Inches(5.8), Inches(4.2), CARD, MUTED, radius=True)
    textbox(s, MARGIN + Inches(0.3), Inches(2.6), Inches(5), Inches(0.4), "CURRENT STATE", 16, True, MUTED)
    bullets(s, MARGIN + Inches(0.3), Inches(3.1), Inches(5.2), Inches(3.3), [
        "Manual contract & tender summarization",
        "Fragmented document repositories",
        "Reactive management reporting",
        "Siloed PMWeb data access",
        "No AI audit trail or governance",
        "Shadow AI experimentation risk",
    ], 12, SILVER)
    # Arrow
    textbox(s, Inches(6.55), Inches(4.2), Inches(0.8), Inches(0.6), "→", 48, True, RED, PP_ALIGN.CENTER)
    # Future
    rect(s, Inches(7.0), Inches(2.4), Inches(5.8), Inches(4.2), CARD, RED, radius=True)
    textbox(s, Inches(7.3), Inches(2.6), Inches(5), Inches(0.4), "FUTURE STATE", 16, True, RED)
    bullets(s, Inches(7.3), Inches(3.1), Inches(5.2), Inches(3.3), [
        "AI-assisted governance & summarization",
        "Enterprise Knowledge Layer + RAG",
        "Executive AI chatbot with citations",
        "Governed API orchestration to PMWeb",
        "Full audit, RBAC & prompt logging",
        "DAMAC AI Governance Platform",
    ], 12, WHITE)
    textbox(s, MARGIN, Inches(6.55), Inches(12), Inches(0.35),
            "Opportunity: AI-assisted governance — not ungoverned AI connectivity", 12, True, RED_SOFT, PP_ALIGN.CENTER)
    footer(s)


def slide_use_cases_intro(prs):
    s = add_blank_slide(prs)
    section_header(s, "SECTION 02", "DAMAC PMWeb Use Cases",
                   "High-value AI scenarios aligned to procurement, commercial & management needs")
    card(s, MARGIN, Inches(2.5), Inches(3.7), Inches(3.8), "Commitment / CO Approval", [
        "Bid summarization & BAFO comparison",
        "Technical recommendations & benchmarking",
        "Deviations, exclusions & T&C summaries",
    ], "✓")
    card(s, Inches(4.85), Inches(2.5), Inches(3.7), Inches(3.8), "Contract Intelligence", [
        "AI clause extraction & summarization",
        "Auto-population of PMWeb fields",
        "Contract intelligence repository",
    ], "📄")
    card(s, Inches(8.55), Inches(2.5), Inches(3.7), Inches(3.8), "Management AI Chatbot", [
        "Project & package status queries",
        "Building config, unit mix, awards",
        "Vendor & subcontractor insights",
    ], "💬")
    footer(s)


def slide_commitment_use_case(prs):
    s = add_blank_slide(prs)
    section_header(s, "SECTION 02", "Use Case 1 — Commitment / CO Approval Summarization",
                   "Accelerate procurement decisions with governed AI intelligence")
    workflows = [
        ("Bid Summarization", "Structured executive summaries from tender submissions"),
        ("BAFO Vendor Comparison", "Side-by-side commercial & technical comparison matrices"),
        ("Technical Recommendations", "AI-assisted evaluation summaries with citations"),
        ("Historical Benchmarking", "Compare against prior awards and market benchmarks"),
        ("Deviations / Exclusions", "Highlight material deviations from standard terms"),
        ("Contract T&Cs Summary", "Condensed terms for approval committees"),
    ]
    x, y = MARGIN, Inches(2.5)
    for i, (t, b) in enumerate(workflows):
        col, row = i % 3, i // 3
        card(s, x + col * Inches(4.05), y + row * Inches(2.05), Inches(3.85), Inches(1.85), t, [b], "▸")
    # workflow diagram center bottom
    rect(s, MARGIN, Inches(6.35), Inches(12.2), Inches(0.55), CHARCOAL, RED, radius=True)
    textbox(s, MARGIN + Inches(0.2), Inches(6.42), Inches(11.8), Inches(0.4),
            "PMWeb Tender → Document Ingestion → RAG → AI Summarization → Human Approval → PMWeb Update",
            11, False, SILVER, PP_ALIGN.CENTER)
    footer(s)


def slide_contract_use_case(prs):
    s = add_blank_slide(prs)
    section_header(s, "SECTION 02", "Use Case 2 — AI-Assisted Contract Summarization",
                   "Reduce manual effort while preserving enterprise control")
    card(s, MARGIN, Inches(2.5), Inches(5.5), Inches(2.2), "AI Clause Extraction", [
        "Identify key clauses: payment, LDs, warranties, termination",
        "Map extracted data to PMWeb contract schema fields",
    ], "§")
    card(s, MARGIN, Inches(4.9), Inches(5.5), Inches(2.0), "Auto-Population of PMWeb Fields", [
        "Structured outputs feed governed API writes — never raw AI-to-DB",
        "Human-in-the-loop validation before PMWeb record updates",
    ], "↻")
    card(s, Inches(6.3), Inches(2.5), Inches(6.4), Inches(4.4), "Contract Intelligence Workflow", [
        "1. Upload contract PDF to secure ingestion pipeline",
        "2. OCR + chunking + vector indexing (Enterprise Knowledge Layer)",
        "3. Claude document intelligence extracts clauses & summaries",
        "4. Orchestration validates schema, applies RBAC",
        "5. Analyst reviews with citation-linked UI",
        "6. Approved data synced to PMWeb via API",
        "",
        "Outcome: 60–80% reduction in manual summarization effort",
    ], "◆")
    footer(s)


def slide_chatbot_use_case(prs):
    s = add_blank_slide(prs)
    section_header(s, "SECTION 02", "Use Case 3 — AI Chatbot for Management Queries",
                   "Executive-grade conversational access to governed PMWeb intelligence")
    queries = [
        ("Project / Package Status", "Real-time pipeline view across developments"),
        ("Building Configuration", "Typology, floors, areas, specifications"),
        ("Unit Mix", "Inventory breakdown by type, size, price band"),
        ("Design Parameters", "Key design criteria and approval status"),
        ("Awarded Values", "Contract values, variations, commitment status"),
        ("Vendor / Subcontractor Insights", "Performance, awards, risk flags"),
    ]
    for i, (t, b) in enumerate(queries):
        col = i % 3
        row = i // 3
        card(s, MARGIN + col * Inches(4.05), Inches(2.5) + row * Inches(2.05), Inches(3.85), Inches(1.85), t, [b], "◉")
    rect(s, MARGIN, Inches(6.35), Inches(12.2), Inches(0.55), CARD, RED, radius=True)
    textbox(s, MARGIN + Inches(0.15), Inches(6.42), Inches(11.9), Inches(0.4),
            "Every response: RBAC-filtered • Citation-linked • Audit-logged • No direct database inference",
            11, True, RED_SOFT, PP_ALIGN.CENTER)
    footer(s)


def slide_risk_intro(prs):
    s = add_blank_slide(prs)
    section_header(s, "SECTION 03", "Why Direct AI-to-PMWeb Is Risky",
                   "Ungoverned connectivity exposes enterprise data and decision integrity")
    risks = [
        ("Direct DB Access", "AI agents with SQL/DB credentials create irreversible data exposure and injection risk."),
        ("Hallucinations", "LLMs can fabricate figures, vendors, or clauses — catastrophic in procurement decisions."),
        ("Security Breach", "Uncontrolled prompts may leak PII, commercial terms, and vendor pricing across tenants."),
        ("No Governance", "Shadow AI bypasses DAMAC policies, retention rules, and regional data residency."),
        ("No Traceability", "Without audit logs, leadership cannot explain how an AI-derived answer was produced."),
        ("Inaccurate Answers", "Stale embeddings, wrong document versions, and missing context produce silent errors."),
    ]
    for i, (t, b) in enumerate(risks):
        col, row = i % 3, i // 3
        card(s, MARGIN + col * Inches(4.05), Inches(2.45) + row * Inches(2.05), Inches(3.85), Inches(1.85), t, [b], "✕")
    textbox(s, MARGIN, Inches(6.5), Inches(12.2), Inches(0.45),
            '"AI should explain enterprise truth, not derive uncontrolled truth."',
            16, True, RED, PP_ALIGN.CENTER)
    footer(s)


def slide_risk_diagram(prs):
    s = add_blank_slide(prs)
    section_header(s, "SECTION 03", "Anti-Pattern vs Recommended Pattern", "Architecture decision with enterprise consequences")
    # Anti-pattern
    rect(s, MARGIN, Inches(2.5), Inches(5.5), Inches(3.8), RGBColor(0x2A, 0x10, 0x10), RED_DARK, radius=True)
    textbox(s, MARGIN + Inches(0.2), Inches(2.65), Inches(5), Inches(0.4), "✕ ANTI-PATTERN", 14, True, RED_SOFT)
    arch_box(s, Inches(1.5), Inches(3.2), Inches(3.5), Inches(0.7), "Claude / OpenAI")
    textbox(s, Inches(3.0), Inches(3.95), Inches(0.3), Inches(0.3), "↓", 20, True, RED)
    arch_box(s, Inches(1.5), Inches(4.2), Inches(3.5), Inches(0.7), "Direct DB / SQL Access", "UNGOVERNED")
    textbox(s, Inches(3.0), Inches(4.95), Inches(0.3), Inches(0.3), "↓", 20, True, RED)
    arch_box(s, Inches(1.5), Inches(5.2), Inches(3.5), Inches(0.7), "PMWeb Database", "HIGH RISK")
    bullets(s, MARGIN + Inches(0.2), Inches(5.95), Inches(5), Inches(1.2), [
        "No RBAC • No citations • No audit",
    ], 10, MUTED)
    # Recommended
    rect(s, Inches(7.0), Inches(2.5), Inches(5.8), Inches(3.8), RGBColor(0x10, 0x1A, 0x10), RED, radius=True)
    textbox(s, Inches(7.2), Inches(2.65), Inches(5), Inches(0.4), "✓ RECOMMENDED", 14, True, WHITE)
    layers = ["Management Experience", "AI Orchestration + Governance", "Enterprise Knowledge Layer (RAG)", "API / Integration Layer", "PMWeb"]
    y = Inches(3.15)
    for layer in layers:
        arch_box(s, Inches(7.8), y, Inches(4.2), Inches(0.52), layer)
        y += Inches(0.62)
    footer(s)


def slide_architecture(prs):
    s = add_blank_slide(prs)
    section_header(s, "SECTION 04", "Recommended Enterprise Architecture",
                   "Governed intelligence layer — cloud-native, auditable, API-first")
    layers = [
        ("Management Experience Layer", "Executive dashboards • AI chatbot • Approval workflows • Citations UI"),
        ("Claude / OpenAI", "Document intelligence • Reasoning • Orchestration assist • Model routing"),
        ("AI Orchestration Layer", "Prompt mgmt • Model routing • Guardrails • Human-in-loop • Cost controls"),
        ("Enterprise Knowledge Layer", "Vector DB • RAG • Document ingestion • Embeddings • Version control"),
        ("API / Integration Layer", "PMWeb APIs • Event bus • ETL • Schema validation • Rate limiting"),
        ("PMWeb", "System of record • Contracts • Tenders • Projects • Commercial data"),
    ]
    y = Inches(2.35)
    w = Inches(10.5)
    cx = Inches(1.5)
    for i, (title, sub) in enumerate(layers):
        arch_box(s, cx, y, w, Inches(0.72), title, sub)
        if i < len(layers) - 1:
            textbox(s, cx + w / 2 - Inches(0.15), y + Inches(0.72), Inches(0.4), Inches(0.25), "▼", 14, True, RED, PP_ALIGN.CENTER)
        y += Inches(0.88)
    # Side capabilities
    caps = ["RBAC", "Audit Logs", "Prompt Logging", "Citation Tracking", "Vector DB", "RAG Pipeline"]
    x = Inches(0.55)
    for i, c in enumerate(caps):
        rect(s, x, Inches(2.5) + i * Inches(0.85), Inches(0.85), Inches(0.65), RED if i % 2 == 0 else CARD_LIGHT, radius=True)
        textbox(s, x - Inches(0.05), Inches(2.58) + i * Inches(0.85), Inches(0.95), Inches(0.5), c, 7, True, WHITE, PP_ALIGN.CENTER)
    footer(s)


def slide_rag_architecture(prs):
    s = add_blank_slide(prs)
    section_header(s, "SECTION 04", "RAG & Knowledge Architecture", "Retrieval-augmented generation with enterprise controls")
    # Flow boxes
    boxes = [
        (Inches(0.6), "PMWeb\nDocuments"),
        (Inches(2.5), "Ingestion\nPipeline"),
        (Inches(4.4), "Chunking &\nEmbedding"),
        (Inches(6.3), "Vector\nDatabase"),
        (Inches(8.2), "RAG\nRetrieval"),
        (Inches(10.1), "AI Orchestration\n+ LLM"),
        (Inches(12.0), "Cited\nResponse"),
    ]
    for i, (left, label) in enumerate(boxes):
        arch_box(s, left, Inches(3.2), Inches(1.65), Inches(1.1), label.replace("\n", " "), "")
        if i < len(boxes) - 1:
            textbox(s, left + Inches(1.65), Inches(3.55), Inches(0.5), Inches(0.3), "→", 18, True, RED, PP_ALIGN.CENTER)
    components = [
        ("Document Ingestion", "PDF, Word, PMWeb exports — OCR, dedup, classification"),
        ("Orchestration Engine", "LangChain / custom — routing, fallbacks, eval hooks"),
        ("AI Governance Layer", "Policy engine, PII redaction, output validation, kill switch"),
        ("PMWeb APIs", "Read via governed APIs; write only post human approval"),
    ]
    for i, (t, b) in enumerate(components):
        card(s, MARGIN + (i % 2) * Inches(6.2), Inches(4.8) + (i // 2) * Inches(1.35), Inches(5.9), Inches(1.15), t, [b])
    footer(s)


def slide_model_comparison(prs):
    s = add_blank_slide(prs)
    section_header(s, "SECTION 05", "AI Model Comparison", "Enterprise evaluation across four leading platforms")
    headers = ["Capability", "Claude Enterprise", "OpenAI GPT-5/4.1", "Azure OpenAI", "Gemini Enterprise"]
    rows = [
        ["Document Summarization", "★★★★★", "★★★★☆", "★★★★☆", "★★★★☆"],
        ["Contract Analysis", "★★★★★", "★★★★☆", "★★★★☆", "★★★☆☆"],
        ["Coding / Orchestration", "★★★★☆", "★★★★★", "★★★★☆", "★★★☆☆"],
        ["Ecosystem Maturity", "★★★★☆", "★★★★★", "★★★★★", "★★★★☆"],
        ["API Flexibility", "★★★★★", "★★★★★", "★★★★☆", "★★★★☆"],
        ["Enterprise Readiness", "★★★★★", "★★★★★", "★★★★★", "★★★★☆"],
        ["Context Window", "200K–1M", "128K–1M", "128K", "1M–2M"],
        ["Hallucination Control", "★★★★★", "★★★★☆", "★★★★☆", "★★★☆☆"],
        ["Governance Capability", "★★★★★", "★★★★☆", "★★★★★", "★★★★☆"],
        ["Integration Ease", "★★★★☆", "★★★★★", "★★★★★", "★★★★☆"],
        ["Cost Optimization", "★★★★☆", "★★★★☆", "★★★☆☆", "★★★★☆"],
    ]
    add_table(s, MARGIN, Inches(2.35), Inches(12.2), Inches(4.5), headers, rows, font_size=8)
    footer(s)


def slide_model_recommendation(prs):
    s = add_blank_slide(prs)
    section_header(s, "SECTION 05", "Recommended Option — Hybrid Architecture", "Best-of-breed model routing for DAMAC enterprise AI")
    card(s, MARGIN, Inches(2.5), Inches(3.8), Inches(3.5), "Claude Enterprise", [
        "Primary: document intelligence & summarization",
        "Contract clause extraction & long-context analysis",
        "Lowest hallucination risk for legal/commercial text",
    ], "◆")
    card(s, Inches(4.75), Inches(2.5), Inches(3.8), Inches(3.5), "OpenAI GPT-5 / 4.1", [
        "Primary: orchestration & coding ecosystem",
        "Agent frameworks, function calling, evals",
        "Broad developer tooling & integrations",
    ], "◇")
    card(s, Inches(8.5), Inches(2.5), Inches(4.25), Inches(3.5), "Hybrid — Recommended", [
        "Claude for document & contract intelligence",
        "OpenAI for orchestration layer & code-gen",
        "Azure OpenAI optional for ME data residency",
        "Intelligent router optimizes cost & quality",
    ], "★")
    rect(s, MARGIN, Inches(6.2), Inches(12.2), Inches(0.65), CARD, RED, radius=True)
    textbox(s, MARGIN + Inches(0.2), Inches(6.32), Inches(11.8), Inches(0.45),
            "Long-term: Multi-model orchestration with unified governance — single DAMAC AI platform",
            13, True, WHITE, PP_ALIGN.CENTER)
    footer(s)


def slide_pricing_tokens(prs):
    s = add_blank_slide(prs)
    section_header(s, "SECTION 06", "Enterprise API Pricing Comparison", "Per-million-token pricing — indicative May 2026 enterprise rates")
    headers = ["Provider / Model", "Input ($/1M tokens)", "Output ($/1M tokens)", "Best For"]
    rows = [
        ["Claude Haiku 4.5", "$0.80", "$4.00", "High-volume retrieval, classification"],
        ["Claude Sonnet 4.5", "$3.00", "$15.00", "Balanced summarization & analysis"],
        ["Claude Opus 4.5", "$15.00", "$75.00", "Complex contracts, executive summaries"],
        ["OpenAI GPT-4.1", "$2.00", "$8.00", "General enterprise workloads"],
        ["OpenAI GPT-4.1 Mini", "$0.40", "$1.60", "Chatbot, lightweight queries"],
        ["OpenAI GPT-5 class", "$12.00", "$48.00", "Advanced reasoning, agents"],
        ["Azure OpenAI (GPT-4.1)", "$2.20", "$8.80", "ME residency, Microsoft ecosystem"],
        ["Azure OpenAI (GPT-4.1 mini)", "$0.44", "$1.76", "Cost-optimized Azure deployment"],
    ]
    add_table(s, MARGIN, Inches(2.35), Inches(12.2), Inches(3.8), headers, rows, font_size=9)
    textbox(s, MARGIN, Inches(6.35), Inches(12), Inches(0.4),
            "* Indicative enterprise list pricing. Actual DAMAC rates subject to volume commits & Azure EA.",
            9, False, MUTED)
    footer(s)


def slide_pricing_scenarios(prs):
    s = add_blank_slide(prs)
    section_header(s, "SECTION 06", "Monthly Enterprise Cost Scenarios", "Realistic DAMAC workload estimates")
    headers = ["Use Case Scenario", "Volume", "Model Strategy", "Est. Monthly Cost (USD)"]
    rows = [
        ["Contract Summaries", "1,000 / month", "Claude Sonnet + Haiku routing", "$8,500 – $14,000"],
        ["Tender Summarizations", "200 / month", "Claude Sonnet (long docs)", "$4,200 – $7,500"],
        ["Management Chatbot", "500 users, ~20 queries/day", "GPT-4.1 Mini + RAG", "$6,000 – $12,000"],
        ["Combined Enterprise (Phase 3)", "All workloads", "Hybrid routing + caching", "$18,000 – $32,000"],
        ["Full Platform (Phase 4)", "All + governance infra", "Hybrid + Azure option", "$35,000 – $55,000"],
    ]
    add_table(s, MARGIN, Inches(2.35), Inches(12.2), Inches(2.8), headers, rows, font_size=9)
    textbox(s, MARGIN, Inches(5.3), Inches(12), Inches(0.4), "Cost Optimization Strategies", 14, True, RED)
    bullets(s, MARGIN, Inches(5.75), Inches(12), Inches(1.2), [
        "Prompt caching — up to 90% savings on repeated contract templates",
        "RAG architecture — smaller models for retrieval, premium models for synthesis only",
        "Hybrid AI routing — Haiku/Mini for triage, Sonnet/GPT-4.1 for generation",
        "Batch processing — off-peak tender summarization at 50% discount",
    ], 11, SILVER)
    footer(s)


def slide_pricing_detail(prs):
    s = add_blank_slide(prs)
    section_header(s, "SECTION 06", "Procurement & Chatbot Cost Breakdown", "Per-use-case economics for business case validation")
    headers = ["Cost Component", "Assumptions", "Claude Path", "OpenAI Path", "Hybrid (Rec.)"]
    rows = [
        ["Contract summary (avg)", "~80K in / 4K out tokens", "$0.30", "$0.22", "$0.25"],
        ["Tender BAFO pack (avg)", "~200K in / 8K out tokens", "$0.85", "$0.65", "$0.72"],
        ["Chatbot query (avg)", "~2K in / 500 out tokens", "—", "$0.004", "$0.003"],
        ["Monthly — 1000 contracts", "Sonnet-class", "$12,000", "$9,500", "$10,200"],
        ["Monthly — 200 tenders", "Sonnet + long ctx", "$6,800", "$5,400", "$5,900"],
        ["Monthly — 500 chatbot users", "Mini + RAG", "—", "$9,200", "$7,800"],
    ]
    add_table(s, MARGIN, Inches(2.35), Inches(12.2), Inches(3.5), headers, rows, font_size=8)
    rect(s, MARGIN, Inches(6.0), Inches(12.2), Inches(0.85), CARD, RED, radius=True)
    textbox(s, MARGIN + Inches(0.25), Inches(6.1), Inches(11.7), Inches(0.65),
            "Hybrid routing typically delivers 15–25% cost reduction vs single-vendor — with higher quality on documents",
            12, True, WHITE, PP_ALIGN.CENTER)
    footer(s)


def slide_roadmap(prs):
    s = add_blank_slide(prs)
    section_header(s, "SECTION 07", "Phased Implementation Strategy", "Disciplined delivery with measurable value at each gate")
    phases = [
        ("PHASE 1", "Contract Summarization POC", "2–3 weeks",
         ["PMWeb API integration", "Document ingestion + RAG MVP", "Claude contract extraction", "Human-in-loop approval UI"]),
        ("PHASE 2", "Tender Recommendation Engine", "4–6 weeks",
         ["BAFO comparison automation", "Deviation & exclusion detection", "Historical benchmarking", "PMWeb workflow integration"]),
        ("PHASE 3", "Executive AI Chatbot", "2–3 months",
         ["Management query interface", "RBAC + citation layer", "500-user pilot", "PMWeb real-time data sync"]),
        ("PHASE 4", "Enterprise AI Governance Platform", "4–6 months",
         ["Multi-model orchestration", "Full audit & compliance", "Predictive procurement analytics", "DAMAC-wide AI standards"]),
    ]
    x = MARGIN
    for i, (phase, title, timeline, items) in enumerate(phases):
        w = Inches(2.95)
        rect(s, x + i * Inches(3.05), Inches(2.4), w, Inches(4.3), CARD, RED if i == 0 else CARD_LIGHT, radius=True)
        textbox(s, x + i * Inches(3.05) + Inches(0.15), Inches(2.55), w - Inches(0.3), Inches(0.3), phase, 10, True, RED)
        textbox(s, x + i * Inches(3.05) + Inches(0.15), Inches(2.85), w - Inches(0.3), Inches(0.55), title, 11, True, WHITE)
        rect(s, x + i * Inches(3.05) + Inches(0.15), Inches(3.45), w - Inches(0.3), Inches(0.35), RED_DARK, radius=True)
        textbox(s, x + i * Inches(3.05) + Inches(0.15), Inches(3.48), w - Inches(0.3), Inches(0.3), timeline, 10, True, WHITE, PP_ALIGN.CENTER)
        bullets(s, x + i * Inches(3.05) + Inches(0.15), Inches(3.9), w - Inches(0.3), Inches(2.5), items, 9, SILVER)
    footer(s)


def slide_roadmap_timeline(prs):
    s = add_blank_slide(prs)
    section_header(s, "SECTION 07", "Implementation Timeline", "Quarter-by-quarter delivery view")
    milestones = [
        ("Week 1–3", "Phase 1", "Contract POC", Inches(0.8)),
        ("Week 4–9", "Phase 2", "Tender Engine", Inches(3.5)),
        ("Month 3–5", "Phase 3", "Executive Chatbot", Inches(6.2)),
        ("Month 6–11", "Phase 4", "AI Governance Platform", Inches(8.9)),
    ]
    rect(s, MARGIN, Inches(3.5), Inches(12.2), Inches(0.08), RED)
    for time, phase, desc, left in milestones:
        rect(s, left, Inches(3.15), Inches(0.15), Inches(0.5), RED)
        rect(s, left - Inches(0.1), Inches(3.7), Inches(2.8), Inches(1.8), CARD, RED, radius=True)
        textbox(s, left - Inches(0.05), Inches(3.82), Inches(2.6), Inches(0.3), time, 10, True, RED)
        textbox(s, left - Inches(0.05), Inches(4.15), Inches(2.6), Inches(0.35), phase, 12, True, WHITE)
        textbox(s, left - Inches(0.05), Inches(4.55), Inches(2.6), Inches(0.8), desc, 10, False, SILVER)
    textbox(s, MARGIN, Inches(5.8), Inches(12), Inches(0.5),
            "Total program: ~9–11 months to full DAMAC AI Governance Platform | Quick win in 2–3 weeks",
            13, True, GOLD, PP_ALIGN.CENTER)
    footer(s)


def slide_security(prs):
    s = add_blank_slide(prs)
    section_header(s, "SECTION 08", "Security & Governance Framework", "Enterprise controls aligned to DAMAC policies")
    controls = [
        ("RBAC", "Role-based access aligned to PMWeb permissions — procurement, commercial, executive tiers."),
        ("Audit Logging", "Immutable logs: who asked what, which documents retrieved, which model, which output."),
        ("Prompt Logging", "Full prompt/response capture for compliance review and incident investigation."),
        ("AI Governance", "Policy engine: approved models, data classification rules, output validation gates."),
        ("Human-in-the-Loop", "Mandatory analyst approval before any PMWeb write or commitment action."),
        ("Data Privacy", "PII redaction, encryption at rest/transit, UAE data residency via Azure option."),
        ("DAMAC Enterprise Controls", "SSO integration, retention policies, vendor DPAs, SOC2-aligned providers."),
        ("Secure API Architecture", "API gateway, mTLS, secrets vault, zero direct DB credentials to AI."),
    ]
    for i, (t, b) in enumerate(controls):
        col, row = i % 4, i // 4
        card(s, MARGIN + col * Inches(3.05), Inches(2.4) + row * Inches(2.15), Inches(2.85), Inches(1.95), t, [b], "🔒")
    footer(s)


def slide_governance_diagram(prs):
    s = add_blank_slide(prs)
    section_header(s, "SECTION 08", "AI Governance Control Plane", "Centralized policy enforcement across all AI workloads")
    center_x, center_y = Inches(5.0), Inches(4.0)
    rect(s, center_x, center_y, Inches(3.3), Inches(1.4), RED, radius=True)
    textbox(s, center_x + Inches(0.15), center_y + Inches(0.35), Inches(3), Inches(0.7),
            "AI Governance\nControl Plane", 14, True, WHITE, PP_ALIGN.CENTER)
    orbit = [
        (Inches(1.0), Inches(2.8), "RBAC & SSO"),
        (Inches(9.5), Inches(2.8), "Audit & Compliance"),
        (Inches(1.0), Inches(5.2), "Prompt Management"),
        (Inches(9.5), Inches(5.2), "Model Allowlist"),
        (Inches(3.5), Inches(6.0), "Human Approval"),
        (Inches(7.0), Inches(6.0), "Data Classification"),
    ]
    for left, top, label in orbit:
        arch_box(s, left, top, Inches(2.5), Inches(0.75), label)
    footer(s)


def slide_future_vision(prs):
    s = add_blank_slide(prs)
    section_header(s, "SECTION 09", "Future Vision — DAMAC AI Governance Platform",
                   "From PMWeb intelligence to enterprise-wide procurement AI")
    capabilities = [
        ("Predictive Procurement Intelligence", "Forecast pricing trends, bid competitiveness, and award outcomes."),
        ("AI Risk Scoring", "Automated vendor and subcontractor risk assessment across portfolio."),
        ("Vendor Performance Intelligence", "Historical performance, SLA compliance, and anomaly patterns."),
        ("Procurement Anomaly Detection", "Flag unusual pricing, scope gaps, and compliance deviations."),
        ("Enterprise Project Intelligence", "Cross-project insights: cost, schedule, design, commercial."),
        ("Executive Copilots", "Personalized AI advisors for CEO, CFO, and procurement leadership."),
    ]
    for i, (t, b) in enumerate(capabilities):
        col, row = i % 3, i // 3
        card(s, MARGIN + col * Inches(4.05), Inches(2.45) + row * Inches(2.05), Inches(3.85), Inches(1.85), t, [b], "◎")
    rect(s, MARGIN, Inches(6.35), Inches(12.2), Inches(0.55), CARD, RED, radius=True)
    textbox(s, MARGIN + Inches(0.2), Inches(6.42), Inches(11.8), Inches(0.4),
            "Vision: DAMAC AI Governance Platform — the trusted intelligence layer for all enterprise decisions",
            12, True, WHITE, PP_ALIGN.CENTER)
    footer(s)


def slide_final_recommendation(prs):
    s = add_blank_slide(prs)
    section_header(s, "SECTION 10", "Final Recommendation", "Consulting conclusion — path to governed enterprise AI")
    recommendations = [
        "Build the Enterprise AI Orchestration Layer first — before any production AI workloads.",
        "Avoid direct AI-to-database architecture — enforce API-first, governed connectivity to PMWeb.",
        "Deploy AI as a governed intelligence layer that explains enterprise truth with citations.",
        "Start with Contract Intelligence POC (Phase 1) — 2–3 weeks to demonstrable value.",
        "Adopt hybrid Claude + OpenAI architecture for document quality and orchestration depth.",
        "Scale systematically to DAMAC AI Governance Platform over 9–11 months.",
    ]
    bullets(s, MARGIN, Inches(2.5), Inches(7.5), Inches(4.0), recommendations, 14, WHITE)
    rect(s, Inches(8.5), Inches(2.5), Inches(4.25), Inches(3.8), CARD, RED, radius=True)
    textbox(s, Inches(8.7), Inches(2.7), Inches(3.85), Inches(0.45), "Decision Ask", 16, True, RED)
    bullets(s, Inches(8.7), Inches(3.3), Inches(3.85), Inches(2.8), [
        "Approve Phase 1 POC budget & team",
        "Nominate DAMAC executive sponsor",
        "Confirm PMWeb API access scope",
        "Establish AI governance steering committee",
    ], 12, SILVER)
    textbox(s, MARGIN, Inches(6.5), Inches(12.2), Inches(0.5),
            "The opportunity is not connecting AI to PMWeb — it is building the intelligence layer that governs how AI serves DAMAC.",
            14, True, RED, PP_ALIGN.CENTER)
    footer(s)


def slide_section_divider(prs, num: str, title: str, subtitle: str = ""):
    s = add_blank_slide(prs)
    fill_bg(s)
    accent_bar(s, Inches(0), Inches(0.1))
    rect(s, Inches(0), Inches(0), Inches(0.35), SLIDE_H, RED)
    red_swoosh(s, Inches(8.5), Inches(1.0), Inches(5), Inches(5.5))
    textbox(s, MARGIN, Inches(2.8), Inches(2), Inches(0.6), num, 48, True, RED)
    textbox(s, MARGIN, Inches(3.5), Inches(10), Inches(1.2), title, 32, True, WHITE)
    if subtitle:
        textbox(s, MARGIN, Inches(4.7), Inches(9), Inches(0.6), subtitle, 16, False, MUTED)
    footer(s)


def slide_thank_you(prs):
    s = add_blank_slide(prs)
    fill_bg(s)
    accent_bar(s)
    red_swoosh(s, Inches(4), Inches(2), Inches(5.5), Inches(4))
    textbox(s, MARGIN, Inches(2.8), Inches(12), Inches(1.0), "Thank You", 44, True, WHITE, PP_ALIGN.CENTER)
    textbox(s, MARGIN, Inches(4.0), Inches(12), Inches(0.6),
            "Enterprise AI Governance & Intelligence Layer for PMWeb", 18, False, RED_SOFT, PP_ALIGN.CENTER)
    textbox(s, MARGIN, Inches(5.0), Inches(12), Inches(0.5),
            "CMCS | DAMAC AI Transformation | Confidential", 12, False, MUTED, PP_ALIGN.CENTER)
    footer(s)


def build_presentation(output_path: Path) -> Path:
    prs = prs_blank()
    slide_title(prs)
    slide_agenda(prs)
    slide_section_divider(prs, "01", "Executive Summary",
                          "Current challenges, opportunity, and transformation narrative")
    slide_exec_summary(prs)
    slide_challenges(prs)
    slide_current_vs_future(prs)
    slide_section_divider(prs, "02", "DAMAC PMWeb Use Cases",
                          "Commitment approval, contract intelligence, management chatbot")
    slide_use_cases_intro(prs)
    slide_commitment_use_case(prs)
    slide_contract_use_case(prs)
    slide_chatbot_use_case(prs)
    slide_section_divider(prs, "03", "Why Direct AI-to-PMWeb Is Risky",
                          "Enterprise truth must be governed — not inferred from raw databases")
    slide_risk_intro(prs)
    slide_risk_diagram(prs)
    slide_section_divider(prs, "04", "Recommended Enterprise Architecture",
                          "API-first orchestration with knowledge layer and AI governance")
    slide_architecture(prs)
    slide_rag_architecture(prs)
    slide_section_divider(prs, "05", "AI Model Comparison",
                          "Claude, OpenAI, Azure OpenAI, Gemini — hybrid recommendation")
    slide_model_comparison(prs)
    slide_model_recommendation(prs)
    slide_section_divider(prs, "06", "Enterprise Pricing & Cost Optimization",
                          "Token economics, scenarios, and hybrid routing savings")
    slide_pricing_tokens(prs)
    slide_pricing_scenarios(prs)
    slide_pricing_detail(prs)
    slide_section_divider(prs, "07", "Implementation Strategy",
                          "Phased roadmap from POC to DAMAC AI Governance Platform")
    slide_roadmap(prs)
    slide_roadmap_timeline(prs)
    slide_section_divider(prs, "08", "Security & Governance",
                          "RBAC, audit, human-in-the-loop, and DAMAC enterprise controls")
    slide_security(prs)
    slide_governance_diagram(prs)
    slide_section_divider(prs, "09", "Future Vision",
                          "DAMAC AI Governance Platform — enterprise procurement intelligence")
    slide_future_vision(prs)
    slide_section_divider(prs, "10", "Final Recommendation",
                          "Build orchestration first — scale governed intelligence across DAMAC")
    slide_final_recommendation(prs)
    slide_thank_you(prs)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(output_path))
    return output_path


if __name__ == "__main__":
    out = Path(__file__).resolve().parents[1] / "output" / "DAMAC_PMWeb_AI_Governance_Intelligence_Layer.pptx"
    path = build_presentation(out)
    print(f"Generated: {path} ({path.stat().st_size // 1024} KB)")
