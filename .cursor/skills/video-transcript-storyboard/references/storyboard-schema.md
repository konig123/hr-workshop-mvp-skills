# Storyboard Scene JSON

Use this shape as input to `scripts/build_storyboard_html.py`.

The example uses escaped Unicode for Traditional Chinese. That is intentional: it prevents lossy writes from turning CJK text into question marks.

```json
{
  "meta": {
    "title": {
      "en": "Example Employee Onboarding Video - Storyboard",
      "zh": "\u54e1\u5de5\u5165\u8077\u5f71\u7247\u7bc4\u4f8b - \u5206\u93e1\u8868"
    },
    "source": "https://www.youtube.com/watch?v=...",
    "duration": "3:38",
    "notes": "Transcript from YouTube; timings estimated."
  },
  "scenes": [
    {
      "id": 1,
      "time": "0-12 sec",
      "en": {
        "goal": "Welcome and set context",
        "narration": "Original or edited English voiceover.",
        "ttsScript": "Exact MiniMax T2A text after rewrites and pause tags. Empty if not Yue/MiniMax.",
        "visual": "Visual direction for the scene.",
        "onScreen": "Text shown in the video.",
        "asset": "welcome-title-card.png",
        "risk": "Production, privacy, or accuracy check."
      },
      "zh": {
        "goal": "\u6b61\u8fce\u65b0\u4eba\u4e26\u8aaa\u660e\u5f71\u7247\u76ee\u7684",
        "narration": "\u7e41\u9ad4\u4e2d\u6587\u65c1\u767d\u3002",
        "ttsScript": "",
        "visual": "\u7e41\u9ad4\u4e2d\u6587\u756b\u9762\u6307\u793a\u3002",
        "onScreen": "\u87a2\u5e55\u6587\u5b57\u3002",
        "asset": "welcome-title-card.png",
        "risk": "\u98a8\u96aa\u6aa2\u67e5\u3002"
      }
    }
  ]
}
```

## Field Rules

| Field | Rule |
|---|---|
| `id` | Stable scene number; keep aligned across languages. |
| `time` | Use exact captions if available; otherwise estimated range. |
| `goal` | Scene purpose in one short phrase. |
| `narration` | Keep transcript-backed; do not invent missing content. Human-readable VO. |
| `ttsScript` | Exact MiniMax T2A `text` (after `text_rewrites` + pauses). Column **MiniMax TTS**. Empty when not using MiniMax Yue. |
| `visual` | Describe what Descript or an editor should create. |
| `onScreen` | Short text overlays only. |
| `asset` | Filename(s), screenshot names, or placeholder asset names. |
| `risk` | Accuracy, privacy, compliance, credential, or localization checks. |

## Descript Prompt Requirements

The generator creates the prompt column automatically from the fields above. Make each field specific enough that the prompt can stand alone when pasted into Descript.
