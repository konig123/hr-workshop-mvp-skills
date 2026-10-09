---
name: video-transcript-storyboard
description: Use when turning a video, YouTube link, transcript, onboarding email, training demo, product walkthrough, or recorded lesson into a scene-by-scene storyboard, especially when the user asks for bilingual English/Traditional Chinese output, an editable table, Descript prompts, or a format matching a screenshot/table.
---

# Video Transcript Storyboard

## Overview

Create a transcript-backed storyboard artifact from video content. The default output is an editable bilingual HTML table with English and Traditional Chinese versions plus one copy-ready Descript prompt per scene.

## Workflow

1. **Extract or obtain the transcript**
   - Prefer the video platform transcript/captions when available.
   - If extraction fails, say so and ask for a transcript; do not invent missing narration.
   - Preserve the original narration before summarizing.

2. **Segment into storyboard scenes**
   - Group by intent, not equal time slices.
   - Estimate timings only when exact timestamps are unavailable; label estimates clearly.
   - Default columns: Scene, Time, Goal, Narration, **MiniMax TTS**, Visual, On-Screen Text, Asset, Risk Check, Descript Prompt.
   - `narration` = human VO. `ttsScript` = exact MiniMax T2A string (rewrites + `<#…#>` pauses). For Vox/Yue films, fill MiniMax TTS via `minimax-yue-tts-script`; do not send `narration` to T2A when `ttsScript` exists. If English is mispronounced, follow `minimax-yue-tts-script` **english-words.md** (S14 method): remove dict phonetic hacks; send lowercase real English.

3. **Create bilingual content**
   - English version should stay close to the source transcript.
   - Traditional Chinese version must use Traditional Chinese, not Simplified Chinese.
   - Keep scene IDs, timings, assets, and risk checks aligned across both languages.

4. **Generate Descript prompts**
   - Each prompt must be copy-paste ready for one scene.
   - Include scene number, duration, goal, voiceover, visual direction, on-screen text, assets, production notes, and style.
   - Do not make one generic prompt for the whole video unless the user asks.

5. **Produce an editable artifact when requested**
   - Create a scene JSON file matching `references/storyboard-schema.md`.
   - Run:
     ```bash
     python ~/.cursor/skills/video-transcript-storyboard/scripts/build_storyboard_html.py input-scenes.json output-folder
     ```
   - Open `output-folder/storyboard.html`.

## Encoding Guardrails

- Use UTF-8 for source files.
- For generated `storyboard-data.js`, write JSON with escaped Unicode (`ensure_ascii=True`) so CJK text cannot turn into four-question-mark runs.
- After writing files, scan:
  ```bash
  rg "\?{4}|\ufffd" output-folder ~/.cursor/skills/video-transcript-storyboard
  ```
- If the browser still shows old question-mark runs, bump the HTML localStorage key or tell the user to reset edits.

## Quality Checklist

- Transcript source is explicit.
- Storyboard is scene-based and not just a prose summary.
- English and Traditional Chinese versions contain the same scenes.
- Traditional Chinese has no question-mark runs, replacement characters, or Simplified-only phrasing.
- The last column contains per-scene Descript prompts.
- Vox/Yue films include a MiniMax TTS (`ttsScript`) column; T2A uses that, not Narration.
- Editable output preserves user edits in-browser or exports JSON.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Markdown-only table when user asked editable | Generate HTML/CSV/JSON artifact. |
| Generic Descript prompt | Create one prompt per scene. |
| Transcript invented after extraction fails | Ask for transcript or mark gaps clearly. |
| Chinese text becomes question-mark runs | Generate data with escaped Unicode and scan before final. |
| Timing presented as exact when estimated | Say timings are estimated. |

## Resources

- `scripts/build_storyboard_html.py`: Builds editable bilingual `storyboard.html` and ASCII-safe `storyboard-data.js`.
- `references/storyboard-schema.md`: Input JSON shape and scene-field guidance.
