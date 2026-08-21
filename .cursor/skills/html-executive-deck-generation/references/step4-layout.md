# Step 4 � DAYMARK mood board (visual system)

Lock **paint**: color, type, logo, gold-once. Do **not** ingest another firm�s palette here.

**?? / exhibit structure** waits for Step 5 (optional layout PDF). Part B is the **fallback** layout if Step 5 has no reference.

## Prerequisite

**Default is DAYMARK.** Read [daymark-visual-guide.md](daymark-visual-guide.md) and fill Part A from it.

Do not swap these tokens because the user attached a McKinsey PDF or other deck � that file belongs in **Step 5**.

Only replace DAYMARK if the user explicitly says **replace DAYMARK** or **use HR fallback**.

---

## Part A � Template Profile (mood board)

### Template source

- File: bundled DAYMARK visual guide (`assets/daymark-visual-guide/`)
- Type: brand guide + mood board
- Slide aspect: 16:9

### Visual tokens

| Token | Value |
|-------|-------|
| Primary | #0A335E Deep Navy |
| Ink | #153D66 |
| Background | #FBF8F3 Bone |
| Accent rule | #35827E (#42A9A4 on navy) |
| Accent once | #EFB230 Beacon Gold |
| Heading | Outfit |
| Body | Instrument Sans |
| Captions | IBM Plex Mono |
| Density | low�medium |

### HTML strategy

- **DAYMARK (default):** tokens + logos from `assets/daymark-visual-guide/`; engine from layout-contract
- **Replace DAYMARK** (explicit only): user HTML / HR fallback
- **Layout PDF/PPTX:** ignore for color here � analyze in Step 5

---

## Part B � Fallback ?? (only if Step 5 has no reference)

Native DAYMARK zones, not a McKinsey clone. Step 5 may replace these.

```
Slide N � [Title]
Pattern: A cover | B KPI | C chart | D scope | E close
Zones: header | main | footer
Main: [chart ID]
Gold once: [which stat or none]
Gamma/Kimi: DAYMARK hex; Daymark-native layout
```

### Density (1280�720)

Limits: 6 bar rows; heatmap 6�5; 3 action modules.

End with: **MOOD BOARD LOCKED � ready for Step 5 (optional layout reference)**
