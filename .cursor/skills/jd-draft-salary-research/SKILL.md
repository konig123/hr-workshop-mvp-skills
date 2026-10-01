---
name: jd-draft-salary-research
description: >-
  Draft Ashby-style job descriptions from a rough brief (defaults: company ABC
  Company, location Hong Kong), auto-save each JD as markdown, then research
  market salary bands from primary recruiter guides with a research note plus
  optional canvas. Use when the user asks to draft a JD, write a job
  description, market-price a role, run a salary search for a position, or
  wants the full JD + compensation pack. Do not use for Koshin LinkedIn/jobsDB
  Word JDs (use koshin-jd-style).
---

# JD Draft + Salary Research

End-to-end hiring pack matching this workflow:

1. Clarify blocking facts → draft Ashby-style JD (defaults below)  
2. **Auto-save** the JD as `.md` after every draft  
3. Research market pay from primary sources → research note (+ canvas for the numbers)

## Defaults (always apply unless the user overrides)

| Field | Default |
|-------|---------|
| Company name | **ABC Company** |
| Location | **Hong Kong** |

Do **not** ask for company or location when these defaults apply. If the user names a different company or city, use theirs.

## Progress checklist

Copy and track:

```
Progress:
- [ ] Phase A — JD draft
- [ ] Phase B — Auto-save JD
- [ ] Phase C — Salary research (if asked, or offered after JD)
```

---

## Format routing

| User intent | Action |
|-------------|--------|
| Default / “draft a JD” / Ashby / OpenAI-style | This skill + Ashby template |
| Koshin / LinkedIn / jobsDB / `.docx` Word JD | **Stop** → use `koshin-jd-style` instead |

Template is bundled at [references/jd-template.md](references/jd-template.md). This skill drafts the Ashby-style JD and adds auto-save + salary benchmark phases around that draft.

---

## Phase A — Draft the JD

### 1. Extract from the brief

Pull: role title, company, location, team/department, employment type, compensation, role summary, must-haves, nice-to-haves, company blurb, benefits.

Apply defaults: company → **ABC Company**, location → **Hong Kong**, unless overridden.

### 2. Ask only for blocking gaps

One short batch max. Ask if missing:

| Field | If missing |
|-------|------------|
| Role title | **Ask** |
| Company name | Default **ABC Company** — do not ask |
| Location | Default **Hong Kong** — do not ask |
| Must-haves | **Ask** if none given |
| Compensation | Keep `[Compensation TBD]` — never invent bands in the JD |
| Team / employment type | Default `TBD` / `Full-time` |
| About company | Short placeholder; mark for user edit |

Do **not** invent salary, equity, or company-specific EEO/legal walls of text.

### 3. Write the JD

- Follow Ashby section order and labels **exactly** (see [references/jd-template.md](references/jd-template.md)).
- Direct tone; “We expect you to”; 3–7 must-haves; 2–5 nice-to-haves.
- Deliver plain text in chat (no long preamble).
- After the JD, optional 2–3 line **Assumptions** if placeholders were used.
- **Immediately run Phase B** (auto-save) — do not wait for the user to ask.

### 4. Offer next step

If compensation is TBD and the user did not already ask for pay data, one line:

> Want a market salary search for this role next?

If they already asked for JD + salary / market price, continue to Phase C without waiting.

---

## Phase B — Auto-save JD

Run **after every successful Phase A draft** (no user “save” required):

1. Confirm workspace root (`pwd` + project marker).
2. Write a kebab-case markdown file, e.g. `{role-slug}-jd.md` (workspace-relative path). Overwrite if the same slug already exists unless the user asked to keep a prior version.
3. Verify with `test -f …`.
4. In the same turn as the JD, briefly note the saved filename (e.g. `Saved as finance-manager-jd.md`).

---

## Phase C — Salary research

Trigger when the user asks for market price, salary band, compensation research, or accepts the offer after Phase A.

Follow [references/salary-research.md](references/salary-research.md). Default location for market search is **Hong Kong** unless the JD was overridden to another market.

**Hard rules:**

- Prefer **primary** recruiter/gov sources for the role’s market (not random blogs).
- Never invent numbers; cite source + edition/year + URL.
- State **base vs total cash**; note bonus/MPF/benefits separately when known.
- Map findings to **this JD’s** seniority, scope, and location.
- Give a practical **posting/offer window** + target mid for the employer.

**Outputs (default):**

1. Chat: short verdict table (posting range + recommended mid).  
2. Workspace file: `{role-slug}-salary-research.md` with citations.  
3. Canvas: when the analysis is quantitative, also write a `.canvas.tsx` under the workspace canvases dir (follow the Cursor canvas skill) and link it.

After research, offer one line to **patch the JD Compensation line** with the recommended band (only if the user wants).

---

## File naming

| Artifact | Example |
|----------|---------|
| JD | `hr-manager-jd.md` |
| Salary note | `hr-manager-salary-research.md` |
| Canvas | `hr-manager-salary.canvas.tsx` (in managed `canvases/`) |

---

## Example trigger

User: “Draft an HR Manager JD” → ask must-haves only (company/location default) → Ashby JD → auto-save `hr-manager-jd.md` → offer salary search.  
User: “What’s the market price?” → Phase C → research md + canvas + recommended HKD band.
