#!/usr/bin/env python3
"""Generate CMCS and DAMAC logo PNGs for the presentation."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ASSETS = Path(__file__).resolve().parents[1] / "assets"
RED = (227, 24, 55)
BLACK = (10, 10, 10)
WHITE = (255, 255, 255)
DAMAC_GOLD = (180, 151, 90)


def _font(size: int, bold: bool = False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def create_cmcs_logo(path: Path, width: int = 420, height: int = 120):
    img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    font = _font(52, bold=True)
    text = "CMCS"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (width - tw) // 2 - 10
    y = (height - th) // 2 - 4
    draw.text((x, y), text, fill=BLACK, font=font)
    draw.text((x + tw - 2, y - 8), "TM", fill=BLACK, font=_font(12, bold=True))
    # Red swooshes
    draw.arc([x - 45, y - 35, x + tw + 35, y + th + 15], 200, 340, fill=RED, width=5)
    draw.arc([x - 35, y - 5, x + tw + 45, y + th + 40], 160, 300, fill=RED, width=5)
    img.save(path, "PNG")


def create_damac_logo(path: Path, width: int = 380, height: int = 100):
    img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    font = _font(44, bold=True)
    text = "DAMAC"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (width - tw) // 2
    y = 18
    # Elegant wordmark style
    draw.text((x, y), text, fill=BLACK, font=font)
    draw.rectangle([x, y + 58, x + tw, y + 62], fill=DAMAC_GOLD)
    draw.text((x, y + 68), "PROPERTIES", fill=(90, 90, 90), font=_font(11, bold=True))
    img.save(path, "PNG")


if __name__ == "__main__":
    ASSETS.mkdir(parents=True, exist_ok=True)
    create_cmcs_logo(ASSETS / "cmcs_logo.png")
    create_damac_logo(ASSETS / "damac_logo.png")
    print(f"Logos saved to {ASSETS}")
