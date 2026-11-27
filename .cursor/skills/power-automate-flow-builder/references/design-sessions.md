# Design sessions (thinking process)

Teach this **before** naming connectors. A cloud flow is seven sessions. Not every flow uses all seven. Email is only one possible **Act**.

| # | Session | Question | Typical real nodes |
|---|---|---|---|
| 1 | **Trigger** | What starts it? | Recurrence; Manually trigger a flow; When a row is added (Excel); When an item is created (SharePoint); When a new email arrives (Outlook); When a response is submitted (Forms); When a new chat message is added (Teams) |
| 2 | **Collect** | Where is the data? | List rows present in a table; Get items; Get file content; Get email; Get response details; HTTP GET; Run script (Office Scripts — Excel **transform** only) |
| 3 | **Shape** | One item or many? Clean fields? | Apply to each / 套用至各項; Filter array; Select; Compose / 撰寫; Parse JSON / 剖析 JSON; Create HTML table |
| 4 | **Decide** | Branch or wait for a person? | Condition / 條件; Switch; Do until; Start and wait for an approval |
| 5 | **Act** | What should the system **do**? | Draft/send email; Post message in Teams; Create/update SharePoint item; Create file; Create calendar event; HTTP POST (Premium API / DeepSeek); AI Builder — Create text with GPT |
| 6 | **Record** | How do we not do it twice? | Update a row; Update item; Move file; Set variable |
| 7 | **Guard** | Fail, empty, timezone | Terminate; Configure run after; Scope; Condition on `length(...) = 0` |

## How to choose a trigger

| User says | Session 1 |
|---|---|
| Every morning / every Monday | Recurrence (set **time zone**, not only clock time) |
| I click Run | Manually trigger a flow (good for class tests) |
| When someone fills a form | Forms — When a new response is submitted |
| When a list/Excel row appears | SharePoint / Excel **When a row is added** (Excel trigger is picky; Recurrence + List rows is often more reliable) |
| When mail arrives | Outlook — When a new email arrives (V3) |

## Shape vs Decide

- **Filter array** (session 3) = shrink the list **before** the loop (cleaner).
- **Condition inside Apply to each** (session 4) = Copilot’s default; OK if True holds Act + Record and False is empty.
- Do not put **更新列** outside the loop if each row has its own result.

## Act is not always mail

Examples of Act without Outlook:

- Post to a Teams channel
- Create a Planner task
- Create a SharePoint list item
- Write a row into another Excel table
- Call an HTTP API
- Generate text with AI Builder then **store** it (SharePoint / Excel), no mail

## Record after Act

Stamp status **only after** the Act succeeded (same as `Draft Saved` after 草擬). If Record runs before Act, retries skip work that never happened.

## AI’s place

- **Session 5 (optional):** model writes text or classifies **one** item already in the loop.
- **Not session 1–2:** do not ask the model to “read the whole spreadsheet.”
- **Not Copilot Create:** Copilot is a weak session-1–3 scaffolder for popular connectors only.
