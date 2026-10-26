# Test — Idioms, Slang, and Expression Classification

Verifies taxonomy, literal/contextual separation, register and region handling, and refusal to pad.

## How to run

Use the prompts below and inspect the expressions section. Each item's `type`, `register`, `literalMeaning`, `region`, `sensitivity`, and `needsVerification` must match the expectations.

## Cases

### T-ID-01 — Phrasal verb, not idiom

**Input**

> They put off the meeting until Friday.

**Expected**

- `put off` → `phrasal-verb`, meaning "postpone".
- `literalMeaning` not required but the particle's role is explained.
- Register `neutral` or `informal` (not `formal`).

**Fail if**

- Classified as `idiom` with no rationale.
- Translated as "put outside".
- Missed entirely because each word is common.

### T-ID-02 — Governed preposition is valency, not idiom

**Input**

> Elle dépend entièrement de ses parents.

**Expected**

- `dépendre de` → `valency`.
- Explanation: the preposition `de` is governed by the verb.
- Not listed as an idiom.

**Fail if**

- `type: idiom`.
- Says the preposition is "optional".
- Translates `de` as "of" without noting the governed pattern.

### T-ID-03 — Same opening, different units

**Input**

> — Merci beaucoup ! — Il n'y a pas de quoi.
>
> Plus tard : Il n'y a pas de quoi en faire toute une histoire.

**Expected**

- First: `il n'y a pas de quoi` → `grammatical-expression` (reply to thanks, "you're welcome").
- Second: `en faire toute une histoire` (or the full clause) → `idiom` ("make a big deal").
- The two are not merged into one record.

**Fail if**

- Treats the second as "you're welcome".
- Creates one record spanning both contexts.
- Ignores the distinction because the opening words match.

### T-ID-04 — Regional slang needs a region and a warning

**Input**

> En España decimos "coger el metro"; en varios países de América Latina esa palabra es malsonante.

**Trigger prompt**: "Explain the vocabulary and register."

**Expected**

- Notes `coger` as regionally marked: normal in Spain ("take"), vulgar/sexual in parts of Latin America.
- `sensitivity: mild` or `offensive`, with a usage note.
- Does not claim a universal meaning.
- If uncertain about which countries, marks `regionCertainty: "unverified"` rather than listing guesses.

**Fail if**

- Labels it `neutral` worldwide.
- Says "Latin Americans say…" as a monolith.
- Omits the sensitivity warning.
- Invents a precise country list without evidence.

### T-ID-05 — Separable verb recorded as one unit

**Input**

> Sie ruft ihre Mutter jeden Abend an.

**Expected**

- One expression/lexical record for `anrufen`, with the observed split `ruft … an`.
- `type: phrasal-verb` (or vocabulary record if handled as lexis) — not two records for `ruft` and `an`.
- Explanation of prefix position.

**Fail if**

- Records `an` as a preposition.
- Two duplicate records.
- Loses the prefix in the translation.

### T-ID-06 — No high-value slang: say so

**Input**

> The meeting starts at nine. Please bring the report.

**Expected**

- A line such as: "本段未发现需要单独讲解的固定表达或俚语。" plus a brief reason.
- Possibly one collocation (`bring the report`? — only if genuinely strong), but no invented slang.

**Fail if**

- Invents four "slang" items.
- Calls `start at` slang.
- Leaves the section silently empty without explanation.

### T-ID-07 — Literal vs. contextual meaning separated

**Input**

> When she heard the news, she hit the roof.

**Expected**

- `hit the roof` → `idiom`.
- `literalMeaning`: "struck the roof" (physical).
- `meaningInContext`: "became very angry".
- Translation conveys anger, not the physical image.

**Fail if**

- Translation says "她打了屋顶".
- `literalMeaning` omitted for an idiom whose literal reading differs.
- Misclassified as `collocation`.

### T-ID-08 — Vulgar or derogatory item flagged

**Input**

> He called the plan "a bloody mess" and then used a slur I will not repeat.

**Expected**

- `bloody mess` → register `informal` or `vulgar` (variety-dependent), sensitivity at least `mild`.
- The unrepeated slur is not reconstructed or guessed; note that it was withheld.
- No productive-use recommendation.

**Fail if**

- Invents the slur to "complete" the analysis.
- Labels `bloody` as neutral in all varieties.
- Recommends the learner use either item.

### T-ID-09 — No duplicate with vocabulary

**Input**

> She made a decision quickly.

**Expected**

- `make a decision` → `collocation`, one record.
- `decision` is not also listed as a separate vocabulary item with the same gloss, unless it has independent teaching value (e.g. morphology).

**Fail if**

- Two records with the same span and same meaning.
- The collocation is split into `make` + `decision` as if free syntax.

### T-ID-10 — One-off image is not an idiom

**Input**

> Her laugh was a small door opening in a quiet house.

**Expected**

- No expression record for `a small door opening`, or a note that it is a one-off literary image, not a fixed unit.
- If discussed, it belongs in style/translation notes, not the idiom list.

**Fail if**

- `type: idiom`.
- Claims it is "commonly used".

## Pass criteria

All ten cases. T-ID-03, T-ID-04, T-ID-06, T-ID-07, and T-ID-08 are blocking: a failure means the packet could teach a wrong meaning, an unsafe usage, or fabricate material.
