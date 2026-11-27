---
name: mood-board-extract
description: >-
  Extract a mood board from a student reference (PPT template, brand PDF,
  screenshots, or an existing deck): font and point size, image style,
  colour hex, and infographic marks. Use when the user uploads a visual
  reference, asks for a mood board, 色盤, 字級, or hex colours before slides.
  Measurements come from scripts. Do not invent navy, teal, or gold, and
  do not make slides.
---

# Mood board extract

Extract one mood board from the file the student uploaded. Scripts read the numbers. You name the roles, the image style, and the do / don't list.

You do not write PowerPoint. You do not build a slide deck. You do not copy another firm's logo or palette (including DAYMARK) onto their file.

## Scripts

Run them on the student's files. Write `extract.json`, `mood-board.json`, and `mood-board.md` in the student workspace, not into this skill folder.

`.pptx` theme colours, fonts, and point sizes need only Python. PNG, JPEG, and PDF colours need the packages in `requirements.txt` (Pillow, PyMuPDF). Install only if a script says the import failed:

```bash
python3 -m pip install -r requirements.txt
```

`requirements.txt` sits next to this file. Run the scripts by their path in this skill:

```bash
python3 "<this-skill>/scripts/extract_visuals.py" "REFERENCE.pptx" "PAGE.png" --out extract.json
python3 "<this-skill>/scripts/render_mood_board.py" mood-board.json --against extract.json --md mood-board.md
```

Add `--lock` on the render command only after the student says 確認 / lock / 可以下一步.

Show the student the markdown the script wrote. Do not retype the tables.

## Hard rules

1. First reply asks only: 中文（繁體） or English. After they choose, speak only in that language. Table labels stay English.
2. If nothing is uploaded, ask for the reference. Prefer a `.pptx`, a PDF, or 3–6 images (cover, section, content, chart, footer). Do not guess a palette from a filename.
3. Every hex in the board is copied from `extract.json` `allowed_hexes`, or from `student_overrides` after the student corrects a cell. A colour name without `#RRGGBB` is not a colour.
4. Theme slots and shape fills are the interface colours. `pixel:` and `ppt/media` colours may be a photograph. Do not promote a skin tone or a product photo to Accent when a theme slot already has the brand colour.
5. Font family and point size use `from-file` only when that pair is in `extract.json`. If the name is in the file and the size is not, use `est`. If the letters are unreadable, use `check-slide-master` and a category ("geometric sans"), not a guessed family.
6. Do not ask the student to confirm until `render_mood_board.py` prints `OK`.
7. This is paint, not story. Do not rewrite their SCQA or add slide titles.

## Phase 0 — Language

Ask, then wait:

「接下來我們從你上傳的參考檔抽出 mood board（字型＋字級、圖片風格、色盤 hex、資訊圖元素）。你想用哪一種語言寫這份板？
1) 中文（繁體）
2) English」

## Phase 1 — Reference

Ask what the file is, in one line: 公司投影片模板 / 品牌規範 / 去年簡報 / 其他.

Run `extract_visuals.py`. If it exits with `NO_COLOURS`, or the notes say the `.pptx` had no theme, say you cannot see colours and ask for PNG or PDF pages. Do not publish a board. Pixel sampling keeps colours that cover about 1.5% or more of the picture. If a small swatch is missing, ask for a crop of that swatch.

## Phase 2 — Board

Read `extract.json`. Fill `mood-board.json` in the shape below. Judgment fields (roles, image style, chrome, do / don't, style sentence) are yours. Hex digits, typeface names, and `from-file` sizes are the file's.

```json
{
  "language": "zh-Hant",
  "source_files": ["Brand.pptx"],
  "file_kind": "template",
  "aspect": "16:9",
  "one_line_style": "",
  "fonts": [
    {"role": "title", "family": "", "weight": "", "size_pt": null, "size_note": "from-file"},
    {"role": "subhead", "family": "", "weight": "", "size_pt": null, "size_note": "from-file"},
    {"role": "body", "family": "", "weight": "", "size_pt": null, "size_note": "from-file"}
  ],
  "image_style": {"use": "", "lighting": "", "crop": "", "texture": ""},
  "palette": [
    {"role": "background_dark", "hex": null, "name": "", "sampled_from": "not in file"},
    {"role": "background_light", "hex": null, "name": "", "sampled_from": ""},
    {"role": "text_on_light", "hex": null, "name": "", "sampled_from": ""},
    {"role": "text_on_dark", "hex": null, "name": "", "sampled_from": ""},
    {"role": "accent_1", "hex": null, "name": "", "sampled_from": ""},
    {"role": "accent_2", "hex": null, "name": "", "sampled_from": "not in file"},
    {"role": "chart_1", "hex": null, "name": "", "sampled_from": "not in file"},
    {"role": "chart_2", "hex": null, "name": "", "sampled_from": "not in file"}
  ],
  "infographic": {"line": "", "shape": "", "icon": "", "chart_mark": "", "number_lockup": "", "other": ""},
  "chrome": "",
  "do": ["", "", ""],
  "dont": ["", "", ""],
  "style_sentence": "",
  "student_overrides": []
}
```

`file_kind` is one of: template, brand guide, existing deck, mood-board practice, mixed.

`language` is `zh-Hant` or `en`.

Hex values are `#` plus 6 uppercase digits, or `null` when that row is not in the file. At least one background, one text colour, and `accent_1` must be real hex values. `accent_2` and chart rows may stay null.

`style_sentence` is one paragraph for Gamma / Kimi. It must include each family, each size as `40pt` (no space), every locked hex, the image style, the line and shape, and the words `one hero per page`.

`do` and `dont` are 3 to 5 items each, taken from the file.

Run render. If it prints `FAIL`, fix `mood-board.json` and run it again. Do not hand-edit `mood-board.md`.

Then show that markdown and stop:

- 中文：請核對 hex 與字級；不對就改那一格。確認後回「確認」。
- English: Check the hex values and the type sizes. Name the cell to change, or reply lock.

## Phase 3 — Lock

Apply their correction in `mood-board.json`. A hex they measured themselves goes in `student_overrides` as `{"hex": "#AABBCC", "note": "footer swatch, student confirmed"}`. The note says where they read it.

Run render again. After they say 確認 / lock / 可以下一步, run the same command with `--lock`.

Tell them the next step is page layout, and do not generate slides in this step.

Only if they ask for a picture: describe a still-life board (swatches, type specimen, chart crop, footer crop) using the locked tokens. Do not generate a deck.

## Anti-patterns

- A hex that is not in `extract.json` and not in `student_overrides`
- Treating a photo colour as the accent while a theme slot exists
- A font family that the file does not name
- Confirming a board while render still prints `FAIL`
- Retyping the markdown tables
- Adding a second brand on top of their reference
- Generating slides in this step
