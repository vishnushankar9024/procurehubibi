#!/usr/bin/env python3
"""Generate logos, icons, and decorative PNG assets for the DAMAC deck."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ASSETS = Path(__file__).resolve().parents[1] / "assets"
ICONS = ASSETS / "icons"
RED = (227, 24, 55)
RED_LIGHT = (253, 242, 244)
BLACK = (26, 26, 26)
GRAY = (107, 107, 107)
WHITE = (255, 255, 255)
GOLD = (180, 151, 90)


def _font(size: int, bold: bool = False):
    for name in (
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        "LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf",
    ):
        for base in ("/usr/share/fonts/truetype/dejavu/", "/usr/share/fonts/truetype/liberation/"):
            try:
                return ImageFont.truetype(base + name, size)
            except OSError:
                continue
    return ImageFont.load_default()


def create_cmcs_logo(path: Path):
    """Clean wordmark only — no swoosh / parabolic accents."""
    w, h = 400, 90
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = _font(52, True)
    text = "CMCS"
    bb = d.textbbox((0, 0), text, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    x, y = (w - tw) // 2, (h - th) // 2 - 4
    d.text((x, y), text, fill=BLACK, font=f)
    d.text((x + tw + 2, y - 4), "™", fill=BLACK, font=_font(12, True))
    img.save(path, "PNG")


def create_damac_logo(path: Path):
    w, h = 440, 120
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = _font(48, True)
    text = "DAMAC"
    bb = d.textbbox((0, 0), text, font=f)
    tw = bb[2] - bb[0]
    x = (w - tw) // 2
    d.text((x, 16), text, fill=BLACK, font=f)
    d.rectangle([x, 74, x + tw, 78], fill=GOLD)
    d.text((x + tw // 2 - 52, 84), "PROPERTIES", fill=GRAY, font=_font(12, True))
    img.save(path, "PNG")


def _icon_base(size=96):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([4, 4, size - 5, size - 5], fill=RED_LIGHT, outline=RED, width=3)
    return img, d, size


def icon_document(path: Path):
    img, d, s = _icon_base()
    m = s // 5
    d.rounded_rectangle([m + 8, m, s - m, s - m - 6], radius=8, outline=RED, width=3, fill=WHITE)
    d.line([m + 22, m + 22, s - m - 8, m + 22], fill=RED, width=2)
    d.line([m + 14, m + 38, s - m - 14, m + 38], fill=GRAY, width=2)
    d.line([m + 14, m + 52, s - m - 30, m + 52], fill=GRAY, width=2)
    img.save(path, "PNG")


def icon_contract(path: Path):
    img, d, s = _icon_base()
    m = s // 5
    d.rectangle([m + 6, m + 8, s - m - 6, s - m - 10], outline=RED, width=3, fill=WHITE)
    d.line([m + 14, m + 30, s - m - 14, m + 30], fill=RED, width=2)
    d.text((m + 18, m + 40), "§", fill=RED, font=_font(22, True))
    img.save(path, "PNG")


def icon_chat(path: Path):
    img, d, s = _icon_base()
    m = s // 5
    d.rounded_rectangle([m, m + 6, s - m - 4, s - m - 18], radius=12, outline=RED, width=3, fill=WHITE)
    d.polygon([(m + 18, s - m - 18), (m + 34, s - m - 6), (m + 40, s - m - 22)], fill=RED)
    d.ellipse([m + 22, m + 28, m + 34, m + 40], fill=RED)
    d.ellipse([m + 42, m + 28, m + 54, m + 40], fill=RED)
    d.ellipse([m + 62, m + 28, m + 74, m + 40], fill=RED)
    img.save(path, "PNG")


def icon_ai(path: Path):
    img, d, s = _icon_base()
    cx, cy = s // 2, s // 2 - 2
    d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], outline=RED, width=3, fill=WHITE)
    d.line([cx - 12, cy + 6, cx - 4, cy - 4], fill=RED, width=3)
    d.line([cx - 4, cy - 4, cx + 14, cy + 10], fill=RED, width=3)
    d.ellipse([cx - 8, cy - 10, cx - 2, cy - 4], fill=RED)
    d.ellipse([cx + 4, cy - 10, cx + 10, cy - 4], fill=RED)
    img.save(path, "PNG")


def icon_governance(path: Path):
    img, d, s = _icon_base()
    m = s // 5
    d.rectangle([m + 20, m + 8, s - m - 20, m + 22], fill=RED, outline=RED)
    d.rectangle([m + 10, m + 28, s - m - 10, s - m - 12], outline=RED, width=3, fill=WHITE)
    d.line([m + 28, m + 44, s - m - 28, m + 44], fill=GRAY, width=2)
    d.line([m + 28, m + 58, s - m - 28, m + 58], fill=GRAY, width=2)
    img.save(path, "PNG")


def icon_risk(path: Path):
    img, d, s = _icon_base()
    cx = s // 2
    d.polygon([(cx, 14), (s - 18, s - 22), (18, s - 22)], outline=RED, fill=RED_LIGHT, width=3)
    d.text((cx - 8, s // 2 - 6), "!", fill=RED, font=_font(28, True))
    img.save(path, "PNG")


def icon_architecture(path: Path):
    img, d, s = _icon_base()
    m, cx = s // 5, s // 2
    d.rectangle([cx - 28, m + 34, cx + 28, s - m - 8], fill=RED, outline=RED)
    d.rectangle([cx - 18, m + 22, cx + 18, m + 36], fill=WHITE, outline=RED, width=2)
    d.rectangle([cx - 10, m + 10, cx + 10, m + 24], fill=WHITE, outline=RED, width=2)
    img.save(path, "PNG")


def icon_quote(path: Path):
    img, d, s = _icon_base(88)
    d.text((22, 18), "\u201c", fill=RED, font=_font(48, True))
    d.text((48, 38), "\u201d", fill=RED, font=_font(36, True))
    img.save(path, "PNG")


def icon_timeline(path: Path):
    img, d, s = _icon_base()
    m = s // 5
    d.line([m + 12, s // 2, s - m - 12, s // 2], fill=RED, width=4)
    for i, xi in enumerate([m + 16, s // 2 - 4, s - m - 24]):
        d.ellipse([xi, s // 2 - 8, xi + 16, s // 2 + 8], fill=RED if i == 2 else WHITE, outline=RED, width=2)
    img.save(path, "PNG")


DIAGRAMS = ASSETS / "diagrams"


def _rounded_rect(d, xy, radius, fill, outline=None, width=1):
    x0, y0, x1, y1 = xy
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def create_agenda_diagram(path: Path):
    """Two-column executive agenda with clear numbering."""
    w, h = 1800, 920
    img = Image.new("RGB", (w, h), WHITE)
    d = ImageDraw.Draw(img)
    items = [
        "Executive Summary & Current vs Future State",
        "DAMAC PMWeb Use Cases",
        "Why Direct AI-to-PMWeb Is Risky",
        "Recommended Enterprise Architecture",
        "AI Model Comparison & Recommendation",
        "Enterprise Pricing & Cost Optimization",
        "Phased Implementation Strategy",
        "Security, Governance & Controls",
        "Future Vision — DAMAC AI Governance Platform",
        "Final Recommendation",
    ]
    f_num = _font(22, True)
    f_txt = _font(26, False)
    col_x = [80, 920]
    row_h = 82
    start_y = 40
    for i, text in enumerate(items):
        col = i // 5
        row = i % 5
        x = col_x[col]
        y = start_y + row * row_h
        cx, cy = x + 28, y + 34
        d.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill=RED)
        num = str(i + 1)
        nb = d.textbbox((0, 0), num, font=f_num)
        d.text((cx - (nb[2] - nb[0]) // 2, cy - (nb[3] - nb[1]) // 2 - 2), num, fill=WHITE, font=f_num)
        d.text((x + 72, y + 18), text, fill=BLACK, font=f_txt)
        if row < 4:
            d.line([cx, cy + 32, cx, y + row_h + 6], fill=(220, 220, 220), width=2)
    img.save(path, "PNG")


def create_architecture_diagram(path: Path):
    """Enterprise layer stack diagram."""
    w, h = 1600, 1080
    img = Image.new("RGB", (w, h), WHITE)
    d = ImageDraw.Draw(img)
    layers = [
        ("Management Experience Layer", "Dashboards · Chatbot · Approvals · Citations", False),
        ("Claude Enterprise", "Document intelligence · Reasoning · Summarization", True),
        ("AI Orchestration Layer", "Guardrails · Human-in-loop · Audit · Cost control", False),
        ("Enterprise Knowledge Layer", "Vector DB · RAG · Ingestion · Versioning", False),
        ("API / Integration Layer", "PMWeb APIs · ETL · Schema validation", False),
        ("PMWeb", "System of record — contracts, tenders, projects", False),
    ]
    bw, bh = 1320, 118
    x0 = (w - bw) // 2
    y = 30
    f_t = _font(28, True)
    f_s = _font(20, False)
    for title, sub, highlight in layers:
        fill = RED_LIGHT if highlight else WHITE
        outline = RED if highlight else (210, 210, 210)
        _rounded_rect(d, [x0, y, x0 + bw, y + bh], 14, fill, outline, 3 if highlight else 1)
        if highlight:
            d.rectangle([x0, y, x0 + 8, y + bh], fill=RED)
        d.text((x0 + 24, y + 18), title, fill=RED if highlight else BLACK, font=f_t)
        d.text((x0 + 24, y + 62), sub, fill=GRAY, font=f_s)
        ay = y + bh + 8
        if title != "PMWeb":
            d.polygon([(w // 2 - 12, ay), (w // 2 + 12, ay), (w // 2, ay + 16)], fill=RED)
        y += bh + 28
    # Foundation bar
    _rounded_rect(d, [x0, y + 10, x0 + bw, y + 58], 10, RED_LIGHT, RED, 2)
    cap = "RBAC  ·  Audit Logs  ·  Prompt Logging  ·  Citations  ·  Vector DB  ·  RAG"
    cb = d.textbbox((0, 0), cap, font=f_s)
    d.text((x0 + (bw - cb[2] + cb[0]) // 2, y + 22), cap, fill=RED, font=f_s)
    img.save(path, "PNG")


def create_delivery_slope_diagram(path: Path):
    """Value ramp bar chart with trend line."""
    w, h = 1500, 520
    img = Image.new("RGB", (w, h), WHITE)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, h], outline=(220, 220, 220), width=2)
    d.text((40, 24), "Value & Capability Ramp (2–3 Month Program)", fill=BLACK, font=_font(26, True))
    chart = [0.25, 0.48, 0.72, 1.0]
    labels = ["Foundation", "Accelerate", "Steep climb", "Enterprise"]
    weeks = ["Wk 1–3", "Wk 4–6", "Wk 7–9", "Wk 10–12"]
    x0, y0 = 120, 90
    cw, ch = w - 180, h - 160
    d.line([x0, y0 + ch, x0 + cw, y0 + ch], fill=GRAY, width=2)
    d.line([x0, y0, x0, y0 + ch], fill=GRAY, width=2)
    bar_w = cw // 5
    pts = []
    for i, (frac, lbl, wk) in enumerate(zip(chart, labels, weeks)):
        bx = x0 + 40 + i * bar_w
        bh = int(ch * frac)
        by = y0 + ch - bh
        col = RED if i >= 2 else (255, 200, 210)
        _rounded_rect(d, [bx, by, bx + bar_w - 20, y0 + ch], 8, col, RED, 2)
        d.text((bx + 8, y0 + ch + 12), wk, fill=RED, font=_font(18, True))
        tb = d.textbbox((0, 0), lbl, font=_font(16, False))
        d.text((bx + (bar_w - 20 - tb[2] + tb[0]) // 2, by - 28), lbl, fill=GRAY, font=_font(16, False))
        pts.append((bx + (bar_w - 20) // 2, by))
    d.line(pts, fill=RED, width=4)
    for p in pts:
        d.ellipse([p[0] - 6, p[1] - 6, p[0] + 6, p[1] + 6], fill=RED)
    d.text((x0 + 80, y0 + ch + 48), "Month 1", fill=GRAY, font=_font(18, False))
    d.text((x0 + cw // 3, y0 + ch + 48), "Month 2", fill=GRAY, font=_font(18, False))
    d.text((x0 + 2 * cw // 3 - 40, y0 + ch + 48), "Month 3  (10–12 weeks)", fill=GRAY, font=_font(18, False))
    img.save(path, "PNG")


def create_rag_pipeline_diagram(path: Path):
    """Horizontal RAG pipeline flow."""
    w, h = 1700, 280
    img = Image.new("RGB", (w, h), WHITE)
    d = ImageDraw.Draw(img)
    steps = ["PMWeb Docs", "Ingestion", "Embedding", "Vector DB", "RAG", "Claude", "Response"]
    n = len(steps)
    bw = 200
    gap = (w - n * bw) // (n + 1)
    f = _font(22, True)
    for i, lbl in enumerate(steps):
        x = gap + i * (bw + gap)
        y = 60
        hi = lbl == "Claude"
        _rounded_rect(d, [x, y, x + bw, y + 100], 12, RED_LIGHT if hi else WHITE, RED if hi else (210, 210, 210), 3 if hi else 1)
        bb = d.textbbox((0, 0), lbl, font=f)
        d.text((x + (bw - bb[2] + bb[0]) // 2, y + 36), lbl, fill=RED if hi else BLACK, font=f)
        if i < n - 1:
            ax = x + bw + 8
            d.polygon([(ax, y + 50), (ax + 28, y + 50), (ax + 14, y + 38)], fill=RED)
            d.polygon([(ax, y + 50), (ax + 28, y + 50), (ax + 14, y + 62)], fill=RED)
    img.save(path, "PNG")


def create_slope_cards_diagram(path: Path):
    """Two summary panels for delivery slope slide."""
    w, h = 1700, 340
    img = Image.new("RGB", (w, h), WHITE)
    d = ImageDraw.Draw(img)
    panels = [
        ("What Is the Delivery Slope?", [
            "Rate at which DAMAC gains governed AI capability and business value.",
            "Early weeks: foundation — APIs, RAG, governance shell.",
            "Mid program: tender intelligence and chatbot visibility.",
            "Final weeks: enterprise governance platform operational.",
        ]),
        ("Slope Dimensions", [
            "Technical maturity: POC → orchestration → control plane",
            "User adoption: analysts → procurement → executives",
            "Governance: audit → RBAC + citations → full HITL",
            "Business value: contracts → tenders → portfolio intelligence",
        ]),
    ]
    pw = (w - 60) // 2
    f_h = _font(24, True)
    f_b = _font(20, False)
    for i, (title, lines) in enumerate(panels):
        x = 20 + i * (pw + 20)
        _rounded_rect(d, [x, 10, x + pw, h - 10], 14, WHITE, RED, 2)
        d.rectangle([x, 10, x + 6, h - 10], fill=RED)
        d.text((x + 20, 28), title, fill=BLACK, font=f_h)
        yy = 72
        for line in lines:
            d.text((x + 28, yy), f"•  {line}", fill=GRAY, font=f_b)
            yy += 58
    img.save(path, "PNG")


def create_header_accent(path: Path):
    """Subtle slide header strip texture."""
    w, h = 1600, 120
    img = Image.new("RGBA", (w, h), (250, 250, 250, 255))
    d = ImageDraw.Draw(img)
    d.rectangle([0, h - 4, w, h], fill=RED)
    d.rectangle([0, 0, 6, h], fill=RED)
    img.save(path, "PNG")


if __name__ == "__main__":
    ASSETS.mkdir(parents=True, exist_ok=True)
    ICONS.mkdir(parents=True, exist_ok=True)
    DIAGRAMS.mkdir(parents=True, exist_ok=True)
    create_cmcs_logo(ASSETS / "cmcs_logo.png")
    create_agenda_diagram(DIAGRAMS / "agenda.png")
    create_architecture_diagram(DIAGRAMS / "architecture_stack.png")
    create_delivery_slope_diagram(DIAGRAMS / "delivery_slope_chart.png")
    create_slope_cards_diagram(DIAGRAMS / "delivery_slope_cards.png")
    create_rag_pipeline_diagram(DIAGRAMS / "rag_pipeline.png")
    icon_document(ICONS / "document.png")
    icon_contract(ICONS / "contract.png")
    icon_chat(ICONS / "chat.png")
    icon_ai(ICONS / "ai.png")
    icon_governance(ICONS / "governance.png")
    icon_risk(ICONS / "risk.png")
    icon_architecture(ICONS / "architecture.png")
    icon_quote(ICONS / "quote.png")
    icon_timeline(ICONS / "timeline.png")
    print(f"Assets ready: {ASSETS}")
