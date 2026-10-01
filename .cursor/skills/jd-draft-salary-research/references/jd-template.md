# Ashby-style JD template

Emit exactly this structure (fill brackets; drop a section only if the user asked to omit it).

```text
**{Role Title} @ {Company}**

**Location:** {City or Remote}
**Team / Department:** {Team}
**Employment type:** {Full-time | Contract | …}
**Compensation:** {e.g. $250K – $445K · Offers Equity}   ← or [Compensation TBD]

---

{Optional one-liner, e.g. By applying to this role, you will be considered for {Role} roles across {scope}.}

**About the Role**

{2–4 paragraphs: what they build/own, why the role matters, scale/context.}

**We expect you to:**

- {Must-have 1}
- {Must-have 2}
- {Must-have 3}

**Nice to have:**

- {Nice-to-have 1}
- {Nice-to-have 2}

**About {Company}**

{2–4 sentences: mission, what the company builds, why people join.}

We are an equal opportunity employer and do not discriminate on the basis of race, religion, color, national origin, sex, sexual orientation, gender identity, age, veteran status, disability, genetic information, or any other applicable legally protected characteristic.

{Optional: link to company EEO / privacy policy if provided.}

{Optional closing line: mission / “join us” sentence.}

---

**Compensation & benefits note**

The base pay offered may vary depending on multiple individualized factors, including market location, job-related knowledge, skills, and experience. In addition to the salary range listed above, total compensation may include equity and/or performance-related bonus(es) for eligible employees{, and the following benefits:}.

{If benefits known, bullet list:}
- {Benefit}
- {Benefit}

More details about compensation and benefits are available to candidates during the hiring process.
```

## Heading labels (locked)

Use these exact bold labels:

- `About the Role`
- `We expect you to:`
- `Nice to have:`
- `About {Company}`
- `Compensation & benefits note`

## Reference shape (OpenAI Research Engineer — structure only)

Metadata → optional apply note → About the Role → We expect you to → Nice to have → About Company → short EEO → optional mission close → Compensation & benefits note.

Do not reproduce OpenAI’s long jurisdiction-specific legal paragraphs unless the user supplies equivalent legal copy for their company.
