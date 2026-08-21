# DAYMARK visual guide (default)

**Default brand for this skill.** Apply unless the user attaches a different template.

Read this at Step 4. Open `assets/daymark-visual-guide/moodboard.png` if you need the specimen. Copy logos from the same folder into the HTML deck when building.

## Tokens (sampled from lockups)

| Name | Hex | Role |
|------|-----|------|
| Deep Navy | `#0A335E` | Title slides, full-bleed fields |
| Ink Navy | `#153D66` | Body type, icon pillar on cream |
| Horizon Teal | `#35827E` | Rules; underline the turn of a headline |
| Horizon Bright | `#42A9A4` | Same rule on navy fields |
| Beacon Gold | `#EFB230` | **One** sun or one KPI per slide |
| Bone | `#FBF8F3` | Content slide background |
| Ivory | `#F9F5EC` | Type / wordmark on navy |

```css
:root {
  --deep: #0A335E;
  --ink: #153D66;
  --horizon: #35827E;
  --horizon-bright: #42A9A4;
  --beacon: #EFB230;
  --bone: #FBF8F3;
  --ivory: #F9F5EC;
  --slide-w: 1280px;
  --slide-h: 720px;
}
```

## Type

- **Titles:** Outfit SemiBold–Bold. Wordmarks: all-caps, tracking ~0.28–0.34em. Sentence titles: tracking −0.02em.
- **Body:** Instrument Sans Regular / Medium.
- **Captions, sources, axes:** IBM Plex Mono, small.
- Underline only the **turn** of a headline (the MARK half), in Horizon Teal — never a full-title underline.

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Instrument+Sans:wght@400;500;600&family=Outfit:wght@400;500;600;700&display=swap" rel="stylesheet" />
```

## Shape grammar

- Rounded-crown vertical pillar, short teal horizon bar, gold circle **once**.
- No shadows, no gradients, no extra hues, no emoji (SVG only).
- Title = Deep Navy + ivory type + one gold sun.
- Content = Bone + teal hairline.
- Gold = lighthouse: one number or one sun per frame.

## Slide archetypes

| Pattern | Letter | Look |
|---------|--------|------|
| Title | A | Navy field, ivory wordmark (`logo-reversed.png` or CSS lockup), gold sun top-right |
| Insight | D | Bone field, navy headline, teal underline on the turn |
| KPI row | B | One gold hero number **or** three ink KPIs; teal rule; never three gold numbers |
| Chart + callout | C | Navy or bone panel; callout uses ink + one gold stat |
| Actions / close | E | Three cards; teal hairlines; gold unused unless a single next-step mark |

## Logos

| File | Use |
|------|-----|
| `assets/daymark-visual-guide/logo-reversed.png` | Title / navy slides |
| `assets/daymark-visual-guide/logo-primary.png` | Bone slides, footer lockup |
| `assets/daymark-visual-guide/logo-mark.png` | Favicon, small corner mark |
| `assets/daymark-visual-guide/moodboard.png` | Visual specimen — do not paste into slides |

## Gamma / Kimi style block (paste when Daymark is active)

```
Primary: #0A335E (title fields)
Ink: #153D66 (type)
Background: #FBF8F3 (content)
Accent rule: #35827E (underline the turn of a headline)
Accent once: #EFB230 (one KPI or one sun per slide)
On navy, teal lifts to #42A9A4
Fonts: Outfit titles, Instrument Sans body, IBM Plex Mono captions
Keywords: navigational, daylight mark, executive brief, no shadows, no gradients
Gold is a lighthouse — never more than one gold number on a slide
```

## Template Profile (pre-fill when using this guide)

- Source: bundled DAYMARK visual guide
- Type: brand guide + mood board
- Aspect: 16:9
- Density: low–medium
- Icon style: geometric (pillar / horizon / sun), flat, no emoji
