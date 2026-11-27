# Beginner mistakes

Each row is a general failure. The two practice flows only show where it was seen. Fix the row that matches the screenshot. Do not switch the user to a different business process.

## Finding and naming actions

| What they see | Cause | Fix |
|---|---|---|
| Search shows one card per connector | The rest are behind 查看詳細資訊 | Open the connector, then pick the action by its full name |
| Word card asks for 內容 and 檔案名稱 | That action creates a file from text | Delete it. Add Populate a Microsoft Word template. The card must ask for 位置, 文件庫, 檔案 |
| Dynamic content has no field they were told to use | The action that produces it is not above this card, or Parse JSON has no schema yet | Move the source action up. On Parse JSON, use 使用樣本產生結構描述 |
| `body('Some_name')` or 無效參考 | The expression names a card that is not above, or the card was renamed | Use the name shown in 程式碼檢視 |
| 儲存草稿 is the only save button | The flow is still a draft | Save, turn the flow on, then copy a trigger URL. The designer page address is not the trigger URL |

## SharePoint and Excel

| What they see | Cause | Fix |
|---|---|---|
| List dropdown is empty or Unauthorized on a site whose URL contains `/contentstorage/` | That site is not a team site | Paste the team site URL with 輸入自訂值 |
| 輸入有效的數字 on a date | The column was imported as a number | Recreate the column as 日期和時間, 包含時間 = 否 |
| 輸入有效的日期時間 | A form date is text | `formatDateTime(pill, 'yyyy-MM-dd')`. The pill comes from Get response details |
| Update item has no Status field | The selected list is the wrong list | Change 列表名稱. 識別碼 is the trigger's 識別碼 |
| Script error `reading 'derRowRange'` or `getTable` is undefined | The range is not an Excel table, or the table name differs | Select the header row plus the data row, 插入 → 表格, set the table name the script uses. The header row must be text, not formulas |
| 此作業正嘗試變更篩選範圍 | An AutoFilter is already on that range | Turn 資料 → 篩選 off, then insert the table |
| Formulas are not allowed in the header row | The selection starts on the formula row | The first selected row must be the plain-text headers |
| 指令碼名稱已被使用 | Office Scripts are stored once per account in OneDrive, not on each sheet | Open the existing script from Office Scripts and replace its code. One script can read every sheet by name |
| Only one column appears when adding a row | The file has no table, or the table has one column | Rename 表格1 to a real name. Add the columns before the flow action |
| Excel dates look like 46265 | The connector returned a serial | `addDays('1899-12-30', int(serial), 'yyyy-MM-dd')` |
| New blank rows appear after a run | Add a row runs even when the key field is empty | Put a condition around the write, or filter those rows out first |

## Conditions, approvals, loops

| What they see | Cause | Fix |
|---|---|---|
| They pressed 核准 and the false branch ran | The condition compares the Chinese button label, or the whole approval action, or a second empty row is included with 以及 | Left value must be that approval's 結果. Right value is `Approve`. If the second row still says 選擇值 on both sides, it is the add-row slot and is not a rule. If it has values, delete that rule from its ⋯ menu |
| A new 選擇值 row appears as soon as the last box is filled | The designer keeps one empty row ready | Leave that empty row. Do not fill it |
| 輸入有效的陣列 on Apply to each | From is typed text | Pick value with the lightning bolt, or an expression that returns an array |
| ActionFailed. No dependent actions succeeded | A child action failed. This message is the parent | Open the child with the red mark |
| The loop fails because one person has no email | Apply to each stops on the first bad item | Filter to rows where the email is not empty before the loop |

## Word, mail, and tests

| What they see | Cause | Fix |
|---|---|---|
| 選取的檔案不含範本元素 | The file has no plain-text content controls, or the action sends the file with no field values | Re-pick the file until the control names appear. Replace typed sample text with pills from the action above. Do not open the template in Word for Mac before upload |
| Attachment content cannot be found | The Word action is not above the mail | Add it above. Attachment content is Microsoft Word 文件. The name includes `.docx`. Two attachments need two names |
| Manual test sits on 請修改清單項目 | The test is waiting for the trigger | Save a change to the list or file the trigger watches. Do it after the test starts |
| The same flow runs twice | The flow updates the item that triggers it | Set a status first so the next run fails the opening condition |

## Practice notes

These are examples of the rows above, not extra workflows to teach.

- Offboarding: Forms → SharePoint list → approval → Excel script → Parse JSON → two Word templates → second approval → mail and checklist. Daily reminder is a third flow.
- Meeting notes: HTTP or a manual run writes Excel tables; a separate daily flow lists open tasks and mails each person. `body('List_meetings')` failed until the action's code name matched. Excel serial dates and empty people rows were the other failures.
