# Real nodes (allow-list)

Recommend **only** these (or Microsoft Learn connector pages you just fetched). English = designer search. 中文 = typical Traditional Chinese UI.

## Built-in / Control / Data / Schedule

| Search | 中文 UI (common) | Session | Notes |
|---|---|---|---|
| Recurrence | Recurrence | 1 | Time zone e.g. `(UTC+08:00) Hong Kong SAR` |
| Manually trigger a flow | 手動觸發流程 | 1 | Class test |
| Apply to each | 套用至各項 / Foreach | 3 | From must be an **array** via 運算式 |
| Condition | 條件 | 4 | Top combinator 以及 vs 或 |
| Switch | 開關 | 4 | |
| Do until | 執行直到 | 4 | |
| Terminate | 終止 | 7 | |
| Scope | 範圍 | 7 | |
| Filter array | 過濾陣列 | 3 | |
| Select | 選取 | 3 | |
| Compose | 撰寫 | 3 | Good substitute for a second Parse JSON |
| Parse JSON | 剖析 JSON | 3 | Schema required; 使用樣本產生結構描述 is a **link**, not a node |
| Create HTML table | 建立 HTML 表格 | 3 | |
| Join | 聯結 | 3 | |
| HTTP | HTTP | 2/5 | **Premium**. Method/URI/Headers/Body. Queries often empty |

## Excel Online (Business) — OneDrive / SharePoint

File must be a **Table** (Insert → Table). Personal Excel Online (OneDrive consumer) is a different connector.

| Search | 中文 UI | Session |
|---|---|---|
| List rows present in a table | 列出表格中的列 | 2 |
| Get a row | 取得列 | 2 |
| Add a row into a table | 將一列新增到表格 | 5 |
| Update a row | 更新列 | 6 |
| Delete a row | 刪除列 | 6 |
| Get tables | 取得表格 | 2 |
| Run script | 在 Excel 中執行指令碼 | 2/3 |
| Create table | 建立表格 | 2 |

Update a row: Key Column + 金鑰值 (運算式 into `employeeId` etc.). Extra columns under **進階參數 → 顯示全部**. Blank columns are left unchanged.

## Office 365 Outlook (not Outlook.com unless they only have consumer)

| Search | 中文 UI | Session | Careful |
|---|---|---|---|
| Draft an email message | **草擬電子郵件訊息** | 5 | Human review |
| Send an email (V2) | 傳送電子郵件 (V2) | 5 | Sends now |
| Send a draft message | 傳送草稿訊息 | 5 | Sends an **existing** draft — not create |
| When a new email arrives (V3) | 當新電子郵件送達時 | 1 | |
| Get emails (V3) | 取得電子郵件 | 2 | |
| Create event (V4) | 建立事件 (V4) | 5 | Calendar |
| Flag email | (varies) | 5 | |

## SharePoint

| Search | Session |
|---|---|
| When an item is created | 1 |
| When an item is created or modified | 1 |
| Get items | 2 |
| Create item | 5 |
| Update item | 6 |
| Get file content | 2 |
| Create file | 5 |
| Send an HTTP request to SharePoint | 5 |

## Microsoft Forms / Teams / Approvals / AI Builder

| Search | Session | Notes |
|---|---|---|
| When a new response is submitted | 1 | Forms |
| Get response details | 2 | Forms |
| Post message in a chat or channel | 5 | Teams |
| Post adaptive card | 5 | Teams |
| Start and wait for an approval | 4 | Approvals |
| Create text with GPT / Run a prompt | 5 | AI Builder; Microsoft models, **not** DeepSeek |

## Office Scripts

Excel **自動化** scripts: tables, ranges, `fetch` sometimes. **Cannot** create Outlook drafts, Recurrence, or store secrets well. Use **Run script** to return JSON (`joiners`), then loop in Power Automate. Not a VBA replacement for the whole flow.

## Do not recommend (or only after Learn check)

- Fake nodes: “Filter onboarding today”, “DeepSeek connector”, “Create a draft (V3)” as the search string in 中文 tenants (use **草擬電子郵件訊息**).
- **使用樣本產生結構描述** as an action.
- Gmail / Google Drive in an M365-only workplace unless they have those connectors.
- Desktop **Pad** / UI flows unless they asked for Power Automate **Desktop**.
