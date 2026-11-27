#!/usr/bin/env python3
"""Read colours, fonts, and type sizes from a visual reference.

Prints JSON. Does not decide which colour is an accent or a background.
.pptx theme colours use the standard library only. PNG/JPEG need Pillow.
PDF page colours need PyMuPDF and Pillow.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
HEX_IN_TEXT = re.compile(r"#([0-9A-Fa-f]{6})")
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
MEDIA_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}


def uppercase_hex(value: str) -> str:
    raw = value.strip().lstrip("#")
    if len(raw) != 6 or any(c not in "0123456789abcdefABCDEF" for c in raw):
        raise ValueError(value)
    return "#" + raw.upper()


def rgb_hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def size_pt(raw: str | None) -> int | float | None:
    if not raw:
        return None
    try:
        value = int(raw) / 100
    except ValueError:
        return None
    if abs(value - round(value)) < 1e-6:
        return int(round(value))
    return round(value, 2)


def aspect_label(width: float, height: float) -> str:
    if width <= 0 or height <= 0:
        return ""
    ratio = width / height
    known = (("16:9", 16 / 9), ("16:10", 1.6), ("4:3", 4 / 3), ("A4", 210 / 297))
    for label, target in known:
        if abs(ratio - target) < 0.08:
            return label
    return f"{ratio:.3f}"


def add_hex(bucket: list[dict], hex_value: str, source: str, count: int = 1, share: float | None = None) -> None:
    try:
        hex_value = uppercase_hex(hex_value)
    except ValueError:
        return
    for item in bucket:
        if item["hex"] == hex_value and item["source"] == source:
            item["count"] = int(item.get("count") or 0) + count
            if share is not None:
                item["share"] = share
            return
    row = {"hex": hex_value, "source": source, "count": count}
    if share is not None:
        row["share"] = share
    bucket.append(row)


def dominant_hexes(path: Path, max_colors: int = 8) -> list[dict]:
    from PIL import Image

    image = Image.open(path).convert("RGB")
    image.thumbnail((180, 180))
    try:
        reduced = image.quantize(colors=12, method=Image.Quantize.MEDIANCUT)
    except Exception:
        reduced = image.quantize(colors=12)
    pairs = reduced.getcolors() or []
    palette = reduced.getpalette() or []
    total = sum(count for count, _ in pairs) or 1
    blobs: list[tuple[int, tuple[int, int, int]]] = []
    for count, index in sorted(pairs, reverse=True):
        start = index * 3
        if start + 2 >= len(palette):
            continue
        rgb = (palette[start], palette[start + 1], palette[start + 2])
        placed = False
        for i, (seen_count, seen_rgb) in enumerate(blobs):
            distance = sum((a - b) ** 2 for a, b in zip(rgb, seen_rgb))
            if distance <= 26**2:
                merged = seen_count + count
                blended = tuple(round((a * seen_count + b * count) / merged) for a, b in zip(seen_rgb, rgb))
                blobs[i] = (merged, blended)
                placed = True
                break
        if not placed:
            blobs.append((count, rgb))
    blobs.sort(reverse=True)
    found: list[dict] = []
    for count, rgb in blobs[:max_colors]:
        share = count / total
        if share < 0.015:
            continue
        found.append({"hex": rgb_hex(rgb), "share": round(share, 4), "source": f"pixel:{path.name}"})
    return found


def pillow_status() -> str | None:
    try:
        import PIL  # noqa: F401
    except ImportError:
        return "Pillow is not installed. PNG/JPEG sampling needs: python3 -m pip install -r requirements.txt"
    return None


def theme_fonts(root: ET.Element) -> dict[str, dict[str, str]]:
    fonts: dict[str, dict[str, str]] = {}
    for role, node_name in (("major", "majorFont"), ("minor", "minorFont")):
        node = root.find(f".//{A}{node_name}")
        if node is None:
            continue
        found: dict[str, str] = {}
        for script in ("latin", "ea", "cs"):
            el = node.find(f"{A}{script}")
            face = (el.get("typeface") or "").strip() if el is not None else ""
            if face:
                found[script] = face
        if found:
            fonts[role] = found
    return fonts


def resolve_face(face: str, fonts: dict[str, dict[str, str]]) -> str:
    alias = {
        "+mj-lt": ("major", "latin"),
        "+mj-ea": ("major", "ea"),
        "+mj-cs": ("major", "cs"),
        "+mn-lt": ("minor", "latin"),
        "+mn-ea": ("minor", "ea"),
        "+mn-cs": ("minor", "cs"),
    }
    if face in alias:
        role, script = alias[face]
        return fonts.get(role, {}).get(script) or face
    return face


def parse_pptx(path: Path, colors: list[dict], notes: list[str]) -> dict:
    record: dict = {
        "name": path.name,
        "kind": "pptx",
        "aspect": "",
        "theme_colors": [],
        "major_font": {},
        "minor_font": {},
        "font_runs": [],
        "printed_hexes": [],
        "embedded_images": [],
    }
    run_counts: Counter[tuple[str, int | float | None, bool]] = Counter()
    explicit: Counter[str] = Counter()
    printed: set[str] = set()
    try:
        package = zipfile.ZipFile(path)
    except zipfile.BadZipFile:
        notes.append(f"{path.name} is not a readable .pptx zip.")
        record["error"] = "bad-zip"
        return record

    fonts: dict[str, dict[str, str]] = {}
    told_pillow = False
    with package:
        names = package.namelist()
        for name in names:
            if not (name.startswith("ppt/theme/theme") and name.endswith(".xml")):
                continue
            root = ET.fromstring(package.read(name))
            fonts = theme_fonts(root)
            record["major_font"] = fonts.get("major", {})
            record["minor_font"] = fonts.get("minor", {})
            scheme = root.find(f".//{A}clrScheme")
            if scheme is None:
                continue
            for child in list(scheme):
                slot = local(child.tag)
                srgb = child.find(f".//{A}srgbClr")
                sys = child.find(f".//{A}sysClr")
                raw = None
                if srgb is not None and srgb.get("val"):
                    raw = srgb.get("val")
                elif sys is not None and sys.get("lastClr"):
                    raw = sys.get("lastClr")
                if raw:
                    add_hex(record["theme_colors"], raw, f"theme:{slot}")
                    add_hex(colors, raw, f"{path.name} theme:{slot}")
        for name in names:
            if name == "ppt/presentation.xml":
                root = ET.fromstring(package.read(name))
                size = root.find(f".//{P}sldSz")
                if size is not None:
                    record["aspect"] = aspect_label(int(size.get("cx") or 0), int(size.get("cy") or 0))
            slide_xml = name.startswith(("ppt/slides/", "ppt/slideMasters/", "ppt/slideLayouts/"))
            if slide_xml and name.endswith(".xml"):
                root = ET.fromstring(package.read(name))
                for el in root.iter():
                    if local(el.tag) in {"rPr", "defRPr", "endParaRPr"}:
                        face = ""
                        latin = el.find(f"{A}latin")
                        ea = el.find(f"{A}ea")
                        chosen = latin if latin is not None and latin.get("typeface") else ea
                        if chosen is not None:
                            face = resolve_face(chosen.get("typeface") or "", fonts)
                        pt = size_pt(el.get("sz"))
                        bold = el.get("b") == "1"
                        if face or pt is not None:
                            run_counts[(face, pt, bold)] += 1
                    if local(el.tag) == "srgbClr" and el.get("val"):
                        try:
                            explicit[uppercase_hex(el.get("val") or "")] += 1
                        except ValueError:
                            pass
                    if local(el.tag) == "t" and el.text:
                        for match in HEX_IN_TEXT.findall(el.text):
                            printed.add(uppercase_hex(match))
            if name.startswith("ppt/media/") and Path(name).suffix.lower() in MEDIA_SUFFIXES:
                missing = pillow_status()
                if missing:
                    if not told_pillow:
                        notes.append(missing)
                        told_pillow = True
                else:
                    blob = Path("/tmp") / f"mood-extract-{path.stem}-{Path(name).name}"
                    blob.write_bytes(package.read(name))
                    try:
                        sampled = dominant_hexes(blob)
                    finally:
                        blob.unlink(missing_ok=True)
                    record["embedded_images"].append({"file": name, "colors": sampled})
                    for item in sampled:
                        add_hex(colors, item["hex"], f"{path.name} {name}", share=item["share"])

    for (face, pt, bold), count in run_counts.most_common(24):
        if not face and pt is None:
            continue
        record["font_runs"].append(
            {"typeface": face, "size_pt": pt, "bold": bold, "count": count}
        )
    for hex_value, count in explicit.most_common(20):
        add_hex(colors, hex_value, f"{path.name} shape-fill", count=count)
        add_hex(record.setdefault("shape_fills", []), hex_value, "shape-fill", count=count)
    record["printed_hexes"] = sorted(printed)
    for hex_value in sorted(printed):
        add_hex(colors, hex_value, f"{path.name} printed-on-slide")
    if not record["theme_colors"] and not record["font_runs"]:
        notes.append(f"{path.name} has no theme colours or font runs. Upload a PNG or PDF of the pages.")
    return record


def parse_image(path: Path, colors: list[dict], notes: list[str]) -> dict:
    record = {"name": path.name, "kind": path.suffix.lower().lstrip("."), "pixel_colors": []}
    missing = pillow_status()
    if missing:
        notes.append(missing)
        record["error"] = "pillow-missing"
        return record
    sampled = dominant_hexes(path)
    record["pixel_colors"] = sampled
    for item in sampled:
        add_hex(colors, item["hex"], f"{path.name} pixel", share=item["share"])
    if not sampled:
        notes.append(f"No colours sampled from {path.name}.")
    return record


def parse_pdf(path: Path, colors: list[dict], notes: list[str], pages: int) -> dict:
    record: dict = {"name": path.name, "kind": "pdf", "aspect": "", "fonts": [], "pages": []}
    try:
        import fitz
    except ImportError:
        notes.append("PyMuPDF is not installed. PDF sampling needs: python3 -m pip install -r requirements.txt")
        record["error"] = "pymupdf-missing"
        return record
    missing = pillow_status()
    if missing:
        notes.append(missing)
        record["error"] = "pillow-missing"
        return record
    document = fitz.open(path)
    if document.page_count == 0:
        notes.append(f"{path.name} has no pages.")
        return record
    first = document[0].rect
    record["aspect"] = aspect_label(first.width, first.height)
    seen_fonts: set[str] = set()
    limit = min(pages, document.page_count)
    for index in range(limit):
        page = document[index]
        for font in page.get_fonts():
            name = font[3] or font[4] or ""
            if name and name not in seen_fonts:
                seen_fonts.add(name)
        pixmap = page.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)
        raster = Path("/tmp") / f"mood-extract-{path.stem}-p{index + 1}.png"
        pixmap.save(raster)
        try:
            sampled = dominant_hexes(raster)
        finally:
            raster.unlink(missing_ok=True)
        record["pages"].append({"page": index + 1, "colors": sampled})
        for item in sampled:
            add_hex(colors, item["hex"], f"{path.name} page {index + 1}", share=item["share"])
    record["fonts"] = sorted(seen_fonts)
    document.close()
    return record


def build(paths: list[Path], pages: int) -> dict:
    files = []
    colors: list[dict] = []
    notes: list[str] = []
    for path in paths:
        suffix = path.suffix.lower()
        if not path.is_file():
            notes.append(f"File not found: {path}")
            continue
        if suffix == ".pptx":
            files.append(parse_pptx(path, colors, notes))
        elif suffix == ".pdf":
            files.append(parse_pdf(path, colors, notes, pages))
        elif suffix in IMAGE_SUFFIXES:
            files.append(parse_image(path, colors, notes))
        else:
            notes.append(f"{path.name} is not a .pptx, .pdf, or image. Do not guess colours from this file.")
    allowed = []
    seen = set()
    for item in colors:
        if item["hex"] in seen:
            continue
        seen.add(item["hex"])
        allowed.append(item)
    return {
        "instruction": (
            "Copy hex values from allowed_hexes. Do not invent a hex. "
            "Theme and shape-fill colours are the interface. "
            "pixel and ppt/media colours can be a photograph, not the brand accent. "
            "Colours under about 1.5 percent of a picture are omitted. If a swatch is missing, ask for a crop. "
            "Assign roles in mood-board.json, then run render_mood_board.py."
        ),
        "files": files,
        "allowed_hexes": allowed,
        "notes": notes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract visual measurements from a reference file.")
    parser.add_argument("files", nargs="+", help="pptx, pdf, png, or jpeg paths")
    parser.add_argument("--out", required=True, help="Where to write extract.json")
    parser.add_argument("--pages", type=int, default=6, help="PDF pages to sample (default 6)")
    args = parser.parse_args()
    payload = build([Path(item) for item in args.files], max(1, args.pages))
    destination = Path(args.out)
    destination.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if not payload["allowed_hexes"]:
        print("NO_COLOURS", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
