---
name: minimax-audio-generator
description: >-
  Generate high-quality voiceover audio (MP3) from text using MiniMax Text-to-Speech (T2A)
  API with a self-guarding security gate. Automatically detects or sets up .env.local and
  updates .gitignore so users never paste API keys into the chat. Supports Cantonese
  (粵語), English, and Mandarin with natural pauses and preset/custom voices.
---

# MiniMax Audio Generator (Self-Guarding)

Generate professional audio voiceovers (MP3) from text scripts using the MiniMax Text-to-Speech (T2A) API.

Built with an **ironclad security gate**: prevents users from exposing API keys in chat sessions or accidentally committing secrets to GitHub.

---

## The Workflow

```
[Trigger: User asks to generate audio / voiceover / TTS]
       │
       ▼
Phase 0: Self-Guarding Security Gate (Check .env.local & .gitignore)
       │  ├── Missing key? Create .env.local + update .gitignore + instruct user in sidebar
       │  └── Key valid? Proceed to Phase 1
       ▼
Phase 1: Script & Voice Setup (Language, Voice ID, Speed, Pauses)
       │
       ▼
Phase 2: Preview & Approval Gate (Confirm text & settings before API call)
       │
       ▼
Phase 3: Generation & Delivery (Run Python runner, produce MP3, report duration)
```

---

## Phase 0: Self-Guarding Security Gate (MANDATORY FIRST STEP)

**Never allow the user to paste an API key into the chat window.**

Before accepting text or calling any API, perform this automated check:

### 1. Check for Existing API Key
Check if `MINIMAX_API_KEY` is already defined in:
1. Environment variables (`os.environ.get("MINIMAX_API_KEY")`)
2. `.env.local` or `.env` in the current workspace root

### 2. If Key is Missing or Placeholder (`your_...`)

**DO NOT ask the user to paste the key in chat.** Instead, execute these two actions:

1. **Protect Git (`.gitignore`):**
   Check if `.gitignore` exists in the workspace. If `.env*` or `.env.local` is not present, append:
   ```gitignore
   # Local environment & secrets
   .env.local
   .env*.local
   .env
   ```

2. **Create Safe `.env.local` File:**
   Create `.env.local` in the project root:
   ```env
   # MiniMax API Key for Text-to-Speech / Audio Generation
   # Replace the placeholder below with your real key and press Cmd+S / Ctrl+S to save
   MINIMAX_API_KEY=your_api_key_here
   ```

3. **Instruct the User (Hard Gate):**
   Output this exact guidance card in chat:

   > 🔒 **MiniMax API Key Required (Security Gate)**
   > 
   > I have created a safe `.env.local` file for you in this project and added it to `.gitignore` so your key is never committed to GitHub.
   > 
   > **How to set up:**
   > 1. Click on `.env.local` in the file explorer (left sidebar).
   > 2. Replace `your_api_key_here` with your actual MiniMax API key.
   > 3. Save the file (**`Cmd + S`** on Mac / **`Ctrl + S`** on Windows).
   > 4. ⚠️ **DO NOT paste your API key in this chat!**
   > 5. Once saved, simply reply here: *"I have saved my key"*.

4. **Wait for Confirmation:**
   Stop your turn. Do not continue until the user confirms and you verify that `.env.local` contains a valid key (not starting with `your_`).

---

## Phase 1: Script & Voice Setup

Once the API key is verified, gather the voice requirements:

### 1. Narration Script
- Accept text pasted by the user, or read from a designated markdown/script file.
- Clean up formatting: strip non-spoken cues (e.g. `[Scene 1]`, `[BGM fades]`, production notes).
- For natural breathing pauses, add `<#0.35#>` after sentence-ending punctuation (`。`, `！`, `？`, `.`).

### 2. Language Selection
- **Cantonese (粵語):** Set `language="yue"` (`language_boost: "Chinese,Yue"`). Ensure Hong Kong written colloquialisms (`我哋`, `仲有`, `嘅`) sound natural.
- **English:** Set `language="en"` (`language_boost: "English"`).
- **Mandarin:** Set `language="zh"` (`language_boost: "Chinese"`).
- **Mixed / Auto:** Set `language="auto"`.

### 3. Voice Preset
Choose from curated presets (see [references/voice-presets.md](references/voice-presets.md)):
- `female-chengshu`: Mature, confident, corporate executive (Default).
- `female-yujie`: Professional, steady explainer.
- `male-pure`: Sincere, clear, calm coach/trainer.
- `female-qn-qingse`: Warm, youthful, energetic.
- *Custom Voice:* Any cloned voice ID (e.g. `moss_audio_...`).

### 4. Speed & Output Destination
- Default speed: `1.0x` (or `1.1x` for dynamic explainer videos).
- Default output path: `public/audio/{slug}.mp3` (Next.js/Remotion) or `output/audio/{slug}.mp3`.

---

## Phase 2: Preview & Approval Gate

Before calling the API, display the synthesis card in chat:

```markdown
### Voiceover Generation Preview
- **Language:** Cantonese (Chinese,Yue)
- **Voice Preset:** female-chengshu (Professional Female)
- **Speech Speed:** 1.0x
- **Output Destination:** `public/audio/welcome-intro.mp3`

**Script Text:**
> 「歡迎大家參加今日嘅工作坊！喺呢個單元入面，我哋會一齊探索點樣運用 AI 工具提升工作效率。<#0.35#>請大家準備好手頭上嘅練習材料。」

Estimated Duration: ~10 seconds.
```

Ask the user: *"Does this script look good to generate? (Reply 'Yes' or provide adjustments)"*

---

## Phase 3: Generation & Delivery

When approved, run the bundled standalone Python runner (supports project or global skills directory):

```bash
# If running inside a project with the skill installed locally:
python3 .cursor/skills/minimax-audio-generator/scripts/minimax_tts.py \
  --text "Your approved script text here" \
  --output "public/audio/welcome-intro.mp3" \
  --voice-id "female-chengshu" \
  --language "yue" \
  --speed 1.0

# Or if running via global ~/.cursor/skills:
python3 ~/.cursor/skills/minimax-audio-generator/scripts/minimax_tts.py \
  --text "Your approved script text here" \
  --output "public/audio/welcome-intro.mp3" \
  --voice-id "female-chengshu" \
  --language "yue" \
  --speed 1.0
```

*Or read from a text file:*
```bash
python3 ~/.cursor/skills/minimax-audio-generator/scripts/minimax_tts.py \
  --text-file "scripts/narration.txt" \
  --output "public/audio/welcome-intro.mp3" \
  --language "yue"
```

### Post-Generation Verification
1. Confirm the file exists on disk with `test -f <output_path>`.
2. Report the result to the user:
   - File path (relative to workspace root).
   - Audio duration in seconds.
   - File size in KB.
   - How to reference it in HTML (`<audio src="/audio/welcome-intro.mp3" controls />`) or Remotion (`<Audio src={staticFile("audio/welcome-intro.mp3")} />`).

---

## Error Handling

| Issue | Cause | Solution |
|---|---|---|
| `KEY_NOT_FOUND` | No API key in `.env.local` or environment | Re-trigger Phase 0 instructions. Remind user to save `.env.local`. |
| `HTTP 401 / Invalid Key` | The key in `.env.local` is incorrect or expired | Ask user to check their MiniMax account dashboard and re-paste into `.env.local`. |
| `Status 1004 / Balance Exhausted` | Account out of quota/credits | Instruct user to top up credits on MiniMax platform. |
| Missing Cantonese tone | Spoken term pronounced awkwardly | Use explicit phonetic hints or Cantonese character rewrites (e.g. `返` → `番`). |
