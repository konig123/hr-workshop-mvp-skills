# Step 1 ù Insight Analysis

Produce an **Insight Brief** only. No charts, slides, layout, or output files.

## Input modes

### Mode A ù Structured file (CSV / XLSX)

1. Run Python first ù [python-metrics.md](python-metrics.md). Do not calculate aggregates in the LLM.
2. Pulse-shaped files (`Manager` / `People Leader` + Q1ùQ20): `pulse-survey-analysis` runner with `--json-out`.
3. Any other CSV/XLSX: `scripts/compute_deck_metrics.py`.
4. Build this brief **only** from `metrics.json` (+ chart PNG paths). Infer scale/segments from JSON fields, not by re-summing the file.

### Mode B ù Free text (pasted narrative, bullets, notes)

1. Parse for: topic, period, audience, achievements, challenges, KPIs, headcount, programs, risks, recommendations.
2. Extract every number explicitly stated; label source quote.
3. **Do not invent metrics.** If a metric is implied but not quantified, list under data gaps as `[TBD]`.
4. For year-end performance text: identify themes (talent, engagement, L&D, recruitment, compliance, budget, etc.).

### Mode C ù Mixed

Use Python `metrics.json` for numbers; text for narrative framing and priorities.

## Agent output format

### A. Input summary

- Input type: file / text / mixed
- Source: [filename or "user pasted text"]
- Python metrics: [path to metrics.json, or N/A for text-only]
- Deck topic inferred: [e.g. HR Year-End Performance 2025]
- Language: [en / zh / etc.]

### B. Data profile

- Scope (population, period, org units)
- Segments available (dept, role, region, etc.)
- Dimensions or theme areas
- Quantified metrics found (table)
- **At-risk / threshold definitions** (if applicable; else N/A)

### C. Executive summary (max 3 sentences)

1. Overall story in one line
2. Core tension or headline achievement
3. Recommended focus for leadership / next period

### D. Key metrics table

| Metric | Value | Source | So what? |
|--------|-------|--------|----------|
| | | metrics.json field / text line | |

Adapt rows to content type (survey scores vs year-end HR KPIs vs qualitative themes).

### E. Segment or theme findings

- Top themes (ranked)
- Best / worst areas (if data supports)
- 2 surprising non-findings or caveats

### F. Insight hierarchy (ranked, exactly 5)

1. [Insight] ù evidence: [number or quote]
2. ù
5. ù

### G. Narratives to avoid

2ù3 misleading stories this content could be misread as.

### H. Open questions / data gaps

Missing numbers or clarifications needed before charts.

## Defaults (if user did not specify)

- Audience: senior leadership / CHRO
- Deck length target: 8ù12 slides, ~10 minutes
- Scale: 1ù5 only when survey data present

End with: **INSIGHT BRIEF COMPLETE ù ready for Step 2 (chart planning)**
