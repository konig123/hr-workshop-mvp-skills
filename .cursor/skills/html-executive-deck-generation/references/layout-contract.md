# HTML Executive Deck � Layout Contract

Slide **engine** (viewport, nav, charts, print) lives here.  
Default **visual tokens** live in [daymark-visual-guide.md](daymark-visual-guide.md) � use those unless the user chose another template.

The green / cream / coral `:root` below is **legacy** for the HRBP HTML clone only.

## Slide engine

```css
:root {
  --green: #1e4d3b;
  --green-dark: #0e4d41;
  --cream: #fce6d5;
  --cream-light: #f8e1c6;
  --coral: #f08c7d;
  --coral-light: #f1a69a;
  --white: #ffffff;
  --text-dark: #1e4d3b;
  --text-muted: #5a6b64;
  --warn: #c0392b;
  --slide-w: 1280px;
  --slide-h: 720px;
}
```

### Viewport behavior

- `body { overflow: hidden; }` during presentation
- `.deck` centers slides in viewport
- `.slide` uses `width: min(96vw, var(--slide-w)); height: min(90vh, var(--slide-h));`
- Only one `.slide.active` visible; others `opacity: 0; pointer-events: none`

### Padding budget

| Zone | Value | Purpose |
|------|-------|---------|
| Slide default | `48px 56px 72px` | Top/sides + room for nav |
| Title slide right column | `60px 56px 60px 20px` | Asymmetric title layout |
| Green panel (default) | `28px 36px` | Chart container |
| Green panel (heatmap slide) | `20px 28px` | Tighter for 5�4 grid |
| Slide-num | `bottom: 48px; right: 56px` | Above nav safe zone |

Per-slide overrides via `[data-slide="N"]` selectors when content is dense (e.g. slide 6 heatmap, slide 9 actions).

---

## Typography

**DAYMARK (default):** Outfit titles, Instrument Sans body, IBM Plex Mono captions � see visual guide.

**Legacy HR clone only:**

| Element | Font | Size guidance |
|---------|------|---------------|
| h1, h2, h3, KPI values | Playfair Display | h2: `clamp(1.6rem, 3vw, 2.4rem)` |
| Body, labels, nav | Inter | 12�15px for supporting text |
| Headline hook | Playfair italic accent | `.headline-text em { color: var(--coral); }` |

Load fonts (legacy HR clone):

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:ital,wght@0,600;0,700;1,600&display=swap" rel="stylesheet" />
```

---

## Icons and symbols

### Icon box (template C/E header)

```html
<div class="icon-box" aria-hidden="true">
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none"
       stroke="#fff" stroke-width="2" stroke-linecap="round">
    <!-- path only, no emoji -->
  </svg>
</div>
```

### Navigation arrows

```html
<button aria-label="Previous slide">&larr;</button>
<button aria-label="Next slide">&rarr;</button>
```

### Timeline banner arrow

```html
<span class="arrow">&rarr;</span>
```

**Never** paste emoji or special Unicode symbols from chat clients into HTML source.

---

## Chart geometry

### Gap / score bars

- Track: `height: 26px; border-radius: 13px; background: rgba(255,255,255,.12)`
- Fill width: `style="--w:84.8%"` where `% = (score / maxScale) * 100`
- Benchmark at score 3.0 on 1�5 scale: `left: 60%` pseudo-element on `.gap-track`
- Animation: fill starts `width: 0`; on `.slide.active`, `width: var(--w)`
- Print: `.gap-fill { width: var(--w) !important; }`

### Risk percentage bars

- Same pattern with `.risk-fill` and `--w` as percentage (0�100)

### Heatmap

```css
.heatmap {
  display: grid;
  grid-template-columns: 120px repeat(N, 1fr);
  gap: 6px;
}
.heatmap .cell {
  height: 44px;  /* fixed � do not use aspect-ratio alone */
  border-radius: 10px;
}
.heatmap .row-head { min-height: 44px; }
```

- Include `.corner` + `.col-head` cells before data rows
- Wrap in `.heatmap-wrap { overflow-x: auto; }` for narrow viewports only
- Level colors: `high` #2d6b52, `mid` cream-light, `low` coral

### Dot plot

- Header row required: empty label + column names (`Leadership`, `Team Eff.`)
- Position: `--pos: ((score - 1) / 4 * 100)%` mapped to `left: var(--pos)` on dot
- Two dot colors: `.lead` (cream-light), `.team` (coral)
- Legend below chart

### KPI panel

- 3 columns in green pill: `border-radius: 48px; padding: 32px 44px`
- Values visible on load: `<div class="kpi-value" data-count="3.73">3.73</div>`
- Count-up runs only when user navigates to KPI slide (not on initial paint for slide 2 if already active � template sets static defaults)

---

## JavaScript requirements

Minimum slide engine:

- `goTo(n)` with `.active` / `.prev` classes
- Keyboard: ArrowLeft, ArrowRight, Space
- Progress bar width = `(current+1)/total * 100%`
- `buildHeatmap()` / `buildDotplot()` from `DATA` object if charts are dynamic
- `window.matchMedia("print").matches` guard on animations
- Tooltip optional for heatmap hover

Keep `DATA` object at bottom of script for easy number updates without touching markup.

---

## Print mode

```css
@media print {
  .nav, .progress-bar, .tooltip { display: none !important; }
  .slide {
    position: relative;
    opacity: 1 !important;
    page-break-after: always;
    min-height: 100vh;
    padding-bottom: 48px;
  }
  .gap-fill, .risk-fill, .resource-fill { width: var(--w) !important; }
  .slide.active .dotplot-dot { left: var(--pos) !important; }
  .insight-callout, .action-card, .heatmap .cell {
    opacity: 1 !important;
    transform: none !important;
  }
}
```

---

## Mobile fallback (secondary)

Presentation target is **1280�720 desktop**. Mobile `@media (max-width: 900px)` may stack grids � do not optimize mobile at the expense of desktop slide fit.

---

## Content density limits

| Slide type | Max rows / items |
|------------|------------------|
| Gap chart | 4�6 dimension rows |
| Risk bars | 4�6 items |
| Heatmap | ?6 departments � ?5 columns |
| Dot plot | ?8 managers |
| Action cards | 3 cards + 1 timeline banner |

If data exceeds limits, split across slides or move detail to appendix slide.
