# Parameters, `fx`, and debug

## 動態內容 vs 運算式

| You see | Do |
|---|---|
| Named pill (`email`, `subject`) | Click it — no `fx` |
| Only **目前的項目** | 運算式: `items('Apply_to_each')?['employeeId']` (use loop `"name"`) |
| Nested `result.joiners` | 運算式: `body('Run_script')?['result']?['joiners']` or `json(body('Run_script')?['result'])?['joiners']` |
| Grey/black formula text in the box | Still a **string**. Delete → 運算式 → 確定 → **purple token** |
| 程式碼檢視 without `@` | Need `@body('…')` in code view |

`Run_script` is the **action name**, not the Office Script `GetTodaysJoiners`. 程式碼檢視 `"name"`; spaces → underscores.

## Apply to each — 輸入有效的陣列

Cause: From is text, not an array expression. Fix via 運算式. Designer does **not** need a previous run.

HTTP that uses `items('Apply_to_each')` must sit **inside** that loop, and the loop **name** must exist (`InvalidTemplate` / `HTTP_1` referenced `Apply_to_each`).

## Parse JSON

- **使用樣本產生結構描述** = button on the Parse JSON card, not a node.
- OpenAI/DeepSeek: first parse = wrapper (`choices`); `content` is a **string**. Second parse **or 撰寫**: `json(body('FIRST_CARD_NAME')?['choices'][0]?['message']?['content'])`.
- Second card must **not** `body('its_own_name')` (self-reference / 無效參考).
- Extra fields (`logprobs`, `system_fingerprint`) break strict schemas → prefer 撰寫 + `json(...)` on `content`.
- HTTP action often named `HTTP_1` → `body('HTTP_1')`, not `body('HTTP')`.

## Excel 更新列

- 金鑰值 = current row id via 運算式, **not** the status text `Draft Saved`.
- Welcome Email Sent / Sent Date = **進階參數 → 顯示全部**.
- Record **after** Act, inside the loop.
- Open the **OneDrive** file in Excel for the web after a green run (desktop cache lies).

## Copilot

無流程建議: prompt named HTTP/DeepSeek/Parse JSON. Shorten to Recurrence + Excel + Outlook + loop.

## HTTP

Queries empty unless the API documents query params. Cookie empty. Auth: header `Authorization: Bearer …` or 進階 Authentication. Body JSON with `@{items('LoopName')?['field']}` as **expressions**, not labels like `Parse JSON subject`.

## Import solution

Flow appears as its **display name** (e.g. `onboard_test`), type 雲端流程. Click that row. `?` on Excel/Outlook = bind **連接參考**. Zip has no spreadsheet, script, or API key.
