# Step 2 — Chart Plan

Map Step 1 insights to visuals for **HTML, Gamma, and Kimi**.

**Input:** Insight Brief from Step 1.

## Chart catalog

### HTML-native (when building `.html`)

| Chart type | Best for | HTML class |
|------------|----------|------------|
| KPI cards (3) | Headline metrics | `.kpi-panel` |
| Gap bars | Compare dimensions | `.gap-chart` / `.gap-fill` |
| Risk % bars | % at-risk | `.risk-chart` / `.risk-fill` |
| Heatmap | Segment × dimension | `.heatmap` |
| Dot plot | Two metrics per entity | `.dotplot` |
| Scope list | Methodology, agenda | `.scope-grid` |
| Action cards | Recommendations | `.action-grid` |
| Timeline | Year milestones | `.timeline-banner` or custom |

### Gamma / Kimi (describe in prompt — tool renders chart)

| Chart type | Best for |
|------------|----------|
| Bar / column | YoY comparison, goal vs actual |
| Pie / donut | Composition (headcount, budget split) |
| Line | Trends over quarters |
| Table | Rating distribution, program list |
| Icon cards | Highlights, initiatives |
| Process flow | HR cycle, performance process |

Pick charts that match **data type** (survey vs year-end narrative). Prefer ?6 data points per slide.

## Chart math (HTML / shared numbers)

- Survey scale 1–5: bar width `(score/5)×100%`; benchmark 3.0 at **60%**
- Heatmap cells: **44px** height
- Dot position: `((score?1)/4)×100%`
- Percentages: use explicit % from data or computed count/n

## Agent output format

### A. Chart inventory

| Chart ID | Chart type (HTML / Gamma / both) | Insight | Audience question |
|----------|----------------------------------|---------|-------------------|
| CH-01 | | | |

### B. Detailed spec per chart

```
CH-XX — [type]
Platforms: HTML | Gamma | Kimi | all
Data source: [column / text quote / computed]
Rows / data points:
  - Label | value | display format
Callout stat: [bold number + sentence]
Why this chart: [1 line]
```

### C. Charts excluded

2–3 rejected ideas and why.

### D. Data blocks (for Step 6)

```json
{
  "kpiValues": [{"label":"","value":"","display":""}],
  "charts": [
    {"id":"CH-01","type":"","title":"","rows":[],"gammaHint":"","kimiHint":""}
  ]
}
```

End with: **CHART PLAN COMPLETE — ready for Step 3 (storyline)**
