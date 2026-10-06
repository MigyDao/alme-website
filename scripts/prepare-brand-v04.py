"""Prepare web derivatives from the approved v04 ZIP without redrawing artwork.

Usage: python scripts/prepare-brand-v04.py PATH_TO_EXTRACTED_V04_PACKAGE
Requires Pillow and Windows Bahnschrift/Segoe UI fonts for the share graphic.
"""
from pathlib import Path
import hashlib
import json
import shutil
import sys
from PIL import Image, ImageDraw, ImageFont

repo = Path(__file__).resolve().parents[1]
source = Path(sys.argv[1]).resolve()
output = repo / "public/assets/brand"
output.mkdir(parents=True, exist_ok=True)
manifest = json.loads((source / "08 Source - Editable Assets/brand-manifest-v04.json").read_text(encoding="utf-8-sig"))
used = [
    "01 Logos/ALME-Primary-Horizontal-Full-Colour-v04.png",
    "01 Logos/ALME-Small-Icon-Full-Colour-v04.png",
    "08 Source - Editable Assets/ALME-Mark-White-v04.svg",
]
records = []
for name in used:
    path = source / name
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    record = next(item for item in manifest["files"] if item["path"] == name)
    assert record["sha256"] == digest, f"Manifest mismatch: {name}"
    records.append({"source": name, "sha256": digest, "drive_url": record["drive_url"]})

# Trim only transparent canvas, retaining clear space and every artwork pixel.
primary = Image.open(source / used[0]).convert("RGBA")
x0, y0, x1, y1 = primary.getchannel("A").getbbox()
primary = primary.crop((x0 - 50, y0 - 50, x1 + 50, y1 + 50))
header = primary.resize((640, round(640 * primary.height / primary.width)), Image.Resampling.LANCZOS)
header.save(output / "alme-primary-horizontal-v04.png", optimize=True)
shutil.copyfile(source / used[2], output / "alme-mark-white-v04.svg")

icon = Image.open(source / used[1]).convert("RGBA")
icon = icon.crop(icon.getchannel("A").getbbox())
def square_icon(size):
    canvas = Image.new("RGBA", (size, size), "#FBF5EA")
    artwork = icon.copy()
    artwork.thumbnail((round(size * .88), round(size * .88)), Image.Resampling.LANCZOS)
    canvas.alpha_composite(artwork, ((size - artwork.width) // 2, (size - artwork.height) // 2))
    return canvas
for size in (32, 180, 192, 512):
    square_icon(size).save(output / f"alme-icon-v04-{size}.png", optimize=True)
square_icon(64).save(repo / "public/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])

# A typography-and-logo composition; no synthetic project evidence.
share = Image.new("RGB", (1200, 630), "#FBF5EA")
logo = primary.resize((700, round(700 * primary.height / primary.width)), Image.Resampling.LANCZOS)
share.paste(logo, ((1200 - logo.width) // 2, 56), logo)
draw = ImageDraw.Draw(share)
font = ImageFont.truetype("C:/Windows/Fonts/bahnschrift.ttf", 46)
for y, line in ((385, "Practical solutions for spaces,"), (444, "production and land.")):
    draw.text((600, y), line, fill="#073B22", font=font, anchor="mm")
draw.rectangle((80, 551, 1120, 554), fill="#6F8F1F")
draw.rectangle((0, 606, 1200, 630), fill="#073B22")
share.save(output / "alme-social-share-v04.jpg", quality=90, optimize=True, subsampling=0)

ledger = {
    "version": "v04", "package": "https://drive.google.com/file/d/1w-791MLKZ0aKHxurG7rN3MzeUyF7tVBW/view",
    "usage_guide": "https://drive.google.com/file/d/1ZEme5MB5OD2WGUJNzmFEbBMOhCwQzcO8/view",
    "sources": records,
    "derivatives": "Header PNG resized with transparent outer canvas trimmed and clear space retained. Icon PNG/ICO derivatives preserve the supplied small-icon artwork, fitted proportionally onto cream. White SVG is byte-identical to the approved master. Share JPEG uses only approved logo pixels, brand colours and approved primary positioning.",
    "outputs": [{"path": str(p.relative_to(repo)).replace("\\", "/"), "bytes": p.stat().st_size, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(output.iterdir())] + [{"path": "public/favicon.ico", "bytes": (repo / "public/favicon.ico").stat().st_size}],
}
(repo / "docs/brand-v04-assets.json").write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"header_dimensions": header.size, "share_dimensions": share.size, "outputs": ledger["outputs"]}, indent=2))
