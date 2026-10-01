---
name: linkedin-candidate-search
description: >-
  Scores public LinkedIn profiles against a workspace JD file and a
  hiring-requirements file, then writes a ranked Cursor canvas. Use when
  the user names this skill, asks for a LinkedIn candidate shortlist, or
  wants scored profiles from local JD / hiring-requirements folders.
disable-model-invocation: true
---

# LinkedIn candidate search

Copy and track:

```
Progress:
- [ ] Folders ready (JD/ and hiring-requirements/)
- [ ] One JD file + one hiring-requirements file chosen
- [ ] Criteria extracted
- [ ] Public LinkedIn search (no invented people)
- [ ] Ranked shortlist (default 10)
- [ ] Canvas written
```

Do **not** search LinkedIn until both files are chosen. Do **not** message, InMail, or reject anyone.

## Hard rules

- **Draft only.** Rank and recommend. The user send/decides.
- **Ground, don’t invent.** Every candidate needs a public LinkedIn URL and evidence from that profile (or a cited public page). If you cannot verify the person, drop them.
- **No protected-characteristic scoring.** Do not use age, gender, race, photo, appearance, marital status, disability, or religion.
- **Work identity only.** Name, title, company, location, public LinkedIn URL. No HKID, passport, address, DOB, phone scrape, or health.
- **Follower status is a proxy** unless the user has Recruiter/Sales Nav and pastes the follow filter. Never claim “follows the hiring company” as a fact from the public web.
- **Salary is inferred**, never invented as known. Score “likely in band” vs market title/scope. Cite the market source when you use one.
- Exclude people already in the hiring company (incumbent, internal). Note them under **Not on this list**.

## 1. Folders

Workspace root of the **open repo** (relative paths only; confirm with `pwd` first):

| Folder | Purpose |
|---|---|
| `JD/` | Job description files |
| `hiring-requirements/` | Extra filters (culture, salary, followers, visa, language, and other named criteria) |

**If both folders exist:** list files in each (ignore `README.md`, `.gitkeep`, `.DS_Store`). Ask which **one JD** and which **one hiring-requirements** file to use. Prefer `AskQuestion`. Wait.

**If one or both folders are missing:** ask whether to create them. If the user says yes, `mkdir -p JD hiring-requirements` from repo root and confirm with `ls`. Then ask them to put files in and **tell you when they are ready**. Do not invent a JD. When they say ready, list files and ask which to use in each folder.

**If a folder exists but has no usable files:** treat as not ready. Ask them to add a file and tell you when to continue.

Usable files: `.md`, `.txt`, `.pdf`, `.docx`, `.html`, or a file that contains a JD URL.

If the chosen JD is a URL, fetch it. If fetch fails, ask for a paste.

## 2. Extract criteria

From the JD pull: title, company, locations, must-haves, nice-to-haves, languages, team scope, seniority, visa notes.

From hiring-requirements pull extra score axes. Typical (use only if present):

- Culture (e.g. tech / startup)
- Salary range (currency + period)
- LinkedIn follower of the hiring company
- Location / right-to-work
- Other named filters

Restate the locked files + extracted criteria in one short paragraph. Then search.

Scoring math: [scoring.md](scoring.md). Sample files: [examples.md](examples.md).

## 3. Search LinkedIn

Public web only unless the user pastes Recruiter results.

1. Build search queries from title, must-haves, location, competitors, languages.
2. Prefer `site:linkedin.com/in` plus company/title keywords.
3. Open/fetch profiles you will score. Discard anyone without a working profile URL.
4. Default **10** candidates, high composite to low, unless the hiring-requirements file says otherwise.
5. Flag JD-vs-salary clashes (Head title vs Manager cash band) in a warning callout — do not hide them.

Cannot enumerate company-page followers. Use the **proxy** in [scoring.md](scoring.md) and put a Recruiter Boolean on the canvas.

## 4. Canvas output

Required. Follow `~/.cursor/skills-cursor/canvas/SKILL.md` and [canvas-output.md](canvas-output.md).

Write one file under the workspace canvases directory, named `{role-slug}-linkedin-shortlist.canvas.tsx`.

Chat reply: ranked table + markdown link to that canvas + one line that Recruiter is needed to verify followers. Do not dump a second copy of the full canvas as a markdown table if the canvas is complete.

## Done check

- Both folders used; filenames named in chat
- 10 (or requested N) people, each with LinkedIn URL
- Composite scores ordered high to low
- Salary and follower axes labelled inferred / proxy
- Canvas opens with real data (no empty states)
