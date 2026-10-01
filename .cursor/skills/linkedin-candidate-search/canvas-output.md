# Canvas output

Read `~/.cursor/skills-cursor/canvas/SKILL.md` first. One `.canvas.tsx` file. Import only `cursor/canvas`. Embed all candidate data. No `fetch`. No empty states.

## File

Workspace canvases directory:

`{role-slug}-linkedin-shortlist.canvas.tsx`

Example: `hr-manager-linkedin-shortlist.canvas.tsx`

## Required sections (in order)

1. **H1** — `{Company} {Role} — public LinkedIn shortlist`
2. **Warning Callout** if salary band clashes with posted seniority
3. **Stats row** — N scored, market band used, follower = Unverified, internals excluded
4. **BarChart** (horizontal) — composite score by candidate, titled, axis units 0–100
5. **Table** — rank, name (Link to LinkedIn), current role, location, composite, JD, culture, salary, follower, level pill
6. **Cards** — one per person: why, risk, Mandarin/language, follower proxy note
7. **Not on this list** table — incumbents / internals / over-band Heads you dropped
8. **Recruiter Boolean** card — copy-paste follow filter

## Data shape

Keep weights in a `WEIGHTS` constant. Each candidate:

- rank, name, title, company, location, url
- jd, culture, salary, follower (0–100)
- why, risk
- language status
- followerNote (proxy sentence)
- level: `Head+` | `Lead/SM` | `Manager` | `Stretch`

Composite = round(jd*wJd + culture*wCulture + salary*wSalary + follower*wFollower). If an axis was dropped, omit it from the type and the table.

Row tone: salary ≥ 70 success; salary < 40 warning.

## Design

`useHostTheme()` tokens only. No gradients, emoji, box-shadows, rainbow pills. Mix a heading + table + a few cards — do not wrap every block in the same Card.

After write, tell the user they can open the canvas beside the chat, with a markdown link to the **absolute** `.canvas.tsx` path.

## Chat companion

Lead with the ranked 10. Link the canvas. One sentence: company-page followers need Recruiter. Name the JD filename and hiring-requirements filename used.
