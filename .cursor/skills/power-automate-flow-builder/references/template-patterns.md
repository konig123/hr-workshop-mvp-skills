# Gallery patterns (reference, not a closed list)

Microsoft’s template gallery (`make.powerautomate.com` → **Templates**) is searched by phrase or category. Templates are **starting graphs** of real connectors. Tweak by adding/removing actions. If no template fits, build from blank using sessions.

When suggesting a template, give a **search phrase** the student can type in 範本. Confirm the graph still uses catalog actions.

## Recurring gallery shapes

| Student idea (any domain) | Gallery search (EN) | Spine |
|---|---|---|
| Something from Excel then notify | `Send an email from Excel`, `Excel Outlook` | List rows → Apply to each → Outlook / Teams |
| New SharePoint item → approval | `approval when new item is added` | When item created → Start and wait for approval → Condition → Update item / email |
| Form submitted → notify | `Microsoft Forms` `Teams` / `email` | Forms trigger → Get response details → Teams or Outlook |
| Manager email → chat ping | `Slack when my manager emails` / Teams equivalent | When email arrives → Condition → Post message |
| Save mail attachment | `Save email attachments to OneDrive` | When email arrives → Get attachment → Create file |
| Recurring reminder from a list | `scheduled` `SharePoint` `email` | Recurrence → Get items → Filter/loop → Act |
| Excel selected row | `Send an email for a selected row` | Instant on one row — **not** a daily batch |

Onboarding / “new hire” gallery templates often **create Entra ID users, Teams, approvals, Send email**. Too heavy if the student only wanted a **draft** from Excel. Prefer the Excel→Outlook **mail-merge** shape, then swap Send → 草擬 and add 更新列.

## How to use a template in class

1. Search gallery → Create → bind connections.  
2. Immediately check: Send vs Draft; Recurrence timezone; Excel **Table**.  
3. Then **adapt** with this skill (add HTTP, status column, Filter).  

Importing **your** solution zip is the same idea: working graph, then bind OneDrive + keys. The skill still maps **their** next idea onto sessions — it does not only clone onboarding email.

## Copilot vs template vs blank

| Path | Use |
|---|---|
| Template / imported solution | Fast Standard connectors; student sees a real graph |
| Copilot Create | Short prompt; Recurrence + Excel + Outlook + loop only |
| Blank | HTTP, Parse JSON, Office Script, custom `fx` — always hand-add |

Sources to re-check if the gallery moves: [Get started from a template](https://learn.microsoft.com/en-us/power-automate/get-started-logic-template), [Cloud flows overview](https://learn.microsoft.com/en-us/power-automate/overview-cloud).
