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
    create_cmcs_logo(ASSETS / "cmcs_logo.png")
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
