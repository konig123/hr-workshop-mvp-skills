# Scoring

Each candidate: 0–100 per axis. Composite is a weighted average. Rank high to low.

## Default weights

If hiring-requirements includes culture, salary, and company-follower:

| Axis | Weight | What it measures |
|---|---|---|
| JD | 35% | Must-haves, seniority, languages, location/visa, domain (from the JD) |
| Salary | 30% | Likelihood they can accept the stated cash band (inferred) |
| Culture | 20% | Tech / startup vs corporate, as written in hiring-requirements |
| Follower | 15% | Proxy for following the hiring company on LinkedIn |

If an axis is **absent** from hiring-requirements, drop it and renormalise remaining weights to 100%. JD never drops below 35%. Extra named filters (e.g. “Mandarin required”) fold into **JD**, not a fifth axis, unless the user names them as a separate score.

## Axis rubrics

### JD

Score evidence vs must-haves. Typical deductions:

- Seniority far below the posted title (e.g. Assistant Manager vs Head of Global): cap at 55 unless hiring-requirements says stretch is OK
- Missing required language: −15 to −25
- Wrong location / needs visa when JD forbids it: −20
- Nice-to-have present (e.g. crypto): +5 to +10, not a substitute for must-haves

### Culture

High: current or recent high-growth tech, crypto, startup, scale-up.  
Mid: digital bank / fintech corporate.  
Low: airline, real estate, traditional bank HQ with no tech stint.

### Salary (inferred)

Map posted cash to a public market band (cite year + source, e.g. Robert Half HK). Then:

- Title/scope clearly inside the band: 75–90
- One level above the band (possible with equity/token): 45–60
- Head/VP at a large global firm vs Manager cash: 20–35
- Too junior for the JD but inside cash: high salary, low JD — keep both honest

Never write a candidate’s actual pay. Label the column **Salary (inferred)**.

### Follower (proxy only)

Public web cannot list company-page followers. Proxy:

| Proxy | Score |
|---|---|
| Current employee at a direct competitor in the same product/market | 80 |
| Current employee at adjacent Web3 / same-city crypto | 70 |
| Ex-competitor or hiring-company alumni now elsewhere | 55 |
| Same-city tech, not the same industry | 40 |
| Traditional industry, no public tie | 25 |

Label the column **Follower (proxy)**. Put this Recruiter Boolean on the canvas (swap company name):

```
Follows:[Hiring Company] AND
(title:compensation OR title:rewards OR title:"C&B" OR title:"total rewards") AND
(geo:Hong Kong OR geo:Singapore)
```

Adjust geo/title from the locked files.

## Shortlist rules

- Default N = 10
- Exclude current employees of the hiring company; list them as excluded
- If JD-fit Heads and band-fit Managers are different pools, keep a mix and warn in a callout
- One-line **why** + one-line **risk** per person
- Language field: Confirmed / Likely / Possible / Unconfirmed — never guess from a photo
