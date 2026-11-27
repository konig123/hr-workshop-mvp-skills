#!/usr/bin/env python3
"""Turn mood-board.json into the mood board markdown.

Fails if a hex was not measured, or if the style sentence drops a measured hex.
Writes the markdown only after the checks pass.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HEX = r"^#[0-9A-F]{6}$"
FONT_ROLES = ("title", "subhead", "body")
PALETTE = (
    ("background_dark", "Background (cover / dark)", "BG-DARK"),
    ("background_light", "Background (inner / light)", "BG-LIGHT"),
    ("text_on_light", "Text (on light)", "TEXT-ON-LIGHT"),
    ("text_on_dark", "Text (on dark)", "TEXT-ON-DARK"),
    ("accent_1", "Accent 1", "ACCENT"),
    ("accent_2", "Accent 2", "ACCENT-2"),
    ("chart_1", "Chart / series 1", "CHART-1"),
    ("chart_2", "Chart / series 2", "CHART-2"),
)
FILE_KINDS = {"template", "brand guide", "existing deck", "mood-board practice", "mixed"}
SIZE_NOTES = {"from-file", "est", "check-slide-master"}
IMAGE_KEYS = ("use", "lighting", "crop", "texture")
CLOSE = {
    "zh-Hant": "這是草稿 mood board。請核對 hex 與字級；不對就改那一格。確認後回我「確認」。",
    "en": "This is a draft mood board. Check the hex values and the type sizes. Name the cell to change, or reply lock.",
}
LOCK_LINE = {
    "zh-Hant": "MOOD BOARD LOCKED. 下一步才是逐頁版式，不要在這一步生成投影片。",
    "en": "MOOD BOARD LOCKED. Next is page layout. Do not generate slides at this step.",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def is_hex(value: object) -> bool:
    return isinstance(value, str) and len(value) == 7 and value[0] == "#" and all(
        c in "0123456789ABCDEF" for c in value[1:]
    )


def fmt_size(size: object, note: str) -> str:
    if isinstance(size, float) and size.is_integer():
        size = int(size)
    text = f"{size:g}pt" if isinstance(size, (int, float)) else ""
    if note == "est":
        text = f"{text} [est. pt]".strip()
    elif note == "check-slide-master":
        text = f"{text} [check Slide Master]".strip()
    return text


def allowed_hexes(extract: dict) -> set[str]:
    found = set()
    for item in extract.get("allowed_hexes") or []:
        hex_value = item.get("hex")
        if is_hex(hex_value):
            found.add(hex_value)
    return found


def face_known(family: str, names: set[str]) -> bool:
    key = family.casefold().strip()
    if len(key) < 4:
        return False
    for name in names:
        if len(name) < 4:
            continue
        if key == name or key in name or name in key:
            return True
    return False


def font_facts(extract: dict) -> tuple[set[str], set[tuple[str, float]]]:
    names: set[str] = set()
    sizes: set[tuple[str, float]] = set()
    for file_row in extract.get("files") or []:
        for role in ("major_font", "minor_font"):
            for face in (file_row.get(role) or {}).values():
                if isinstance(face, str) and face.strip():
                    names.add(face.casefold())
        for font in file_row.get("fonts") or []:
            if isinstance(font, str) and font.strip():
                names.add(font.casefold())
        for run in file_row.get("font_runs") or []:
            face = (run.get("typeface") or "").strip()
            if face:
                names.add(face.casefold())
            if face and isinstance(run.get("size_pt"), (int, float)):
                sizes.add((face.casefold(), float(run["size_pt"])))
    return names, sizes


def require(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def palette_by_role(board: dict) -> dict[str, dict]:
    rows = {}
    for row in board.get("palette") or []:
        if isinstance(row, dict) and row.get("role"):
            rows[row["role"]] = row
    return rows


def active_hexes(rows: dict[str, dict]) -> list[tuple[str, str, str]]:
    active = []
    for role, _label, short in PALETTE:
        row = rows.get(role) or {}
        hex_value = row.get("hex")
        if hex_value in (None, "", "—", "-"):
            continue
        active.append((role, short, hex_value))
    return active


def check(board: dict, extract: dict) -> list[str]:
    errors: list[str] = []
    language = board.get("language")
    require(errors, language in CLOSE, "language must be zh-Hant or en.")
    require(errors, bool(board.get("source_files")), "source_files is empty.")
    require(errors, board.get("file_kind") in FILE_KINDS, "file_kind must be template, brand guide, existing deck, mood-board practice, or mixed.")
    require(errors, bool(str(board.get("aspect") or "").strip()), "aspect is empty.")
    require(errors, bool(str(board.get("one_line_style") or "").strip()), "one_line_style is empty.")
    require(errors, bool(str(board.get("chrome") or "").strip()), "chrome is empty.")

    fonts = {row.get("role"): row for row in board.get("fonts") or [] if isinstance(row, dict)}
    known_names, known_sizes = font_facts(extract)
    for role in FONT_ROLES:
        row = fonts.get(role) or {}
        family = str(row.get("family") or "").strip()
        note = row.get("size_note")
        size = row.get("size_pt")
        require(errors, bool(family), f"fonts.{role}.family is empty.")
        require(errors, note in SIZE_NOTES, f"fonts.{role}.size_note must be from-file, est, or check-slide-master.")
        require(errors, isinstance(size, (int, float)) and float(size) > 0, f"fonts.{role}.size_pt must be a number in pt.")
        require(errors, bool(str(row.get("weight") or "").strip()), f"fonts.{role}.weight is empty.")
        if note in {"from-file", "est"} and family:
            require(
                errors,
                face_known(family, known_names),
                f"fonts.{role}.family {family!r} was not in the file. Use check-slide-master and a category, or copy the typeface from extract.json.",
            )
        if note == "from-file" and isinstance(size, (int, float)) and family:
            matched = any(abs(float(size) - seen) < 0.2 and face_known(family, {face}) for face, seen in known_sizes)
            require(
                errors,
                matched,
                f"fonts.{role} {family} {size}pt was not stored on a run. Use size_note est or check-slide-master.",
            )

    rows = palette_by_role(board)
    unknown_roles = sorted(set(rows) - {role for role, _label, _short in PALETTE})
    require(errors, not unknown_roles, f"Unknown palette roles: {', '.join(unknown_roles)}.")
    for role, _label, _short in PALETTE:
        if role not in rows:
            errors.append(f"palette is missing role {role}. Use hex null when that row is not in the file.")
            continue
        hex_value = rows[role].get("hex")
        if hex_value in (None, "", "—", "-"):
            continue
        require(errors, is_hex(hex_value), f"palette.{role} hex must be #RRGGBB uppercase, not {hex_value!r}.")
        require(errors, bool(str(rows[role].get("sampled_from") or "").strip()), f"palette.{role} needs sampled_from.")

    active = active_hexes(rows)
    require(errors, any(role == "accent_1" for role, _short, _hex in active), "accent_1 needs a hex from the file.")
    require(
        errors,
        any(role.startswith("background_") for role, _short, _hex in active),
        "At least one background row needs a hex.",
    )
    require(
        errors,
        any(role.startswith("text_") for role, _short, _hex in active),
        "At least one text row needs a hex.",
    )

    measured = allowed_hexes(extract)
    overrides = []
    for item in board.get("student_overrides") or []:
        if not isinstance(item, dict):
            errors.append("student_overrides entries must be objects with hex and note.")
            continue
        require(errors, is_hex(item.get("hex")), f"student override hex is invalid: {item.get('hex')!r}.")
        note = str(item.get("note") or "").strip()
        require(errors, len(note) >= 8, "Each student override needs a note of at least 8 characters saying where the student read it.")
        if is_hex(item.get("hex")):
            overrides.append(item["hex"])
    allowed = measured | set(overrides)
    for role, _short, hex_value in active:
        if is_hex(hex_value):
            require(
                errors,
                hex_value in allowed,
                f"palette.{role} {hex_value} is not in extract.json. Copy a measured hex, or record a student_overrides note after the student corrects it.",
            )

    image = board.get("image_style") or {}
    for key in IMAGE_KEYS:
        require(errors, bool(str(image.get(key) or "").strip()), f"image_style.{key} is empty.")
    info = board.get("infographic") or {}
    require(errors, bool(str(info.get("line") or "").strip()), "infographic.line is empty.")
    require(errors, bool(str(info.get("shape") or "").strip()), "infographic.shape is empty.")

    do_items = [str(item).strip() for item in board.get("do") or [] if str(item).strip()]
    dont_items = [str(item).strip() for item in board.get("dont") or [] if str(item).strip()]
    require(errors, 3 <= len(do_items) <= 5, "do must contain 3 to 5 items taken from the file.")
    require(errors, 3 <= len(dont_items) <= 5, "dont must contain 3 to 5 items taken from the file.")

    sentence = str(board.get("style_sentence") or "")
    require(errors, "one hero per page" in sentence.casefold(), 'style_sentence must include "one hero per page".')
    for role in FONT_ROLES:
        row = fonts.get(role) or {}
        family = str(row.get("family") or "").strip()
        if family:
            require(errors, family.casefold() in sentence.casefold(), f"style_sentence is missing the {role} family {family}.")
        size = row.get("size_pt")
        if isinstance(size, (int, float)):
            token = f"{int(size) if float(size).is_integer() else size:g}pt"
            compact = re.sub(r"\s+", "", sentence)
            require(
                errors,
                re.search(rf"(?<!\d){re.escape(token)}", compact, re.I) is not None,
                f"style_sentence is missing {token}.",
            )
    for _role, _short, hex_value in active:
        if is_hex(hex_value):
            require(errors, hex_value.casefold() in sentence.casefold(), f"style_sentence is missing {hex_value}.")
    return errors


def palette_line(active: list[tuple[str, str, str]]) -> str:
    return " · ".join(f"{short} {hex_value}" for _role, short, hex_value in active)


def render_markdown(board: dict, line: str, locked: bool) -> str:
    language = board.get("language") or "en"
    rows = palette_by_role(board)
    fonts = {row.get("role"): row for row in board.get("fonts") or []}
    image = board.get("image_style") or {}
    info = board.get("infographic") or {}
    font_lines = [
        "| Role | Family | Weight | Size |",
        "| --- | --- | --- | --- |",
    ]
    labels = {"title": "Title / heading", "subhead": "Subhead", "body": "Body / caption"}
    for role in FONT_ROLES:
        row = fonts.get(role) or {}
        font_lines.append(
            f"| {labels[role]} | {row.get('family','')} | {row.get('weight','')} | {fmt_size(row.get('size_pt'), row.get('size_note') or '')} |"
        )
    color_lines = [
        "| Role | Hex | Optional name | Sampled from |",
        "| --- | --- | --- | --- |",
    ]
    for role, label, _short in PALETTE:
        row = rows.get(role) or {}
        hex_value = row.get("hex")
        if hex_value in (None, "", "—", "-"):
            shown = "—"
        else:
            shown = hex_value
        color_lines.append(
            f"| {label} | {shown} | {row.get('name') or ''} | {row.get('sampled_from') or ''} |"
        )
    info_labels = (
        ("line", "Line"),
        ("shape", "Shape"),
        ("icon", "Icon"),
        ("chart_mark", "Chart mark"),
        ("number_lockup", "Number lockup"),
        ("other", "Other"),
    )
    info_lines = ["| Kind | Spec |", "| --- | --- |"]
    for key, label in info_labels:
        spec = str(info.get(key) or "").strip() or "—"
        info_lines.append(f"| {label} | {spec} |")
    do_lines = "\n".join(f"- {item}" for item in board.get("do") or [])
    dont_lines = "\n".join(f"- {item}" for item in board.get("dont") or [])
    sources = ", ".join(board.get("source_files") or [])
    ending = LOCK_LINE[language] if locked else CLOSE[language]
    parts = [
        "# MOOD BOARD",
        f"Source file: {sources}",
        f"File type: {board.get('file_kind')}",
        f"Aspect: {board.get('aspect')}",
        f"One-line style: {board.get('one_line_style')}",
        "",
        "## 1. Font",
        *font_lines,
        "",
        "## 2. Image style",
        f"- Use: {image.get('use')}",
        f"- Lighting / grade: {image.get('lighting')}",
        f"- Crop: {image.get('crop')}",
        f"- Texture: {image.get('texture')}",
        "",
        "## 3. Color palette",
        *color_lines,
        "",
        "Palette line (copy-paste, hex only):",
        f"`{line}`",
        "",
        "## 4. Infographic element",
        *info_lines,
        "",
        "## 5. Chrome",
        str(board.get("chrome") or "").strip(),
        "",
        "## 6. Do / Don't",
        "Do:",
        do_lines,
        "",
        "Don't:",
        dont_lines,
        "",
        "## 7. Paste-ready style sentence",
        str(board.get("style_sentence") or "").strip(),
        "",
        ending,
        "",
    ]
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate mood-board.json and write the markdown board.")
    parser.add_argument("board", help="Path to mood-board.json")
    parser.add_argument("--against", required=True, help="Path to extract.json")
    parser.add_argument("--md", required=True, help="Where to write the markdown")
    parser.add_argument("--lock", action="store_true", help="Mark the board locked after it passes")
    args = parser.parse_args()
    board_path = Path(args.board)
    board = load_json(board_path)
    extract = load_json(Path(args.against))
    errors = check(board, extract)
    if errors:
        print("FAIL")
        for message in errors:
            print(f"- {message}")
        return 1
    rows = palette_by_role(board)
    line = palette_line(active_hexes(rows))
    markdown = render_markdown(board, line, args.lock)
    Path(args.md).write_text(markdown, encoding="utf-8")
    if args.lock:
        board["locked"] = True
        board["palette_line"] = line
        board_path.write_text(json.dumps(board, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("OK")
    print(Path(args.md).resolve())
    return 0


if __name__ == "__main__":
    sys.exit(main())
