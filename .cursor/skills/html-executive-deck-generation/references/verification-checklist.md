# Step 4 � Verification Checklist

Run before marking an HTML executive deck complete.

## A. Static file checks (grep / read)

| Check | Pass criteria |
|-------|---------------|
| Charset | `<meta charset="UTF-8" />` present |
| No emoji | No Unicode emoji in HTML (use SVG / entities) |
| No corruption | No standalone `?` or `??` in visible UI strings |
| Title tag | Single clean title, no duplicated words |
| Slide count | Matches storyline (8�10 typical) |
| Canvas vars | `--slide-w: 1280px; --slide-h: 720px` |
| Bottom padding | Slides use `72px` bottom padding (or equivalent safe zone) |

Quick grep patterns to fail on:

```
[\x{1F300}-\x{1F9FF}]   # emoji range (if supported)
>?\?<|?? 
```

## B. Layout checks (manual or browser)

Open file in browser at **1280�720** (resize window or devtools device).

| Slide | What to verify |
|-------|----------------|
| 1 Title | Navy field, ivory type, one gold sun; logo not clipped |
| 2 KPI | Numbers visible immediately (not all `0`); at most one gold hero number |
| 4 Gap chart | Vertical benchmark visible; mid-tier bars readable on light fill |
| 6 Heatmap | All cells visible; no row clipped at bottom |
| 8 Dot plot | Column headers aligned; dots on tracks |
| 9 Actions | Timeline banner above nav; slide-num not overlapping text |
| Nav | Prev/next centered; does not cover slide footer |

## C. Interaction checks

- [ ] Arrow keys and buttons change slides
- [ ] Progress bar advances
- [ ] Gap/risk bars animate on slide enter
- [ ] Heatmap tooltips work (if implemented)
- [ ] Returning to slide 2 re-triggers KPI count-up (optional)

## D. Print checks

Print preview (Cmd/Ctrl+P):

- [ ] One slide per page
- [ ] Nav and progress bar hidden
- [ ] Bar fills at full width
- [ ] Dot positions correct
- [ ] Callouts and heatmap cells visible (opacity 1)

## E. Optional automated screenshots

If Playwright or similar is available:

```javascript
// Capture dense slides at 1280x720
const slides = [2, 4, 6, 8, 9];
// Navigate to each, screenshot, check document.scrollWidth === 1280
```

Save to `{deck_folder}/verify-screenshots/` for regression comparison.

Reference example: `HRBP/pulse_survey_eng/verify-screenshots/`

## F. Data accuracy spot-check

- [ ] KPI numbers match Python `metrics.json` (`kpiValues`) — not LLM mental math
- [ ] Bar / heatmap / ranking values match JSON `charts[].rows` or `rankings`
- [ ] Bar widths match formula `(score/5)*100%` when the JSON score is 1–5
- [ ] At-risk percentages match defined threshold **and** JSON
- [ ] Insight callout stats match `metrics.json`
- [ ] No placeholder lorem or `[TBD]` in executive deck

## G. Sign-off template

```markdown
## Deck verification � {filename}

- Date:
- Viewport: 1280�720
- Slides: {n}
- Static checks: PASS / FAIL
- Layout checks: PASS / FAIL
- Print: PASS / FAIL
- Data spot-check: PASS / FAIL
- Notes: {any known minor issues}
```

Only report **complete** when all sections PASS or user accepts documented exceptions.
