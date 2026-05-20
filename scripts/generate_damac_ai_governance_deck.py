#!/usr/bin/env python3
"""
DAMAC PMWeb — Enterprise AI Governance & Intelligence Layer
Premium consulting deck: white base, black & red accents, CMCS wordmark.
"""

from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

# ── Palette: white slides, black text, red accents only ───────────────────
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
OFF_WHITE = RGBColor(0xFA, 0xFA, 0xFA)
BLACK = RGBColor(0x1A, 0x1A, 0x1A)
TEXT = RGBColor(0x2D, 0x2D, 0x2D)
MUTED = RGBColor(0x6B, 0x6B, 0x6B)
LIGHT_GRAY = RGBColor(0xF0, 0xF0, 0xF0)
BORDER = RGBColor(0xDD, 0xDD, 0xDD)
RED = RGBColor(0xE3, 0x18, 0x37)
RED_DARK = RGBColor(0xB0, 0x12, 0x28)
RED_TINT = RGBColor(0xFD, 0xF2, 0xF4)

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
MARGIN = Inches(0.6)
CONTENT_LEFT = MARGIN
CONTENT_WIDTH = Inches(12.1)
HEADER_RULE_Y = Inches(1.58)
CONTENT_TOP = Inches(1.72)
CONTENT_BOTTOM = Inches(6.52)
FOOTER_TEXT_Y = Inches(6.92)
FOOTER_LINE_Y = Inches(7.14)
FONT = "Calibri"

# Uniform typography (pt) — consistent across deck
FS_CAPTION = 10      # section label, footer
FS_BODY = 11         # body, bullets, tables, cards, callouts
FS_TITLE = 22        # slide titles
FS_DISPLAY = 28      # title slide headline only

ASSETS = Path(__file__).resolve().parents[1] / "assets"
ICONS = ASSETS / "icons"
DIAGRAMS = ASSETS / "diagrams"
CMCS_LOGO = ASSETS / "cmcs_logo.png"
CMCS_LOGO_H = Inches(0.34)
CMCS_LOGO_X = Inches(11.55)

RECOMMENDED_AI = "Claude Enterprise"


def prs_blank() -> Presentation:
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    return prs


def add_blank_slide(prs: Presentation):
    return prs.slides.add_slide(prs.slide_layouts[6])


def fill_bg(slide, color: RGBColor = WHITE):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color


def rect(slide, left, top, width, height, fill: RGBColor, line: RGBColor | None = None, radius=False):
    st = MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE if radius else MSO_AUTO_SHAPE_TYPE.RECTANGLE
    s = slide.shapes.add_shape(st, left, top, width, height)
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    if line:
        s.line.color.rgb = line
        s.line.width = Pt(0.75)
    else:
        s.line.fill.background()
    return s


def textbox(slide, left, top, width, height, text: str, size=FS_BODY, bold=False,
            color=TEXT, align=PP_ALIGN.LEFT, font=FONT, line_spacing=1.15):
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
    p.line_spacing = line_spacing
    return tb


def bullets(slide, left, top, width, height, items: list[str], size=FS_BODY, color=TEXT, spacing=7):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"• {item.lstrip('• ').strip()}"
        p.level = 0
        p.font.size = Pt(size)
        p.font.name = FONT
        p.font.color.rgb = color
        p.space_after = Pt(spacing)
        p.line_spacing = 1.2
    return tb


def add_image(slide, path: Path, left, top, height=None, width=None):
    if path.exists():
        if height:
            return slide.shapes.add_picture(str(path), left, top, height=height)
        if width:
            return slide.shapes.add_picture(str(path), left, top, width=width)
        return slide.shapes.add_picture(str(path), left, top)
    return None


def add_diagram(slide, filename: str, left, top, width=None, height=None):
    """Embed pre-rendered diagram PNG with explicit width and/or height."""
    path = DIAGRAMS / filename
    if not path.exists():
        return None
    if height:
        return add_image(slide, path, left, top, height=height)
    if width:
        return add_image(slide, path, left, top, width=width)
    return add_image(slide, path, left, top)


def draw_cmcs_logo(slide):
    add_image(slide, CMCS_LOGO, CMCS_LOGO_X, Inches(0.14), height=CMCS_LOGO_H)


def draw_footer(slide):
    """Minimal footer on white — thin rule only, no grey bar."""
    rect(slide, MARGIN, FOOTER_LINE_Y, SLIDE_W - MARGIN * 2, Inches(0.018), RED)
    textbox(slide, MARGIN, FOOTER_TEXT_Y, Inches(8.2), Inches(0.22),
            "Enterprise AI Governance & Intelligence Layer for PMWeb  |  CMCS", FS_CAPTION, False, MUTED)
    textbox(slide, Inches(10.9), FOOTER_TEXT_Y, Inches(2.0), Inches(0.22),
            "CONFIDENTIAL", FS_CAPTION, True, RED, PP_ALIGN.RIGHT)


def slide_chrome(slide, section: str = "", title: str = "", subtitle: str = ""):
    """White header/footer, CMCS wordmark only, fixed typography."""
    fill_bg(slide, WHITE)
    rect(slide, Inches(0), Inches(0), SLIDE_W, Inches(0.04), RED)
    draw_cmcs_logo(slide)

    if section:
        textbox(slide, CONTENT_LEFT, Inches(0.52), Inches(3), Inches(0.22),
                section.upper(), FS_CAPTION, True, RED)
    if title:
        textbox(slide, CONTENT_LEFT, Inches(0.78), CONTENT_WIDTH, Inches(0.48),
                title, FS_TITLE, True, BLACK)
    if subtitle:
        textbox(slide, CONTENT_LEFT, Inches(1.28), CONTENT_WIDTH, Inches(0.26),
                subtitle, FS_BODY, False, MUTED)

    rect(slide, MARGIN, HEADER_RULE_Y, SLIDE_W - MARGIN * 2, Inches(0.012), BORDER)
    draw_footer(slide)


def card(slide, left, top, w, h, title: str, body: list[str], accent=True, icon: str | None = None):
    rect(slide, left, top, w, h, WHITE, BORDER, radius=True)
    if accent:
        rect(slide, left, top, Inches(0.07), h, RED)
    tx = left + Inches(0.2)
    ty = top + Inches(0.14)
    if icon:
        ip = ICONS / icon
        if ip.exists():
            add_image(slide, ip, left + Inches(0.14), top + Inches(0.12), height=Inches(0.42))
            tx = left + Inches(0.68)
    textbox(slide, tx, ty, w - (tx - left) - Inches(0.15), Inches(0.36), title, FS_BODY, True, BLACK)
    bullets(slide, left + Inches(0.2), top + Inches(0.52), w - Inches(0.35), h - Inches(0.58),
            body, FS_BODY, MUTED, spacing=6)


def insight_panel(slide, left, top, w, h, heading: str, quote: str, icon: str = "quote.png"):
    rect(slide, left, top, w, h, RED_TINT, RED, radius=True)
    if (ICONS / icon).exists():
        add_image(slide, ICONS / icon, left + Inches(0.2), top + Inches(0.18), height=Inches(0.5))
    textbox(slide, left + Inches(0.85), top + Inches(0.2), w - Inches(1.0), Inches(0.35),
            heading, FS_BODY, True, RED)
    textbox(slide, left + Inches(0.25), top + Inches(0.75), w - Inches(0.5), h - Inches(0.9),
            quote, FS_BODY, True, BLACK, PP_ALIGN.CENTER, line_spacing=1.35)


def add_table(slide, left, top, width, height, headers, rows, font_size=FS_BODY):
    tbl = slide.shapes.add_table(len(rows) + 1, len(headers), left, top, width, height).table
    cw = int(width / len(headers))
    for c in range(len(headers)):
        tbl.columns[c].width = cw
    for c, h in enumerate(headers):
        cell = tbl.cell(0, c)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = BLACK
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(font_size)
            p.font.bold = True
            p.font.color.rgb = WHITE
            p.font.name = "Calibri"
            p.alignment = PP_ALIGN.CENTER
    for r, row in enumerate(rows):
        fill = WHITE if r % 2 == 0 else OFF_WHITE
        for c, val in enumerate(row):
            cell = tbl.cell(r + 1, c)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = fill
            bold = c == 0 and "Claude" in str(val)
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(font_size)
                p.font.color.rgb = RED if bold and r == 0 else TEXT
                p.font.bold = bold
                p.font.name = "Calibri"
    return tbl


def arch_box(slide, left, top, w, h, label: str, sub: str = "", highlight=False):
    fill = RED_TINT if highlight else WHITE
    line = RED if highlight else BORDER
    lw = Pt(2) if highlight else Pt(0.75)
    st = MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE
    s = slide.shapes.add_shape(st, left, top, w, h)
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    s.line.color.rgb = line
    s.line.width = lw
    pad = Inches(0.14)
    textbox(slide, left + pad, top + Inches(0.09), w - pad * 2, Inches(0.26),
            label, FS_BODY, True, BLACK if not highlight else RED_DARK, PP_ALIGN.CENTER)
    if sub:
        textbox(slide, left + pad, top + Inches(0.36), w - pad * 2, h - Inches(0.42),
                sub, FS_BODY, False, MUTED, PP_ALIGN.CENTER)


def _centered_left(total_w, area_w=CONTENT_WIDTH, area_l=CONTENT_LEFT):
    return area_l + (area_w - total_w) / 2


def _down_arrow(slide, center_x, top):
    aw, ah = Inches(0.16), Inches(0.1)
    left = center_x - aw / 2
    sh = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ISOSCELES_TRIANGLE, left, top, aw, ah)
    sh.fill.solid()
    sh.fill.fore_color.rgb = RED
    sh.line.fill.background()
    sh.rotation = 180.0


def _flow_arrow(slide, left, top, width=Inches(0.22)):
    sh = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.RIGHT_ARROW, left, top + Inches(0.28), width, Inches(0.14)
    )
    sh.fill.solid()
    sh.fill.fore_color.rgb = RED
    sh.line.fill.background()


def draw_architecture_stack(slide):
    """Centered native layer stack with symmetric styling."""
    stack_w = Inches(9.6)
    stack_l = _centered_left(stack_w, SLIDE_W, Inches(0))
    cx = stack_l + stack_w / 2
    box_h = Inches(0.54)
    gap = Inches(0.1)
    layers = [
        ("Management Experience Layer", "Dashboards · Chatbot · Approvals · Citations", False),
        (RECOMMENDED_AI, "Document intelligence · Reasoning · Summarization", True),
        ("AI Orchestration Layer", "Guardrails · Human-in-loop · Audit · Cost control", False),
        ("Enterprise Knowledge Layer", "Vector DB · RAG · Ingestion · Versioning", False),
        ("API / Integration Layer", "PMWeb APIs · ETL · Schema validation", False),
        ("PMWeb", "System of record — contracts, tenders, projects", False),
    ]
    y = CONTENT_TOP + Inches(0.04)
    for i, (title, sub, highlight) in enumerate(layers):
        arch_box(slide, stack_l, y, stack_w, box_h, title, sub, highlight)
        y += box_h
        if i < len(layers) - 1:
            _down_arrow(slide, cx, y + Inches(0.01))
            y += gap
    cap_h = Inches(0.4)
    y += Inches(0.06)
    rect(slide, stack_l, y, stack_w, cap_h, RED_TINT, RED, radius=True)
    textbox(slide, stack_l + Inches(0.12), y + Inches(0.1), stack_w - Inches(0.24), Inches(0.28),
            "RBAC · Audit Logs · Prompt Logging · Citations · Vector DB · RAG",
            FS_BODY, True, RED_DARK, PP_ALIGN.CENTER)


def flow_node(slide, left, top, w, h, label: str, highlight=False):
    fill = RED_TINT if highlight else WHITE
    line = RED if highlight else BORDER
    rect(slide, left, top, w, h, fill, line, radius=True)
    textbox(slide, left + Inches(0.04), top + Inches(0.22), w - Inches(0.08), Inches(0.35),
            label, FS_BODY, True, RED_DARK if highlight else BLACK, PP_ALIGN.CENTER)


def draw_rag_pipeline(slide):
    """Centered horizontal RAG flow — native shapes."""
    steps = ["PMWeb Docs", "Ingestion", "Embedding", "Vector DB", "RAG", "Claude", "Response"]
    n = len(steps)
    box_w = Inches(1.32)
    arrow_w = Inches(0.2)
    box_h = Inches(0.72)
    row_w = n * box_w + (n - 1) * arrow_w
    row_l = _centered_left(row_w)
    y = CONTENT_TOP + Inches(0.05)
    x = row_l
    for i, lbl in enumerate(steps):
        flow_node(slide, x, y, box_w, box_h, lbl, highlight=(lbl == "Claude"))
        x += box_w
        if i < n - 1:
            _flow_arrow(slide, x, y)
            x += arrow_w


def callout(slide, left, top, width, text: str, size=FS_BODY):
    rect(slide, left, top, width, Inches(0.48), RED_TINT, RED, radius=True)
    textbox(slide, left + Inches(0.15), top + Inches(0.1), width - Inches(0.3), Inches(0.32),
            text, size, True, RED_DARK, PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDES
# ═══════════════════════════════════════════════════════════════════════════

def slide_title(prs):
    s = add_blank_slide(prs)
    fill_bg(s, WHITE)
    rect(s, Inches(0), Inches(0), SLIDE_W, Inches(0.04), RED)
    draw_cmcs_logo(s)
    rect(s, MARGIN, Inches(1.65), Inches(0.09), Inches(2.5), RED)
    textbox(s, Inches(0.82), Inches(1.45), Inches(10.5), Inches(1.2),
            "Enterprise AI Governance &\nIntelligence Layer for PMWeb", FS_DISPLAY, True, BLACK)
    textbox(s, Inches(0.82), Inches(2.95), Inches(10.2), Inches(0.38),
            "Governed AI Orchestration — Not Direct AI-to-Database Connectivity", FS_BODY, False, RED)
    textbox(s, Inches(0.82), Inches(3.45), Inches(10), Inches(0.32),
            "Executive Proposal for DAMAC Leadership & Technology Stakeholders", FS_BODY, False, MUTED)
    if (ICONS / "ai.png").exists():
        add_image(s, ICONS / "ai.png", Inches(9.8), Inches(4.2), height=Inches(1.0))
    textbox(s, Inches(0.82), Inches(5.7), Inches(6), Inches(0.28),
            "Prepared for DAMAC  |  May 2026", FS_BODY, False, MUTED)
    draw_footer(s)


def slide_agenda(prs):
    s = add_blank_slide(prs)
    slide_chrome(s, "Overview", "Agenda", "Boardroom executive briefing structure")
    add_diagram(s, "agenda.png", CONTENT_LEFT, CONTENT_TOP,
                width=CONTENT_WIDTH, height=Inches(4.55))


def slide_section_divider(prs, num: str, title: str, subtitle: str = ""):
    s = add_blank_slide(prs)
    fill_bg(s, WHITE)
    rect(s, Inches(0), Inches(0), Inches(0.22), SLIDE_H, RED)
    rect(s, Inches(0), Inches(0), SLIDE_W, Inches(0.04), RED)
    draw_cmcs_logo(s)
    draw_footer(s)
    textbox(s, Inches(0.55), Inches(2.55), Inches(1.2), Inches(0.55), num, FS_DISPLAY, True, RED)
    textbox(s, Inches(0.55), Inches(3.2), Inches(11), Inches(0.75), title, FS_TITLE, True, BLACK)
    if subtitle:
        textbox(s, Inches(0.55), Inches(4.05), Inches(10), Inches(0.45), subtitle, FS_BODY, False, MUTED)


def slide_exec_summary(prs):
    s = add_blank_slide(prs)
    slide_chrome(s, "Section 01", "Executive Summary",
                 "Governed enterprise AI over PMWeb — not uncontrolled connectivity")
    col_w = Inches(7.35)
    panel_l = Inches(8.25)
    panel_w = Inches(4.45)
    panel_h = Inches(4.35)
    bullets(s, CONTENT_LEFT, CONTENT_TOP + Inches(0.05), col_w, panel_h, [
        "Procurement and commercial workflows on PMWeb generate high-value data trapped in documents and contracts.",
        "Manual summarization and tender analysis create bottlenecks and visibility gaps for leadership.",
        "AI accelerates decisions only when deployed as a governed intelligence layer over enterprise truth.",
        f"Recommended AI platform: {RECOMMENDED_AI} behind an Enterprise Orchestration Layer.",
        "Deliver full scoped program in 2–3 months: POC → tender engine → chatbot → governance platform.",
    ], FS_BODY, TEXT, spacing=8)
    insight_panel(s, panel_l, CONTENT_TOP, panel_w, panel_h,
                  "Strategic Thesis",
                  '"AI should explain enterprise truth,\nnot derive uncontrolled truth."')


def slide_challenges(prs):
    s = add_blank_slide(prs)
    slide_chrome(s, "Section 01", "Current Challenges",
                 "Operational friction across procurement & commercial management")
    data = [
        ("Manual Effort", "Heavy manual work in bid packs, BAFO comparisons, and CO approvals."),
        ("No Executive Summaries", "Leadership lacks trusted summaries of tenders and contracts."),
        ("Slow Tender Cycles", "Decisions delayed by document review and deviation analysis."),
        ("Limited Visibility", "No on-demand access to project status, unit mix, or vendor insights."),
        ("Governance Gap", "Risk of shadow AI and ungoverned database access."),
    ]
    w, h = Inches(3.75), Inches(1.75)
    for i, (t, b) in enumerate(data):
        col, row = i % 3, i // 3
        card(s, CONTENT_LEFT + col * Inches(4.0), CONTENT_TOP + row * Inches(1.95), w, h, t, [b])


def slide_current_vs_future(prs):
    s = add_blank_slide(prs)
    slide_chrome(s, "Section 01", "Current State vs Future State",
                 "Transformation narrative for boardroom stakeholders")
    cw = Inches(5.75)
    rect(s, CONTENT_LEFT, CONTENT_TOP, cw, Inches(4.5), LIGHT_GRAY, BORDER, radius=True)
    textbox(s, CONTENT_LEFT + Inches(0.25), CONTENT_TOP + Inches(0.15), Inches(4), Inches(0.35),
            "CURRENT STATE", FS_BODY, True, MUTED)
    bullets(s, CONTENT_LEFT + Inches(0.25), CONTENT_TOP + Inches(0.55), cw - Inches(0.5), Inches(3.8), [
        "Manual contract & tender summarization",
        "Fragmented document repositories",
        "Reactive management reporting",
        "Siloed PMWeb data access",
        "No AI audit trail or governance",
    ], FS_BODY)
    textbox(s, Inches(6.55), CONTENT_TOP + Inches(1.8), Inches(0.6), Inches(0.5), "→", FS_TITLE, True, RED, PP_ALIGN.CENTER)
    rect(s, Inches(7.0), CONTENT_TOP, cw, Inches(4.5), RED_TINT, RED, radius=True)
    textbox(s, Inches(7.25), CONTENT_TOP + Inches(0.15), Inches(4), Inches(0.35),
            "FUTURE STATE", FS_BODY, True, RED)
    bullets(s, Inches(7.25), CONTENT_TOP + Inches(0.55), cw - Inches(0.5), Inches(3.8), [
        "AI-assisted governance & summarization",
        "Enterprise Knowledge Layer + RAG",
        "Executive AI chatbot with citations",
        "Governed API orchestration to PMWeb",
        "DAMAC AI Governance Platform",
    ], FS_BODY, TEXT)
    callout(s, CONTENT_LEFT, CONTENT_BOTTOM - Inches(0.52), CONTENT_WIDTH,
            "Opportunity: AI-assisted governance — not ungoverned AI connectivity")


def slide_use_cases_intro(prs):
    s = add_blank_slide(prs)
    slide_chrome(s, "Section 02", "DAMAC PMWeb Use Cases",
                 "Procurement, commercial & management scenarios")
    card(s, CONTENT_LEFT, CONTENT_TOP, Inches(3.75), Inches(4.35), "Commitment / CO Approval", [
        "Bid summarization & BAFO comparison",
        "Technical recommendations & benchmarking",
        "Deviations, exclusions & T&C summaries",
    ], icon="document.png")
    card(s, Inches(4.75), CONTENT_TOP, Inches(3.75), Inches(4.35), "Contract Intelligence", [
        "AI clause extraction & summarization",
        "Auto-population of PMWeb fields",
        "Contract intelligence repository",
    ], icon="contract.png")
    card(s, Inches(8.85), CONTENT_TOP, Inches(3.75), Inches(4.35), "Management AI Chatbot", [
        "Project & package status queries",
        "Building config, unit mix, awards",
        "Vendor & subcontractor insights",
    ], icon="chat.png")


def slide_commitment_use_case(prs):
    s = add_blank_slide(prs)
    slide_chrome(s, "Section 02", "Use Case 1 — Commitment / CO Approval",
                 "Accelerate procurement decisions with governed AI")
    items = [
        ("Bid Summarization", "Executive summaries from tender submissions"),
        ("BAFO Comparison", "Commercial & technical comparison matrices"),
        ("Technical Recommendations", "Evaluation summaries with citations"),
        ("Historical Benchmarking", "Compare against prior awards"),
        ("Deviations / Exclusions", "Highlight material deviations"),
        ("Contract T&Cs Summary", "Condensed terms for approval committees"),
    ]
    w, h = Inches(3.85), Inches(1.55)
    for i, (t, b) in enumerate(items):
        col, row = i % 3, i // 3
        card(s, CONTENT_LEFT + col * Inches(4.02), CONTENT_TOP + row * Inches(1.72), w, h, t, [b])
    callout(s, CONTENT_LEFT, CONTENT_BOTTOM - Inches(0.48), CONTENT_WIDTH,
            "PMWeb → Ingestion → RAG → Claude Summarization → Human Approval → PMWeb API")


def slide_contract_use_case(prs):
    s = add_blank_slide(prs)
    slide_chrome(s, "Section 02", "Use Case 2 — AI-Assisted Contract Summarization",
                 "Reduce manual effort with enterprise control")
    card(s, CONTENT_LEFT, CONTENT_TOP, Inches(5.4), Inches(1.65), "AI Clause Extraction", [
        "Payment, LDs, warranties, termination clauses",
        "Mapped to PMWeb contract schema fields",
    ])
    card(s, CONTENT_LEFT, CONTENT_TOP + Inches(1.85), Inches(5.4), Inches(1.55),
         "Auto-Population of PMWeb Fields", [
             "Governed API writes only — never AI-to-database",
             "Human-in-the-loop before record updates",
         ])
    card(s, Inches(6.35), CONTENT_TOP, Inches(6.35), Inches(3.4), "Contract Intelligence Workflow", [
        "1. Secure contract PDF ingestion",
        "2. OCR, chunking, vector indexing",
        f"3. {RECOMMENDED_AI} extracts clauses & summaries",
        "4. Orchestration validates schema + RBAC",
        "5. Analyst reviews with citations",
        "6. Approved data synced via PMWeb API",
        "Outcome: 60–80% reduction in manual effort",
    ], icon="contract.png")


def slide_chatbot_use_case(prs):
    s = add_blank_slide(prs)
    slide_chrome(s, "Section 02", "Use Case 3 — Management AI Chatbot",
                 "Conversational access to governed PMWeb intelligence")
    queries = [
        ("Project / Package Status", "Pipeline view across developments"),
        ("Building Configuration", "Typology, floors, areas, specifications"),
        ("Unit Mix", "Inventory by type, size, price band"),
        ("Design Parameters", "Design criteria and approval status"),
        ("Awarded Values", "Contract values, variations, commitments"),
        ("Vendor Insights", "Performance, awards, risk flags"),
    ]
    for i, (t, b) in enumerate(queries):
        col, row = i % 3, i // 3
        card(s, CONTENT_LEFT + col * Inches(4.02), CONTENT_TOP + row * Inches(1.72),
             Inches(3.85), Inches(1.55), t, [b])
    callout(s, CONTENT_LEFT, CONTENT_BOTTOM - Inches(0.48), CONTENT_WIDTH,
            "RBAC-filtered • Citation-linked • Audit-logged • No direct database inference")


def slide_risk_intro(prs):
    s = add_blank_slide(prs)
    slide_chrome(s, "Section 03", "Why Direct AI-to-PMWeb Is Risky",
                 "Ungoverned connectivity threatens data and decision integrity")
    risks = [
        ("Direct DB Access", "SQL/DB credentials create exposure and injection risk."),
        ("Hallucinations", "Fabricated figures or clauses are catastrophic in procurement."),
        ("Security Breach", "Uncontrolled prompts may leak PII and commercial terms."),
        ("No Governance", "Shadow AI bypasses DAMAC policies and data residency."),
        ("No Traceability", "Leadership cannot explain how answers were produced."),
        ("Inaccurate Answers", "Stale embeddings and wrong document versions."),
    ]
    for i, (t, b) in enumerate(risks):
        col, row = i % 3, i // 3
        card(s, CONTENT_LEFT + col * Inches(4.02), CONTENT_TOP + row * Inches(1.72),
             Inches(3.85), Inches(1.55), t, [b])
    callout(s, CONTENT_LEFT, CONTENT_BOTTOM - Inches(0.48), CONTENT_WIDTH,
            '"AI should explain enterprise truth, not derive uncontrolled truth."')


def slide_risk_diagram(prs):
    s = add_blank_slide(prs)
    slide_chrome(s, "Section 03", "Anti-Pattern vs Recommended Pattern",
                 "Architecture decision with enterprise consequences")
    rect(s, CONTENT_LEFT, CONTENT_TOP, Inches(5.6), Inches(4.35), LIGHT_GRAY, BORDER, radius=True)
    textbox(s, CONTENT_LEFT + Inches(0.2), CONTENT_TOP + Inches(0.12), Inches(4), Inches(0.3),
            "✕  ANTI-PATTERN", FS_BODY, True, RED)
    cx = CONTENT_LEFT + Inches(1.0)
    y = CONTENT_TOP + Inches(0.65)
    for lbl in ["Claude / OpenAI", "Direct DB / SQL", "PMWeb Database"]:
        arch_box(s, cx, y, Inches(3.6), Inches(0.58), lbl)
        textbox(s, cx + Inches(1.65), y + Inches(0.58), Inches(0.3), Inches(0.25), "▼", FS_BODY, True, RED, PP_ALIGN.CENTER)
        y += Inches(0.88)
    textbox(s, CONTENT_LEFT + Inches(0.2), y + Inches(0.1), Inches(5), Inches(0.3),
            "No RBAC • No citations • No audit", FS_CAPTION, False, MUTED)

    rect(s, Inches(6.95), CONTENT_TOP, Inches(5.75), Inches(4.35), RED_TINT, RED, radius=True)
    textbox(s, Inches(7.15), CONTENT_TOP + Inches(0.12), Inches(4), Inches(0.3),
            "✓  RECOMMENDED", FS_BODY, True, RED_DARK)
    y = CONTENT_TOP + Inches(0.55)
    for lbl in ["Management Experience", "AI Orchestration + Governance",
                "Enterprise Knowledge Layer", "API / Integration Layer", "PMWeb"]:
        arch_box(s, Inches(7.5), y, Inches(4.7), Inches(0.52), lbl, highlight=(lbl == "PMWeb"))
        y += Inches(0.62)


def slide_architecture(prs):
    s = add_blank_slide(prs)
    slide_chrome(s, "Section 04", "Recommended Enterprise Architecture",
                 "Governed intelligence layer — API-first, auditable, cloud-native")
    draw_architecture_stack(s)


def slide_rag_architecture(prs):
    s = add_blank_slide(prs)
    slide_chrome(s, "Section 04", "RAG & Knowledge Architecture",
                 "Retrieval-augmented generation with enterprise controls")
    draw_rag_pipeline(s)
    comps = [
        ("Document Ingestion", "PDF, Word, PMWeb exports — OCR and classification"),
        ("Orchestration Engine", "Policy routing, fallbacks, evaluation hooks"),
        ("AI Governance Layer", "PII redaction, output validation, kill switch"),
        ("PMWeb APIs", "Read via APIs; write only after human approval"),
    ]
    col_gap = Inches(0.35)
    card_w = (CONTENT_WIDTH - col_gap) / 2
    card_h = Inches(1.08)
    y2 = CONTENT_TOP + Inches(0.92)
    row_gap = Inches(0.28)
    positions = [
        (CONTENT_LEFT, y2),
        (CONTENT_LEFT + card_w + col_gap, y2),
        (CONTENT_LEFT, y2 + card_h + row_gap),
        (CONTENT_LEFT + card_w + col_gap, y2 + card_h + row_gap),
    ]
    for (left, top), (t, b) in zip(positions, comps):
        card(s, left, top, card_w, card_h, t, [b])


def slide_model_comparison(prs):
    s = add_blank_slide(prs)
    slide_chrome(s, "Section 05", "AI Model Comparison",
                 "Enterprise evaluation — single recommended platform")
    headers = ["Capability", "Claude Enterprise", "OpenAI GPT-5/4.1", "Azure OpenAI", "Gemini"]
    rows = [
        ["Document Summarization", "★★★★★", "★★★★☆", "★★★★☆", "★★★★☆"],
        ["Contract Analysis", "★★★★★", "★★★★☆", "★★★★☆", "★★★☆☆"],
        ["Hallucination Control", "★★★★★", "★★★★☆", "★★★★☆", "★★★☆☆"],
        ["Governance Capability", "★★★★★", "★★★★☆", "★★★★★", "★★★★☆"],
        ["Context Window", "200K–1M", "128K–1M", "128K", "1M–2M"],
        ["Enterprise Readiness", "★★★★★", "★★★★★", "★★★★★", "★★★★☆"],
        ["PMWeb Fit (DAMAC)", "★★★★★", "★★★★☆", "★★★★☆", "★★★☆☆"],
    ]
    add_table(s, CONTENT_LEFT, CONTENT_TOP, CONTENT_WIDTH, Inches(3.6), headers, rows)
    callout(s, CONTENT_LEFT, CONTENT_BOTTOM - Inches(0.5), CONTENT_WIDTH,
            f"Recommendation: {RECOMMENDED_AI} — best fit for contract, tender & document intelligence")


def slide_model_recommendation(prs):
    s = add_blank_slide(prs)
    slide_chrome(s, "Section 05", "Recommended Platform",
                 f"Single enterprise AI standard for DAMAC PMWeb intelligence")
    rect(s, CONTENT_LEFT, CONTENT_TOP, CONTENT_WIDTH, Inches(4.2), RED_TINT, RED, radius=True)
    if (ICONS / "ai.png").exists():
        add_image(s, ICONS / "ai.png", CONTENT_LEFT + Inches(0.3), CONTENT_TOP + Inches(0.35), height=Inches(0.85))
    rect(s, CONTENT_LEFT + Inches(1.2), CONTENT_TOP + Inches(0.28), Inches(1.55), Inches(0.36), RED, radius=True)
    textbox(s, CONTENT_LEFT + Inches(1.3), CONTENT_TOP + Inches(0.33), Inches(1.4), Inches(0.3),
            "RECOMMENDED", FS_CAPTION, True, WHITE, PP_ALIGN.CENTER)
    textbox(s, CONTENT_LEFT + Inches(1.15), CONTENT_TOP + Inches(0.88), Inches(10.5), Inches(0.65),
            RECOMMENDED_AI, FS_TITLE, True, BLACK)
    bullets(s, CONTENT_LEFT + Inches(1.15), CONTENT_TOP + Inches(1.65), Inches(10.5), Inches(2.4), [
        "Primary enterprise AI for DAMAC PMWeb governance layer",
        "Industry-leading document & contract summarization with long context",
        "Lowest hallucination risk for legal, commercial, and procurement text",
        "Strong enterprise governance: RBAC integration, audit, data controls",
        "Consistent model family (Haiku / Sonnet / Opus) for cost-tiered workloads",
        "Unified vendor relationship simplifies security review and DPAs",
    ], FS_BODY, TEXT)
    rect(s, CONTENT_LEFT, Inches(5.75), CONTENT_WIDTH, Inches(0.52), BLACK, radius=True)
    textbox(s, CONTENT_LEFT + Inches(0.2), Inches(5.86), CONTENT_WIDTH - Inches(0.4), Inches(0.35),
            "One platform. One governance model. Orchestration layer routes Haiku → Sonnet → Opus by task complexity.",
            FS_BODY, True, WHITE, PP_ALIGN.CENTER)


def slide_pricing_tokens(prs):
    s = add_blank_slide(prs)
    slide_chrome(s, "Section 06", "Claude Enterprise API Pricing",
                 "Per-million-token rates — primary cost model for DAMAC")
    headers = ["Claude Model", "Input ($/1M)", "Output ($/1M)", "DAMAC Use Case"]
    rows = [
        ["Haiku 4.5", "$0.80", "$4.00", "Retrieval, classification, chatbot triage"],
        ["Sonnet 4.5", "$3.00", "$15.00", "Contract & tender summarization"],
        ["Opus 4.5", "$15.00", "$75.00", "Complex contracts, executive summaries"],
    ]
    add_table(s, CONTENT_LEFT, CONTENT_TOP, Inches(8.5), Inches(1.6), headers, rows)
    textbox(s, CONTENT_LEFT, CONTENT_TOP + Inches(1.85), Inches(11), Inches(0.3),
            "Reference pricing (May 2026 indicative). Competitors shown for context only.", FS_CAPTION, False, MUTED)
    headers2 = ["Provider", "Comparable Tier", "Input", "Output"]
    rows2 = [
        ["OpenAI", "GPT-4.1", "$2.00", "$8.00"],
        ["Azure OpenAI", "GPT-4.1", "$2.20", "$8.80"],
        ["Gemini", "Enterprise", "$1.50", "$6.00"],
    ]
    add_table(s, CONTENT_LEFT, CONTENT_TOP + Inches(2.25), Inches(8.5), Inches(1.5), headers2, rows2)
    bullets(s, CONTENT_LEFT, CONTENT_TOP + Inches(3.95), Inches(11), Inches(1.35), [
        "DAMAC standardizes on Claude — no multi-vendor routing complexity",
        "Prompt caching: up to 90% savings on repeated contract templates",
        "RAG reduces tokens sent to Sonnet/Opus by pre-filtering relevant chunks",
    ], FS_BODY)


def slide_pricing_scenarios(prs):
    s = add_blank_slide(prs)
    slide_chrome(s, "Section 06", "Monthly Enterprise Cost Scenarios",
                 f"Realistic DAMAC workloads — {RECOMMENDED_AI}")
    headers = ["Scenario", "Volume", "Claude Tier", "Est. Monthly (USD)"]
    rows = [
        ["Contract Summaries", "1,000 / month", "Sonnet + Haiku", "$8,500 – $14,000"],
        ["Tender Summarizations", "200 / month", "Sonnet (long docs)", "$4,200 – $7,500"],
        ["Management Chatbot", "500 users × 20 queries/day", "Haiku + Sonnet", "$5,500 – $10,500"],
        ["Combined (Phase 3)", "All workloads + caching", "Tiered routing", "$16,000 – $28,000"],
        ["Full Platform (Phase 4)", "All + governance infra", "Full stack", "$30,000 – $48,000"],
    ]
    add_table(s, CONTENT_LEFT, CONTENT_TOP, CONTENT_WIDTH, Inches(2.6), headers, rows)
    textbox(s, CONTENT_LEFT, CONTENT_TOP + Inches(2.85), Inches(4), Inches(0.35),
            "Cost Optimization Strategies", FS_BODY, True, RED)
    bullets(s, CONTENT_LEFT, CONTENT_TOP + Inches(3.25), Inches(11), Inches(2.0), [
        "Prompt caching for repeated tender and contract templates",
        "Haiku for retrieval and chatbot triage; Sonnet for synthesis; Opus for complex packs only",
        "RAG architecture limits context sent to premium models",
        "Batch off-peak processing for non-urgent summarization",
    ], FS_BODY)


def slide_pricing_detail(prs):
    s = add_blank_slide(prs)
    slide_chrome(s, "Section 06", "Per-Use-Case Cost Breakdown",
                 "Business case validation — Claude Enterprise only")
    headers = ["Use Case", "Token Assumption", "Model", "Cost / Unit", "Monthly Est."]
    rows = [
        ["Contract summary", "~80K in / 4K out", "Sonnet", "$0.28", "$12,000"],
        ["Tender BAFO pack", "~200K in / 8K out", "Sonnet", "$0.82", "$6,400"],
        ["Chatbot query", "~2K in / 500 out", "Haiku", "$0.003", "$6,500"],
        ["Executive summary", "~120K in / 6K out", "Opus", "$2.10", "$1,800"],
    ]
    add_table(s, CONTENT_LEFT, CONTENT_TOP, CONTENT_WIDTH, Inches(2.4), headers, rows)
    callout(s, CONTENT_LEFT, Inches(4.0), CONTENT_WIDTH,
            "Scenarios: 1,000 contracts + 200 tenders + 500 chatbot users ≈ $22,000 – $26,000 / month at scale")


def slide_roadmap(prs):
    s = add_blank_slide(prs)
    slide_chrome(s, "Section 07", "Phased Implementation Strategy",
                 "Full program scope delivered in 2–3 months — parallel workstreams where possible")
    phases = [
        ("PHASE 1", "Contract Summarization POC", "Weeks 1–3",
         ["PMWeb API integration", "RAG MVP", "Claude extraction", "Approval UI"]),
        ("PHASE 2", "Tender Recommendation Engine", "Weeks 4–6",
         ["BAFO automation", "Deviation detection", "Benchmarking", "PMWeb workflows"]),
        ("PHASE 3", "Executive AI Chatbot", "Weeks 7–9",
         ["Management queries", "RBAC + citations", "500-user pilot", "PMWeb sync"]),
        ("PHASE 4", "AI Governance Platform", "Weeks 10–12",
         ["Full audit & compliance", "Governance control plane", "DAMAC AI standards"]),
    ]
    pw = Inches(2.9)
    for i, (ph, title, time, items) in enumerate(phases):
        left = CONTENT_LEFT + i * Inches(3.02)
        rect(s, left, CONTENT_TOP, pw, Inches(4.1), WHITE, RED if i == 0 else BORDER, radius=True)
        textbox(s, left + Inches(0.12), CONTENT_TOP + Inches(0.12), pw - Inches(0.24), Inches(0.25), ph, FS_CAPTION, True, RED)
        textbox(s, left + Inches(0.12), CONTENT_TOP + Inches(0.4), pw - Inches(0.24), Inches(0.5), title, FS_BODY, True, BLACK)
        rect(s, left + Inches(0.12), CONTENT_TOP + Inches(0.95), pw - Inches(0.24), Inches(0.32), RED if i == 0 else BORDER, radius=True)
        textbox(s, left + Inches(0.12), CONTENT_TOP + Inches(0.98), pw - Inches(0.24), Inches(0.28),
                time, FS_CAPTION, True, WHITE if i == 0 else RED, PP_ALIGN.CENTER)
        bullets(s, left + Inches(0.12), CONTENT_TOP + Inches(1.4), pw - Inches(0.24), Inches(2.5), items, FS_BODY, MUTED)


def slide_delivery_slope(prs):
    """Define delivery slope: value & capability ramp over the 2–3 month program."""
    s = add_blank_slide(prs)
    slide_chrome(s, "Section 07", "Delivery Slope Definition",
                 "How capability, effort, and business value accelerate across the program")
    add_diagram(s, "delivery_slope_cards.png", CONTENT_LEFT, CONTENT_TOP,
                width=CONTENT_WIDTH, height=Inches(1.28))
    add_diagram(s, "delivery_slope_chart.png", CONTENT_LEFT, CONTENT_TOP + Inches(1.38),
                width=CONTENT_WIDTH, height=Inches(2.55))
    callout(s, CONTENT_LEFT, CONTENT_BOTTOM - Inches(0.5), CONTENT_WIDTH,
            "Target: complete Phases 1–4 in 2–3 months | Accelerated track: ~8–10 weeks with parallel squads")


def slide_roadmap_timeline(prs):
    s = add_blank_slide(prs)
    slide_chrome(s, "Section 07", "Implementation Timeline",
                 "Total program duration: 2–3 months (10–12 weeks)")
    milestones = [
        ("Weeks 1–3", "Phase 1", "Contract POC"),
        ("Weeks 4–6", "Phase 2", "Tender Engine"),
        ("Weeks 7–9", "Phase 3", "Chatbot"),
        ("Weeks 10–12", "Phase 4", "Governance Platform"),
    ]
    rect(s, CONTENT_LEFT, CONTENT_TOP + Inches(1.5), CONTENT_WIDTH, Inches(0.06), RED)
    n = len(milestones)
    step = CONTENT_WIDTH / n
    for i, (time, phase, desc) in enumerate(milestones):
        left = CONTENT_LEFT + i * step + Inches(0.1)
        rect(s, left + step / 2 - Inches(0.06), CONTENT_TOP + Inches(1.35), Inches(0.12), Inches(0.22), RED)
        rect(s, left, CONTENT_TOP + Inches(1.75), step - Inches(0.25), Inches(1.65), WHITE, BORDER, radius=True)
        textbox(s, left + Inches(0.1), CONTENT_TOP + Inches(1.88), step - Inches(0.4), Inches(0.25), time, FS_CAPTION, True, RED)
        textbox(s, left + Inches(0.1), CONTENT_TOP + Inches(2.15), step - Inches(0.4), Inches(0.3), phase, FS_BODY, True, BLACK)
        textbox(s, left + Inches(0.1), CONTENT_TOP + Inches(2.5), step - Inches(0.4), Inches(0.6), desc, FS_BODY, False, MUTED)
    callout(s, CONTENT_LEFT, CONTENT_BOTTOM - Inches(0.48), CONTENT_WIDTH,
            "Full scope (contract POC + tender engine + chatbot + governance platform) within 2–3 months")


def slide_security(prs):
    s = add_blank_slide(prs)
    slide_chrome(s, "Section 08", "Security & Governance Framework",
                 "Enterprise controls aligned to DAMAC policies")
    controls = [
        ("RBAC", "Aligned to PMWeb permissions — procurement, commercial, executive."),
        ("Audit Logging", "Who asked, which documents, which model, which output."),
        ("Prompt Logging", "Full capture for compliance and incident review."),
        ("AI Governance", "Approved models, data rules, output validation gates."),
        ("Human-in-the-Loop", "Mandatory approval before PMWeb writes."),
        ("Data Privacy", "PII redaction, encryption, UAE residency options."),
        ("DAMAC Controls", "SSO, retention policies, vendor DPAs, SOC2 providers."),
        ("Secure APIs", "API gateway, mTLS, vault — zero DB credentials to AI."),
    ]
    for i, (t, b) in enumerate(controls):
        col, row = i % 4, i // 4
        card(s, CONTENT_LEFT + col * Inches(3.02), CONTENT_TOP + row * Inches(2.05),
             Inches(2.85), Inches(1.85), t, [b])


def slide_governance_diagram(prs):
    s = add_blank_slide(prs)
    slide_chrome(s, "Section 08", "AI Governance Control Plane",
                 "Centralized policy enforcement across all workloads")
    cx, cy = Inches(5.15), Inches(3.85)
    rect(s, cx, cy, Inches(3.0), Inches(1.15), RED, radius=True)
    textbox(s, cx + Inches(0.1), cy + Inches(0.28), Inches(2.8), Inches(0.6),
            "AI Governance\nControl Plane", FS_BODY, True, WHITE, PP_ALIGN.CENTER)
    orbit = [
        (Inches(0.55), Inches(2.55), "RBAC & SSO"),
        (Inches(9.85), Inches(2.55), "Audit & Compliance"),
        (Inches(0.55), Inches(4.85), "Prompt Management"),
        (Inches(9.85), Inches(4.85), "Model Allowlist"),
        (Inches(3.2), Inches(5.55), "Human Approval"),
        (Inches(7.1), Inches(5.55), "Data Classification"),
    ]
    for left, top, label in orbit:
        arch_box(s, left, top, Inches(2.55), Inches(0.68), label)


def slide_future_vision(prs):
    s = add_blank_slide(prs)
    slide_chrome(s, "Section 09", "Future Vision — DAMAC AI Governance Platform",
                 "Enterprise-wide procurement and project intelligence")
    caps = [
        ("Predictive Procurement", "Pricing trends, bid competitiveness, award outcomes"),
        ("AI Risk Scoring", "Vendor and subcontractor risk across portfolio"),
        ("Vendor Performance", "SLA compliance and anomaly patterns"),
        ("Anomaly Detection", "Unusual pricing, scope gaps, compliance deviations"),
        ("Project Intelligence", "Cross-project cost, schedule, design insights"),
        ("Executive Copilots", "AI advisors for CEO, CFO, procurement leadership"),
    ]
    for i, (t, b) in enumerate(caps):
        col, row = i % 3, i // 3
        card(s, CONTENT_LEFT + col * Inches(4.02), CONTENT_TOP + row * Inches(1.72),
             Inches(3.85), Inches(1.55), t, [b])
    callout(s, CONTENT_LEFT, CONTENT_BOTTOM - Inches(0.48), CONTENT_WIDTH,
            "Vision: DAMAC AI Governance Platform — trusted intelligence for all enterprise decisions")


def slide_final_recommendation(prs):
    s = add_blank_slide(prs)
    slide_chrome(s, "Section 10", "Final Recommendation",
                 "Consulting conclusion — governed enterprise AI for DAMAC")
    bullets(s, CONTENT_LEFT, CONTENT_TOP, Inches(7.2), Inches(4.2), [
        "Build the Enterprise AI Orchestration Layer first — before production AI workloads.",
        "Avoid direct AI-to-database architecture — API-first governed PMWeb connectivity only.",
        f"Standardize on {RECOMMENDED_AI} as the enterprise AI platform for PMWeb intelligence.",
        "Deploy AI as a governed layer that explains enterprise truth with citations.",
        "Start with Contract Intelligence POC (Phase 1) — demonstrable value by Week 3.",
        "Complete full program scope in 2–3 months (Phases 1–4).",
    ], FS_BODY)
    rect(s, Inches(8.2), CONTENT_TOP, Inches(4.5), Inches(3.5), RED_TINT, RED, radius=True)
    textbox(s, Inches(8.4), CONTENT_TOP + Inches(0.2), Inches(4.1), Inches(0.4), "Decision Ask", FS_BODY, True, RED)
    bullets(s, Inches(8.4), CONTENT_TOP + Inches(0.7), Inches(4.1), Inches(2.6), [
        "Approve Phase 1 POC budget & team",
        "Nominate DAMAC executive sponsor",
        "Confirm PMWeb API access scope",
        "Approve Claude Enterprise as AI standard",
        "Establish AI governance steering committee",
    ], FS_BODY, TEXT)
    callout(s, CONTENT_LEFT, CONTENT_BOTTOM - Inches(0.48), CONTENT_WIDTH,
            "Build the intelligence layer that governs how AI serves DAMAC — not ungoverned connectivity.")


def slide_thank_you(prs):
    s = add_blank_slide(prs)
    fill_bg(s, WHITE)
    rect(s, Inches(0), Inches(0), SLIDE_W, Inches(0.04), RED)
    draw_cmcs_logo(s)
    textbox(s, MARGIN, Inches(2.6), CONTENT_WIDTH, Inches(0.8), "Thank You", FS_DISPLAY, True, BLACK, PP_ALIGN.CENTER)
    textbox(s, MARGIN, Inches(3.55), CONTENT_WIDTH, Inches(0.4),
            "Enterprise AI Governance & Intelligence Layer for PMWeb", FS_BODY, False, RED, PP_ALIGN.CENTER)
    textbox(s, MARGIN, Inches(4.15), CONTENT_WIDTH, Inches(0.35),
            "CMCS  |  Confidential", FS_BODY, False, MUTED, PP_ALIGN.CENTER)
    draw_footer(s)


def build_presentation(output_path: Path) -> Path:
    # Ensure logos exist
    if not (DIAGRAMS / "agenda.png").exists():
        import subprocess
        subprocess.run(["python3", str(Path(__file__).parent / "create_assets.py")], check=True)

    prs = prs_blank()
    slide_title(prs)
    slide_agenda(prs)

    slide_section_divider(prs, "01", "Executive Summary", "Challenges, opportunity, and transformation")
    slide_exec_summary(prs)
    slide_challenges(prs)
    slide_current_vs_future(prs)

    slide_section_divider(prs, "02", "DAMAC PMWeb Use Cases", "Commitment, contracts, management chatbot")
    slide_use_cases_intro(prs)
    slide_commitment_use_case(prs)
    slide_contract_use_case(prs)
    slide_chatbot_use_case(prs)

    slide_section_divider(prs, "03", "Why Direct AI-to-PMWeb Is Risky", "Governed truth, not uncontrolled inference")
    slide_risk_intro(prs)
    slide_risk_diagram(prs)

    slide_section_divider(prs, "04", "Recommended Enterprise Architecture", "API-first orchestration and RAG")
    slide_architecture(prs)
    slide_rag_architecture(prs)

    slide_section_divider(prs, "05", "AI Model Comparison", f"Single recommendation: {RECOMMENDED_AI}")
    slide_model_comparison(prs)
    slide_model_recommendation(prs)

    slide_section_divider(prs, "06", "Enterprise Pricing", "Claude-centric cost model and scenarios")
    slide_pricing_tokens(prs)
    slide_pricing_scenarios(prs)
    slide_pricing_detail(prs)

    slide_section_divider(prs, "07", "Implementation Strategy", "2–3 month delivery | slope, phases & timeline")
    slide_roadmap(prs)
    slide_delivery_slope(prs)
    slide_roadmap_timeline(prs)

    slide_section_divider(prs, "08", "Security & Governance", "RBAC, audit, human-in-the-loop")
    slide_security(prs)
    slide_governance_diagram(prs)

    slide_section_divider(prs, "09", "Future Vision", "DAMAC AI Governance Platform")
    slide_future_vision(prs)

    slide_section_divider(prs, "10", "Final Recommendation", "Decision ask and next steps")
    slide_final_recommendation(prs)
    slide_thank_you(prs)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(output_path))
    return output_path


if __name__ == "__main__":
    out = Path(__file__).resolve().parents[1] / "output" / "DAMAC_PMWeb_AI_Governance_Intelligence_Layer.pptx"
    path = build_presentation(out)
    print(f"Generated: {path} ({path.stat().st_size // 1024} KB)")
