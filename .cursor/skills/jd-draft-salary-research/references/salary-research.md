# Salary research protocol

Use after (or with) an Ashby JD draft. Goal: a citable market band for **this** role profile, not a generic internet average.

## Workflow

```
- [ ] Lock role profile from the JD
- [ ] Search primary guides for that market
- [ ] Normalize units (monthly → annual ×12; note currency)
- [ ] Triangulate 2–4 sources
- [ ] Map to JD seniority/scope
- [ ] Recommend posting + offer mid
- [ ] Write research md (+ canvas if quantitative)
```

## 1. Lock the profile

From the JD, record:

- Title and aliases (e.g. HR Manager / HRBP)
- Location (city / country / remote)
- Years of experience / seniority
- Scope (IC vs manages N; local vs regional)
- Industry if known (FS / tech / mid-market corporate)
- Must-have premiums (e.g. local employment law, bilingual)

## 2. Preferred primary sources

Prioritize **first-party** salary guides and official tools. Pick sources that match the **location**.

### Hong Kong (example set)

| Source | Where to look |
|--------|----------------|
| Robert Half | HK salary guide pages (often annual percentiles) |
| Morgan McKinley | HK salary guide / role detail pages (often monthly L/Med/H) |
| Michael Page | HK salary guide / benchmark tool (often average base by title) |
| Jobsdb by SEEK | Role Salary Insights (live job ad disclosures) + annual *Hiring, Compensation & Benefits Report* (increments & bonus months) |
| Hays | Asia Salary Guide / Salary Checker (may be gated) |
| Randstad / Robert Walters | HK guides or contractor/permanent PDFs when first-party |

### Other markets

Use the same firms’ local guides, plus reputable local surveys. Prefer placement-based recruiter guides over crowd-only sites (PayScale/Glassdoor = secondary cross-check only).

Skip or clearly flag: ungated scrapes of unknown origin, SEO listicles, data older than ~3 years unless nothing newer exists.

## 3. Collect & normalize

For each source, capture:

- Edition / year
- Role title as published
- Low / mid / high (or P25 / P50 / P75)
- Monthly vs annual
- Base only vs total cash
- Any company-size or industry split

**Normalize to annual local currency** for the summary table. Always show the conversion math when monthly (×12). Do not invent FX; if converting currencies, state rate source/date or keep dual-currency.

## 4. Map to the JD

| JD signal | Pay implication |
|-----------|-----------------|
| Years between two published bands | Interpolate; say so |
| Team lead / small team | Prefer Manager band, not Head of |
| Regional / multi-market | May sit at Regional Manager / Senior Manager |
| Mid-market generic co. | Prefer mid of Manager band; FS/MNC often higher |
| Scarce bilingual / local law | Justify high end of Manager band |

## 5. Recommend

Produce:

1. **Posting / offer window** (employer-facing base range)  
2. **Target mid** (where most offers should land for this JD)  
3. **High / stretch** (exceptional hire or Senior Manager territory)  
4. **Suggested JD Compensation line** (e.g. `HK$650,000 – HK$840,000 · plus discretionary bonus`)

Caveats to include when relevant: base vs bonus, industry premium, title inflation, mover uplift % if the guide states it.

## 6. Research markdown shape

Save as `{role-slug}-salary-research.md`:

```markdown
# {Location} {Role} — Market Salary Research

**Role profile:** …
**JD anchors:** …
**Research date:** …
**Currency:** …

## Executive summary
(recommended band + table Low / Mid / High)

## Source-by-source findings
(cite URL + year; tables of figures)

## Mapping to this JD
(short table)

## Recommended offer band
(floor / target / ceiling + suggested JD line)

## Caveats
## Sources checklist
```

## 7. Canvas (when numbers are the deliverable)

Follow the Cursor `canvas` skill. Typical layout:

- 3 stats: recommended mid, posting range, stretch
- Callout with verdict
- Bar chart of source midpoints
- Table of source detail
- Suggested JD compensation line

Link the `.canvas.tsx` with a markdown link to its full path.

## Anti-patterns

- Filling Compensation in the JD with made-up numbers before research  
- Treating crowd averages as equal to recruiter guides  
- Mixing monthly and annual in one table without labels  
- Recommending Head-of-HR bands for a Manager-of-2–5 JD
