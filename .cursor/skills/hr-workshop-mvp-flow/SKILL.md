---
name: hr-workshop-mvp-flow
description: Use when an HR workshop student kicks off the workshop, uploads a filled brainstorm worksheet (any filename), pastes or attaches an idea document, describes an internal tool, or wants to go from a rough idea to PRD, HTML prototype, Next.js MVP, and local run. This is the generic student entry for every group. Do not require a Group 6 / Group 4 wrapper.
---

# HR Workshop MVP Flow

## Purpose

This is the **student kickoff skill for every group**. Guide non-technical HR workshop students from their own idea (usually an uploaded filled brainstorm sheet, any filename) to PRD, HTML prototype, Next.js MVP, and a local browser preview.

Do not load Group 6 Talent Mapping, Group 4 Pulse Survey, or any other wrapper defaults unless the student's idea already is that product, or the instructor explicitly asks to use an example wrapper.

Keep student-facing output simple, practical, and low-jargon.

Use this skill when the user mentions:
- start / kick off the HR workshop
- brainstorm sheet, PRD worksheet, uploaded/filled worksheet (any name)
- idea document, brief, one-pager, pasted requirements
- HR workshop, L&D workshop, internal HR tool
- rough idea to MVP, PRD, HTML prototype, Next.js, Supabase, Vercel

## Core Rules

- This skill is enough. Students do not need `grp6-talent-mapping-mvp-flow` or another group wrapper.
- Follow the student's idea document or filled worksheet. Do not steer them into a standard Talent Mapping / Pulse Survey / Attendance MVP if their document is a different tool.
- Filename does not matter. Read whatever they attach or paste. Do not require `prd_brainstorm_sheet.md` or `day3 teaching materials/`.
- If the student already uploaded a filled brainstorm sheet, extract and confirm it. Do not refill it from scratch or re-ask questions they already answered.
- Move one stage at a time. After every stage, ask: "Do you want to proceed to the next step?"
- Do not skip confirmation gates. The student must confirm the MVP functions before PRD generation.
- Keep the MVP to a maximum of 5 functions. If the idea has more, group or defer functions.
- Prefer plain language over technical terms. If a technical term is necessary, explain it in one short sentence.
- Do not automatically connect Supabase or Vercel. Build or plan the app, then provide step-by-step connection guidance.
- Default database: Supabase.
- Default deployment: Vercel.
- When generating PRDs, use the `prd-writer` skill if available.
- When the student confirms an HTML or Next.js plan, or says the prototype will not run, follow `workshop-local-run` before `npm` or opening localhost. Pass `mode` (`preflight` or `repair`) and `kind` (`html` or `nextjs`). Do not ask the student to run terminal commands. Detect `projectDir` and `successPath` from this project; do not assume `talent-mapping-next` or `/login`.
- Do not overwhelm the student with architecture details unless they ask.

## Stage Flow

### Stage 1: Collect Input

Students usually start by **uploading a filled brainstorm sheet**. Treat any attached, pasted, or pointed-to file as the source. Ignore the filename.

**Read that first.** Do not search for `day3 teaching materials/prd_brainstorm_sheet.md`. Do not ask them to rename the file.

Decide the input type from **content**, not the name:

| What they gave you | Treat it as | Next |
|---|---|---|
| Covers pain/problem, desired result, and functions (headings may differ; Word/PDF/Markdown/image are all OK) | Filled brainstorm worksheet | Summarize, then Stage 2 Path A. Skip blank filling. |
| A brief, one-pager, or rough idea without a function list | Idea document | Summarize, then Stage 2 Path B |
| Nothing | Missing input | Ask for the sheet or a short idea |

If nothing was provided, ask:

```text
Please upload your filled brainstorm sheet (any filename is fine), or describe your HR tool in 1-3 sentences.
Who uses it, what problem does it solve, and what result should it produce?
```

Do not ask them to rewrite the document in 1-3 sentences if those answers are already in it.

If the idea is still vague after the document, ask at most 2 follow-up questions:
- Who is the main user: HR, manager, employee, leadership, or candidate?
- What painful manual process should this replace?

Then summarize **their** product, not a workshop example:

```markdown
## My Understanding
This tool is for [user group]. It helps them [main job] so that [business result].
```

If it was a **filled worksheet**, end with:

```text
Is this correct? If yes, I will map your sheet and we can confirm the MVP functions.
```

If it was only a **rough idea**, end with:

```text
Is this correct? Do you want to proceed to the worksheet step?
```

### Stage 2: Worksheet — Extract or Fill

Use this structure in chat. Do not depend on a local teaching-file path. Do not edit the student's file unless they ask.

- Part 1: Pain point
- Part 2: Ideal result
- Part 3: Function list
- Part 4: Data
- Part 5: Constraints
- Part 6: Flow
- Final check

#### Path A — Student uploaded a filled sheet (default)

1. Map **their** answers onto Parts 1–6. Keep their wording. Headings do not need to match.
2. Do not write a new worksheet from scratch. Do not re-ask questions they already answered.
3. Mark gaps as `Missing:` and inferences as `Assumption:`.
4. For Part 3, split into Must-have MVP / Nice to have / Future. Cap must-have at 5. If they listed more, group or defer — do not invent extra functions.
5. Output the mapped worksheet in chat.

#### Path B — No filled sheet, only a rough idea

Fill the same Parts 1–6 in chat from the Stage 1 idea. Short point form. Mark `Assumption:` clearly. Cap must-have MVP functions at 5.

If a local teaching copy of the blank sheet exists, you may use it only as a layout reference. Never require the student to have that file or that filename.

Both paths end with:

```text
Please confirm the MVP functions above. We should keep maximum 5.
Do you want to keep, remove, or combine any function before we create the PRD?
```

### Stage 3: Confirm MVP Functions

Present only the MVP function shortlist:

```markdown
## Proposed MVP Functions
1. [Function] - [simple purpose]
2. [Function] - [simple purpose]
3. [Function] - [simple purpose]
4. [Function] - [simple purpose]
5. [Function] - [simple purpose]

## Not In MVP
- [Future function]
- [Future function]

Please confirm: are these the final MVP functions?
```

Do not move to PRD until the user confirms.

### Stage 4: Create Concept PRD With prd-writer

Use `prd-writer` mode A. Create the first version: product concept document.

Student-facing output should include:
- Product name
- One-sentence positioning
- Product format
- Target users
- Product value
- Core MVP function directions
- Not in scope
- Open questions

For product format:
- Recommend Web App by default for internal HR tools.
- Explain simply: "A web app works in the browser and is easiest for HR/admin dashboards."

End with:

```text
Does this product direction look right? If yes, we can move to the detailed PRD.
```

### Stage 5: Move to ?? PRD

Only after concept PRD confirmation, create the detailed implementation PRD.

Include:
- Product overview
- Target users and scenarios
- User flow
- MVP function tree
- One key page wireframe in ASCII
- Detailed description for each MVP function
- Data needed
- Role permissions
- Simple copywriting examples
- Non-functional needs in plain language
- Remaining questions

Keep the language non-technical. Explain database/security as:
- "Data needs to be saved safely."
- "Different roles should see different information."

End with:

```text
Please review this detailed PRD. If it looks right, we can plan the HTML prototype.
```

### Stage 6: Plan HTML Prototype

Create a simple development plan for a single-file HTML prototype.

The prototype plan should include:
- Goal
- Scope
- Screens
- Mock data
- Main user flow
- Interactions
- Build order
- Testing checklist

Default prototype requirements:
- Single HTML file
- Embedded CSS and JavaScript
- Mock data in JavaScript arrays
- No real login
- Role switcher for demo
- No database
- No Supabase or Vercel yet

End with:

```text
Do you want to build this HTML prototype now, or adjust the prototype plan first?
```

If the student chooses to build now: follow `workshop-local-run` with `mode=preflight` and `kind=html` **before** writing the HTML file. If the machine is not ready, finish that skill first. Then build. If later they cannot open the HTML, follow `workshop-local-run` with `mode=repair` and `kind=html`.

### Stage 7: Plan Usable Next.js App

After the HTML prototype is confirmed, create a Next.js MVP development plan.

Default stack:
- Next.js
- Supabase for database and login
- Vercel for deployment

Student-facing plan should be plain-language first:

```markdown
## What changes from prototype to real app
- Demo data becomes saved data.
- Role switcher becomes real login.
- Buttons save to a database.
- Export creates real files.
- HR/admin permissions are enforced.
```

Then include a simple phase plan:
1. Set up Next.js app
2. Set up Supabase database and login
3. Build pages from prototype
4. Add form save/submit flows
5. Add role permissions
6. Add export
7. Test
8. Deploy to Vercel

End with:

```text
Do you want to implement the Next.js MVP now, or review the plan first?
```

If the student chooses to implement now: follow `workshop-local-run` with `mode=preflight` and `kind=nextjs` **before** `npx create-next-app`, `npm install`, or `npm run dev`. Pass `projectDir` and `successPath` if the Group wrapper defined them. If later they cannot open localhost, follow `workshop-local-run` with `mode=repair` and `kind=nextjs`.

### Stage 8: Post-Build Missing Items

After the app is completed, explain what is still missing before real company use.

Use this format:

```markdown
## What Is Completed
- [Completed area]

## What Is Still Missing Before Real Use
- Supabase project needs to be connected
- Vercel deployment needs to be connected
- Real users and roles need to be created
- Real employee data needs to be imported
- Company privacy/security review is needed
- Email notifications/reminders may still need setup
- Backup/export process should be agreed

## How To Connect Supabase
1. Create a Supabase account.
2. Create a new project.
3. Copy the project URL and anon key.
4. Add them to `.env.local`.
5. Run the database migration SQL.
6. Create test users.
7. Test login and role permissions.

## How To Deploy To Vercel
1. Push the app to GitHub.
2. Create a Vercel account.
3. Import the GitHub repository.
4. Add the same environment variables in Vercel.
5. Click Deploy.
6. Test the live URL.
```

Keep this as a checklist for non-technical HR users.

## Output Style

- Use English unless the student uses Chinese/Cantonese; then mirror their language.
- Use tables for worksheets and checklists.
- Avoid long technical explanations.
- Use labels like "Assumption" and "Decision needed".
- Always ask before proceeding to the next stage.

## Common Mistakes

- Do not produce a full technical build plan before MVP functions are confirmed.
- Do not include more than 5 MVP functions.
- Do not treat the HTML prototype as production.
- Do not claim Supabase/Vercel is connected unless actually configured.
- Do not bury the student in database schema unless they ask for developer details.
- Do not skip the "what is still missing" explanation after the app is completed.
- Do not tell the student to run `pwd`, `cd`, `npm install`, or `npm run dev`. Use `workshop-local-run`.
- Do not start HTML or Next.js implementation until `workshop-local-run` preflight has run for that stage.
- Do not start from Group 6 Talent Mapping (or any other group wrapper) when the student only kicked off this generic skill or pasted a different idea document.
- Do not require the filename `prd_brainstorm_sheet.md` or the path `day3 teaching materials/`.
- Do not refill a brainstorm sheet the student already uploaded. Extract, map, and confirm.
- Do not skip their uploaded functions and invent a new function list.
