# HR Workshop MVP Skills

Cursor skills for the HR workshop: take a filled brainstorm sheet to a PRD, a confirmed build slice, an HTML prototype, and one working path in the local browser.

These skills are for **every group**. You do not need a Talent Mapping or Pulse Survey wrapper.

## What this repo installs

| Skill | What it does |
|---|---|
| `hr-workshop-mvp-flow` | Student kickoff: read your sheet, confirm up to 5 MVP functions, lock today's build slice, write the PRD, and build only that slice |
| `prd-writer` | Makes the concept PRD and the detailed PRD more complete |
| `workshop-local-run` | Checks Node/folder/port and opens the HTML or localhost page. You do not type terminal commands |
| `html-executive-deck-generation` | Guided 6-step executive deck: CSV/XLSX or text → HTML slides plus Gamma and Kimi prompts (DAYMARK visual system) |

## Install in Cursor (students)

Do **one** of the two options. Option A is enough for class.

### Option A — Open this folder (recommended)

1. Download this repository: on GitHub, click the green **Code** button → **Download ZIP**.
2. Unzip it. You should see a folder named `hr-workshop-mvp-skills`.
3. Open Cursor.
4. **File → Open Folder…** and choose that `hr-workshop-mvp-skills` folder.
5. Confirm the skills loaded: in Cursor, open **Customize** in the sidebar → **Skills**. You should see the names in the table above.
6. In **Agent** chat, say:

```text
Start the HR workshop
```

Then upload your filled brainstorm sheet. Any filename is fine (Word, PDF, Markdown, or a photo of the sheet).

### Option B — Install for every project (global)

Use this if you want the skills to work after you open a *different* folder (for example your own app folder).

**If you can run a terminal command** (Cursor → Terminal → New Terminal):

```bash
npx skills add konig123/hr-workshop-mvp-skills --agent cursor --global
```

**If you prefer to copy folders by hand:**

1. Finish Option A so the unzipped folder is on your computer.
2. Copy these folders:

   - `.cursor/skills/hr-workshop-mvp-flow`
   - `.cursor/skills/prd-writer`
   - `.cursor/skills/workshop-local-run`
   - `.cursor/skills/html-executive-deck-generation`

3. Paste them into your user skills folder:

   - Mac: `~/.cursor/skills/`
   - Windows: `%USERPROFILE%\.cursor\skills\`

   On a Mac, in Finder press Cmd+Shift+G and paste `~/.cursor/skills`.

4. Restart Cursor, or close and reopen the window.
5. Check **Customize → Skills** again.

## After install — class start

1. Open Cursor on this repo (Option A) or on your project folder (Option B).
2. Open **Agent** chat (not Ask).
3. Say `Start the HR workshop` and attach your filled brainstorm sheet.
4. Confirm each step when the agent asks. Do not skip “are these the final MVP functions?” or the **Build Slice** card (one user, one happy path, what is not in this build). The session builds the slice, not the full MVP list.
5. When it is time to open the prototype, let the agent run the computer checks. You should not type `npm` or `localhost` yourself.

## What not to install

Do **not** add Group 4 / Group 6 wrapper skills unless the instructor asks. This pack is the generic student entry.

`prd-writer` is included here under MIT. Original project: [chituai/prd-writer](https://github.com/chituai/prd-writer).

## For instructors

This repository is public on purpose. It contains skill markdown plus DAYMARK logo/mood-board images used by `html-executive-deck-generation`. No API keys, student work, or `.env` files.

If you update a skill locally, copy the changed folder back into `.cursor/skills/` here and open a pull request.
