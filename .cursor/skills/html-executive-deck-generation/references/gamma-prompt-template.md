# Gamma Slide Generation Prompt Template

Agent: fill every `[bracket]` from Deck Build Brief. Write finished prompt to `{topic}_gamma_prompt.md`.

User copies **everything below the line** into Gamma (Create ? Paste text / Generate presentation).

---

## PROMPT START (copy below)

You are creating a professional HR presentation in Gamma.

### Deck metadata

- **Title:** [Title]
- **Audience:** [Audience]
- **Period:** [Period]
- **Language:** [en / zh / etc.]
- **Tone:** Executive, confident, data-led, minimal jargon
- **Length:** [N] slides, 16:9
- **Presenter time:** ~[8–12] minutes

### Visual style (from user template)

If Template Profile is DAYMARK (default), use this block and skip empty brackets:

- **Primary color:** #0A335E (title fields)
- **Ink:** #153D66 (type)
- **Secondary / background:** #FBF8F3 (Bone content slides)
- **Accent rule:** #35827E (underline the turn of a headline; #42A9A4 on navy)
- **Accent once:** #EFB230 (one KPI or one sun per slide — never more)
- **Fonts:** Outfit for titles, Instrument Sans for body, IBM Plex Mono for captions
- **Style keywords:** navigational, daylight mark, executive brief, no shadows, no gradients
- **Paint:** DAYMARK mood board only (do not use the layout-reference firm's blues or logo)
- **Layout:** If the Deck Build Brief includes a layout reference, follow that page architecture (action titles, exhibit boxes, chart + key drivers, source footer). Structure only.

Do not use emoji. Use simple icons or charts only.

### Narrative arc (SCQA)

- **Situation:** [from Step 3]
- **Complication:** [from Step 3]
- **Question:** [from Step 3]
- **Answer:** [from Step 3]

---

### Slide-by-slide specification

Generate exactly [N] slides in this order. Each slide: title, on-slide text (short bullets), one primary visual, optional speaker note (1 sentence).

#### Slide 1 — Title

- **Title:** [deck title]
- **Subtitle:** [audience + period]
- **Visual:** Cover — [describe: abstract shape, photo style, or icon theme per template]
- **On-slide text:** [meta line, e.g. "HR Year-End Review 2025 | Leadership Briefing"]

#### Slide 2 — [title from storyline]

- **Headline:** [exact headline from brief]
- **Visual:** [CH-01 type — e.g. 3 KPI stat cards]
- **Data on slide:**
  - [KPI 1]: [value]
  - [KPI 2]: [value]
  - [KPI 3]: [value]
- **Speaker note:** [1 sentence hook]

#### Slide 3 — [title]

[Repeat for each slide in storyline table]

```
Slide N — [Title]
Purpose: [narrative job]
Visual: [chart type from Chart Plan — bar, pie, table, icon cards, timeline, etc.]
Data:
  - [row 1]
  - [row 2]
Callout: [insight callout sentence with bold stat]
Speaker note: [optional]
```

#### Final slide — [Actions / Close]

- **Title:** [e.g. Priorities for 2026 / Next Steps]
- **Visual:** 3 action cards or numbered list
- **Actions:**
  1. [Action 01 title] — [1 sentence]
  2. [Action 02 title] — [1 sentence]
  3. [Action 03 title] — [1 sentence]
- **Footer line:** [timeline banner text]

---

### Chart data appendix (for accuracy)

Paste exact numbers Gamma should use:

```json
[paste Chart Plan JSON from Step 2]
```

### Constraints

- One main idea per slide; no walls of text (max 5 bullets per slide)
- Every data slide includes one **insight callout** (single sentence with key number)
- Charts must reflect the data appendix — do not invent figures
- Keep consistent colors from Visual style section
- Last slide must end with clear next steps

### Output request

Generate the full presentation with the slide structure above. Use charts and layouts appropriate to each data type. Professional HR / executive quality.

## PROMPT END
