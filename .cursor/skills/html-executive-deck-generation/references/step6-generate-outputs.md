# Step 6 ? Generate Outputs (HTML + Gamma + Kimi)

**Input:** Deck Build Brief from Step 5.

Produce **three files**. Same storyline and numbers in all three.

---

## 6A ? HTML deck

### Before writing

1. Read DAYMARK visual guide (paint is locked)
2. Read Deck Build Brief ? especially **?? per slide** (Step 5 Part B)
3. Read [layout-contract.md](layout-contract.md) for the slide engine only

### Build rules

| What | Approach |
|------|----------|
| Paint | Always DAYMARK tokens + logos unless user said replace DAYMARK |
| ?? | Step 5 Part B if a layout reference was used; else Step 4 Part B |
| Engine | layout-contract (nav, 1280�720, print). Do not copy reference CSS colors |
| HR fallback | Only if user confirmed the HRBP HTML clone |

Constraints: 1280�720, UTF-8, no emoji, SVG icons, print-safe KPIs, inline CSS+JS.

### Output

`{topic}_deck.html` beside input or user folder.

### Verify

Run [verification-checklist.md](verification-checklist.md).

---

## 6B ? Gamma prompt

1. Read [gamma-prompt-template.md](gamma-prompt-template.md)
2. Fill from Deck Build Brief (DAYMARK paint + Step 5 ??)
3. Write `{topic}_gamma_prompt.md`

---

## 6C ? Kimi AI prompt

1. Read [kimi-prompt-template.md](kimi-prompt-template.md)
2. Fill from Deck Build Brief
3. Write `{topic}_kimi_prompt.md`

---

## Deliver to user

```markdown
## Deck complete

| Output | Path |
|--------|------|
| HTML (open in browser) | ... |
| Gamma prompt | ... |
| Kimi prompt | ... |

**Story:** [2 sentences]
**HTML verification:** PASS / FAIL
**Next steps:**
1. Open HTML locally or share file
2. Paste gamma_prompt into gamma.app
3. Paste kimi_prompt into Kimi slide generator
```

If HTML verification FAIL, still deliver Gamma/Kimi prompts but flag HTML issues.
