# Survey structure (standard 20-Q CSV)

## Columns

| Column | Role |
|--------|------|
| `EmpID` | Respondent id (optional for scoring) |
| `Department` | Org slice (optional) |
| `Manager` | People leader (group key) |
| `Q1_Manager_Leadership` … `Q10_Manager_Leadership` | Direct Leader pillar |
| `Q11_DeptHead_Vision`, `Q12_DeptHead_Strategy`, `Q13_DeptHead_Accessibility` | Dept head / senior leadership |
| `Q14_Team_Goal_Clarity`, `Q15_Team_Collaboration`, `Q16_Team_Resources`, `Q17_Team_Efficiency` | Team support / infrastructure |
| `Q18_Engagement_Pride`, `Q19_Engagement_Retention`, `Q20_Engagement_Referral` | Engagement |

Scale: **1–5** (higher = better). No open-text column in the standard extract — section VII notes silence.

## Score definitions

| Metric | Formula |
|--------|---------|
| Direct Leader / pillar | mean Q1–Q10 |
| Overall / blended | mean Q1–Q20 |
| Dept head | mean Q11–Q13 |
| Team support | mean Q14–Q17 |
| Engagement | mean Q18–Q20 |
| Workload proxy | mean(Q16, Q17) |
| Mood proxy | mean Q18–Q20 |
| Team atmosphere | mean(Q14, Q15) |
| Pressure composite | mean(workload, mood, atmosphere) |

## Thresholds

| Signal | Threshold |
|--------|-----------|
| Pressure / shared danger proxy | composite or team-support &lt; **4.15** |
| Team-support crisis (alt) | team-support &lt; **3.0** |
| Q16 resources crisis | team avg &lt; **2.5** |
| Q13 accessibility concern | team avg &lt; **3.5** |
| Gap note (shared drag) | Direct − Overall &gt; **0.15** |
| Gap note (balanced) | \|Direct − Overall\| &lt; **0.05** |

Pressure alert labels: Danger &lt;4.15 · Caution 4.15–4.50 · Watch 4.50–4.65 · Normal 4.65–4.75 · Optimal &gt;4.75.
