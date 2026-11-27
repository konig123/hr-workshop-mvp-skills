# Teach any Power Automate flow

Use this for a beginner who states a goal, or who pastes a designer screenshot. The goal can be anything. Do not rebuild the offboarding flow or the meeting-notes flow unless that is the goal they just stated.

Answer one screen at a time. The beginner is looking at the designer, not reading a manual.

## First reply

Restate the goal in one sentence, then only these decisions:

1. **Start.** What event starts the flow: a form, a list or file change, a schedule, a button, or an incoming HTTP call?
2. **Data home.** Excel table, SharePoint list, or the body of the trigger? A sheet range is not a table. A document library is not a list.
3. **Human gate.** Which step must a person approve before mail is sent or a record is written?
4. **Do it once.** Which column or flag stops the same item running again?
5. **How many flows.** Split when one flow would both wait for a person and run on a clock. A daily reminder is its own flow. The intake flow still runs without it.

Then name the first action only: connector, exact action, and where it sits. Stop. Ask them to add that action and send the card.

## Each later reply

For the one card they show:

1. Say whether this action is the right one for this step.
2. Search text, in English and in the UI language.
3. The exact card to click when several cards match. Same connector often has several actions.
4. Every required field: dropdown, dynamic-content pill, or typed text. Say which earlier action the pill comes from. Pills only exist for actions above this card.
5. What the card looks like when it is filled correctly.
6. Stop. Do not preview the rest of the flow unless they ask what is left.

## Choose an action

Map the step onto the seven sessions in [design-sessions.md](design-sessions.md), then pick a catalog action. If the catalog and the screenshot disagree, trust the screenshot and say the name you expected is not the card they opened.

| They need | Choose | Do not choose |
|---|---|---|
| Run when a form is submitted | When a new response is submitted, then Get response details | The trigger alone. It only has the response id |
| Run when a list row changes | When an item is created or modified | A file trigger on the document library |
| Run every morning | Recurrence, interval 1 day, time zone set | A clock time with the zone left on UTC |
| Accept a JSON post from another system | When an HTTP request is received | The browser address of the designer |
| Read many Excel rows | List rows present in a table | List rows on a plain range |
| Write calculated inputs and read one result row | Run script, then Parse JSON | Typing the formula into the flow |
| Fill a Word file from fields | Word Online (Business) → Populate a Microsoft Word template | Create a Word document from content, or a third-party Word connector |
| Wait for a yes or no | Start and wait for an approval → Approve/Reject - First to respond | A condition that compares the button label |
| Send a file | Send an email (V2), attachment content = the file action's output | A SharePoint link pasted into the body |
| One row per task | Create item or Add a row, once per task | One field with several titles joined by commas |
| Remind until someone is done | A second flow: Recurrence → Get items or List rows with a filter → Apply to each → email | The same flow that already waited for approval |

## Parameters

- **Dropdown:** site, list, library, file, form, script name, approval type.
- **Pill:** a field from an action above. Click the lightning bolt. Do not type the field's display name.
- **Typed text:** only fixed words the flow must match later, such as a status value or `Approve`.
- **Expression:** the value is an array, a date conversion, or a property the pill list does not show. The token must be purple. Grey text in the box is still a string.
- `body('Action_name')` uses the action's name in code view. Spaces become underscores. Renaming the card changes the name.

## After they say it runs

Tell them the human action that moves the flow forward: submit the form, save the list row, or press the approval button. Then say what they should see. A manual test of an automatic trigger waits until that event happens. A waiting test screen is not a crash.

A green check on the false branch means the condition was false. Open the condition in that run and read the two values it compared.
