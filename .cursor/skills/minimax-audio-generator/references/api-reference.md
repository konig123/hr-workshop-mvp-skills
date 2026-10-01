# MiniMax T2A API Reference

MiniMax Speech v2 Text-to-Audio (T2A) API documentation.

## Endpoint & Authentication

- **URL:** `POST https://api.minimax.io/v1/t2a_v2`
- **Headers:**
  ```http
  Authorization: Bearer <MINIMAX_API_KEY>
  Content-Type: application/json
  ```

---

## Supported Models

| Model Slug | Recommended Use Case | Characteristics |
|---|---|---|
| `speech-2.8-hd` | High-definition general TTS (Default) | Ultra-natural cadence, expressive inflection, multi-language support |
| `speech-2.6-hd` | Video Voiceover & Explainer Films | Consistent rhythm, excellent handling of Cantonese/English code-switching |
| `speech-01-turbo` | Fast generation / Prototyping | Lower latency, lower token cost |

---

## Language Boost (`language_boost`)

Helps the acoustic model optimize phonetic synthesis for specific languages:

- `Chinese,Yue`: Optimized for **Cantonese (粵語)**. Accurately pronounces Cantonese colloquialisms and mixed English terms.
- `Chinese`: Standard Mandarin (普通話).
- `English`: Pure English narration.
- `auto`: Automatic multi-language detection.

---

## Pause Tags & Punctuation

You can insert precise pauses directly into the synthesis text:

- `<#0.25#>`: Short breath pause (~250ms). Good for comma pauses.
- `<#0.35#>`: Standard sentence break (~350ms). Recommended after periods (`。`, `!`, `?`).
- `<#0.5#>`: Paragraph transition pause (~500ms).

*Note: Avoid over-chopping single English words with pause tags.*
