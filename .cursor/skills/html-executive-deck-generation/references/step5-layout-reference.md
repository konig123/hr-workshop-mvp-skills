# Step 5 — Layout reference (排版) + Deck Build Brief

**Input:** Steps 1–4. Step 4 has locked the **DAYMARK mood board** (color, type, logo, gold-once).

This step is **structure only**. A user may upload a deck/PDF as a layout reference. Copy how pages are *arranged*. Do **not** copy their brand.

---

## Hard split

| Take from reference (排版) | Never take from reference (mood board stays DAYMARK) |
|----------------------------|------------------------------------------------------|
| Grid: 2-col chart + drivers, 3-col modules, cover rail | Colors, palette, gradients |
| Action titles (title = the finding) | Fonts (keep Outfit / Instrument Sans / IBM Plex Mono) |
| Kickers, exhibit boxes, header bars, source footers | Logo / wordmark of the reference firm |
| Square bullets, callout boxes, chart-left / copy-right | Gold-once rule, DAYMARK logos |
| Dataviz *method*: waterfall, stacked bar, annotated bars, heatmap-as-table | Their blue/grey fills on bars and cells — remap to DAYMARK tokens |
| Density, margins, alignment, what sits in the footer | Shadows if DAYMARK forbids them |

If the reference is McKinsey-like: exhibit chrome + 排版, **not** McKinsey blue.

---

## Gate

Ask once (unless a file is already attached or user said skip / run all):

```text
Step 5 is layout reference (排版 only). DAYMARK colors and logo stay locked.

Attach a PPTX, PDF, HTML, or slide screenshots if you want this deck to follow that page architecture.
Or say "skip" to use the DAYMARK-native layout from Step 4.
```

- **File attached** → analyze, then Parts A–D.
- **Skip / none** → Part A = "no reference; use Step 4 Part B"; still do C–D.
- **Run all with no file** → do not block; same as skip.

Accepted: `.pptx` `.ppt` `.pdf` `.html` images of slides.

For PDF/PPT: render 4–8 representative pages (cover, contents, data exhibit, 2-col, close) before writing Part A.

---

## Part A — Layout reference analysis

If no file: write `Reference: none — DAYMARK-native 排版`.

If file:

### Source

- File, type, page/slide count, aspect

### Page architecture (what to copy)

| Pattern | How the reference does it | Use on our deck? |
|---------|---------------------------|------------------|
| Cover | | |
| Contents / section | | |
| Data exhibit | | |
| Closing | | |

Cover: rails, footer bars, title placement.  
Data slide: kicker → action title → boxed exhibit → source bar.  
Modules: 1 / 2 / 3 column.  
Chrome: exhibit header wash, thin border, square bullets, SOURCE + brand \| n.

### Elements (structure, not paint)

Header kicker, action title, exhibit frame, chart vs copy split, footnotes, footer.

### Dataviz methods (method only)

| In the reference | When we would use it | DAYMARK remap |
|------------------|----------------------|---------------|
| e.g. waterfall | change story | bars = horizon/ink; **one** gold series |

Do not copy their series colors.

### Do not copy

List brand-specific items (firm name, blues, serif logo, confidential marks that are not ours).

---

## Part B — Slide-by-slide 排版 (authoritative for Step 6)

Map **our** storyline onto the reference’s page types. Keep Step 4 tokens.

```
Slide N — [our title]
Reference pattern: [cover | contents | 2-col exhibit | 3-col modules | …]
Zones: [e.g. kicker / action title / exhibit 65% + drivers 35% / source bar]
Main: [CH-xx]
DAYMARK paint: bone or white field, ink type, horizon rules, gold once on [stat]
Gamma/Kimi: describe 排版 only; still DAYMARK hex
```

If no reference, paste Step 4 Part B here.

Density: 1280×720; ≤6 bar rows; heatmap ≤6×5; 3 action modules.

---

## Part C — HTML interactions

| Feature | Trigger | Print fallback |
|---------|---------|----------------|
| Slide nav | buttons, arrows, space | hide `.nav` |
| Progress bar | slide change | hide in print |
| KPI values | visible in HTML (not `0`) | static |
| Bar fill | `.slide.active` | `width: var(--w) !important` |

| Slide | ON/OFF | Element | Notes |
|-------|--------|---------|-------|
| | | | |

---

## Part D — Deck Build Brief (required for Step 6)

```markdown
## DECK BUILD BRIEF

**Title:**
**Topic slug:**
**Audience:**
**Period:**
**Language:**
**Input type:** file | text | mixed
**Slides:** [N]

### Mood board (locked)
DAYMARK — [daymark-visual-guide.md](daymark-visual-guide.md)
Do not replace tokens with the layout reference.

### Layout reference
[none | filename + 3-line 排版 summary]

### Slide map
[Step 3 table]

### Headline (slide 2 / paradox)
[exact text]

### Closing actions
[Step 3 D]

### Chart data JSON
[Step 2 D]

### 排版 per slide
[Step 5 Part B]

### HTML interactions
[Step 5 Part C]

### Output paths
- {topic}_deck.html
- {topic}_gamma_prompt.md
- {topic}_kimi_prompt.md
```

End with: **LAYOUT REFERENCE COMPLETE — ready for Step 6 (generate HTML + Gamma + Kimi)**

Ask to confirm before Step 6.
