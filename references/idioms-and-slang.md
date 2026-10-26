# Idioms, Collocations, and Slang

Classification drives everything downstream: translation, register warning, exercise design. A wrong label teaches the wrong thing.

## Contents

1. [Taxonomy](#1-taxonomy)
2. [Decision procedure](#2-decision-procedure)
3. [Register labels](#3-register-labels)
4. [Regional claims](#4-regional-claims)
5. [Sensitivity](#5-sensitivity)
6. [Extraction threshold](#6-extraction-threshold)
7. [Worked contrasts](#7-worked-contrasts)
8. [Language notes](#8-language-notes)
9. [Common misclassifications](#9-common-misclassifications)

## 1. Taxonomy

| Type | Definition | Test |
|---|---|---|
| `collocation` | Words that habitually co-occur; meaning is compositional but the combination is preferred | Native speakers expect the partner; substituting a synonym sounds odd |
| `phrasal-verb` | Verb + particle with a meaning not fully predictable from the parts (English; German separable verbs when idiomatic) | Removing the particle changes or destroys the meaning |
| `idiom` | Fixed multi-word unit whose meaning is not derivable compositionally | Literal reading ≠ intended meaning |
| `colloquialism` | Everyday spoken expression, not slang, not regional | Standard vocabulary, informal register |
| `slang` | Informal vocabulary specific to a group/era, often short-lived, often in-group | Not in neutral dictionaries as standard; currency is time- and group-bound |
| `valency` | A verb/adjective/noun's required or preferred complement pattern | The preposition/case is governed, not chosen (`depender de`, `warten auf` + Akk.) |
| `grammatical-expression` | Fixed grammatical frame with a slot (`il n'y a qu'à + inf`, `no es que + subj.`) | Meaning is procedural/grammatical, not lexical |

Borderline calls go to the **more conservative** label. A colloquialism called slang is less harmful than slang called neutral.

## 2. Decision procedure

Ask in order:

1. **Is it one word?** → vocabulary record, not expression (unless it is a separable verb whose particle is split in the sentence — then it is still one lexical unit; record it with the observed surface and note the split).
2. **Is the meaning compositional?**
   - Yes → is the combination strongly preferred? `collocation`. Otherwise it is just syntax, not an expression.
   - No → go to 3.
3. **Is there a required grammatical complement?** → `valency` (or `grammatical-expression` if the frame carries a construction, e.g. subjunctive trigger).
4. **Is the unit fixed as a whole (can't substitute freely)?**
   - Yes, and literal ≠ intended → `idiom`.
   - Yes, and it is a verb + particle → `phrasal-verb`.
5. **Is it informal but standard?** → `colloquialism`.
6. **Is it group/time-bound non-standard vocabulary?** → `slang`.

If two labels genuinely apply (a slang idiom), choose the dominant teaching need and record the secondary label in `notes`. Do not create two records for the same string.

## 3. Register labels

| Label | Meaning | Example context |
|---|---|---|
| `formal` | Official, academic, ceremonial | `il convient de`, `es menester` |
| `neutral` | Standard, usable anywhere | `faire une erreur` |
| `informal` | Relaxed standard speech/writing | `ça marche`, `no pasa nada` |
| `colloquial` | Clearly spoken-register, may be inappropriate in writing | `kriegen`, `pillar` (Spain) |
| `vulgar` | Profanity or crude reference | flag with sensitivity |
| `literary` | Marked for literary prose/poetry | `yonder`, `les sanglots longs` |
| `archaic` | No longer current except in fixed phrases | `thou`, `point n'est besoin` |
| `mixed` | The expression spans registers, or the register is uncertain | explain in `notes` |

Every expression gets a register. "It depends" is not a register label; use `mixed` and explain.

## 4. Regional claims

Only assign `region` when you have a reason:

- The source itself is regional (Québec press, Argentine dialogue, Austrian signage).
- The item is a well-known regionalism (`coger` in Spain vs. taboo in much of Latin America; `vos` in Argentina; `heuer` in Austria).
- A dictionary you can cite marks it regional.

Otherwise omit `region` and set `regionCertainty: "unverified"` if you nonetheless mention it. Never turn one author's usage into "French people say". Never assert that a slang term is "used everywhere" — that claim requires evidence you usually do not have.

When a term is regionally restricted and potentially problematic elsewhere, say both facts: where it is normal, and where it is not.

## 5. Sensitivity

Set `sensitivity`:

- `none` — ordinary material.
- `mild` — mildly crude, insulting in some contexts, or socially risky.
- `offensive` — derogatory, sexual, or strongly profane.
- `slur` — group-directed derogatory term.

For anything above `none`, add a `usageNotes` line naming the constraint (who may use it, in what company, what it becomes in another region). Do not launder it, and do not recommend the learner use it productively.

## 6. Extraction threshold

Include an expression when **at least one** holds:

- Its meaning is non-compositional and a learner would misread it.
- Its collocation is strong enough that a synonym would sound foreign.
- Its register or region would cause a social error if misused.
- It is a valency pattern the learner will need to produce correct sentences.

Exclude when:

- It is ordinary syntax (`in the morning`, `dans la rue`).
- It is a transparent compound whose parts are already glossed.
- It is a one-off poetic image, not a fixed expression.
- Including it would duplicate a vocabulary record.

**If nothing qualifies, write the sentence.** Example output line:

> 表达与俚语：本段未发现需要单独讲解的固定表达或俚语；`prendre le train` 等为普通动宾搭配。

This is a correct, expected result. Padding the section to look thorough is a defect.

Target counts (guidance, not quotas): 2–8 expressions for a 5–10 sentence text; more only if the text is idiom-dense.

## 7. Worked contrasts

**English**
- `cobble together` — phrasal verb: assemble hastily from available parts. Not an idiom (particle carries the "improvise" sense) and not a collocation (meaning shifts).
- `on first-name terms` — idiom: familiar enough to use first names. Literal reading is possible but not the point.
- `make a decision` — collocation. Compositional; `do a decision` is the learner error.
- `depend on` — valency. The preposition is governed.

**French**
- `tant bien que mal` — idiom/ adverbial fixed expression: "just barely, with difficulty".
- `en faire toute une histoire` — idiom: make a big deal of it. Literal "make a whole story of it".
- `avoir besoin de` — valency + fixed frame; `de` is governed.
- `il n'y a pas de quoi` — grammatical fixed expression (response to thanks); but `il n'y a pas de quoi en faire une histoire` is the idiom "no need to make a fuss". Same opening, different unit — record the actual span.

**Spanish**
- `para colmo` — idiom/discourse marker: "to top it all off".
- `por si acaso` — fixed adverbial: "just in case".
- `deber de + inf` — grammatical expression (probability) vs. `deber + inf` (obligation). The distinction is the teaching point.
- `se me cayó` — grammatical expression (accidental `se`), not a lexical idiom.

**German**
- `im Handumdrehen` — idiom: "in no time". Literal "in the turn of the hand".
- `es hinkriegen` — colloquial separable verb: "to manage it". Register `colloquial`.
- `worauf es ankommt` — grammatical expression + valency (`ankommen auf + Akk.`), with a `worauf` pronominal adverb.
- `Zum Glück` — collocation/fixed adverbial: "luckily". Compositional but strongly fixed.

## 8. Language notes

- **English** phrasal verbs are the highest-yield category. Check whether the particle is separable (`pick it up`) and whether the meaning is idiomatic. Note transitivity.
- **French** has many fixed prepositional frames (`penser à`, `s'occuper de`, `être en train de`) — these are valency, not idioms. Spoken French drops `ne`; that is register, not slang.
- **Spanish** regional variation is high; `coger`, `pillar`, `vale`, `guay`, `chévere`, `boludo` all need region notes. The accidental `se` is grammar, not an expression.
- **German** separable verbs must be recorded with the split form observed (`kriegst … hin`). Compounds may be transparent (`Vorderreifen`) — gloss the parts, do not treat the compound as an idiom.

## 9. Common misclassifications

| Wrong | Right | Why |
|---|---|---|
| Calling any informal word "slang" | `colloquialism` or `informal` | Slang is group/time-bound |
| Calling a fixed preposition "idiom" | `valency` | The complement is governed |
| Calling a metaphor an idiom | plain usage | One-off image ≠ fixed unit |
| Calling `of course` an idiom | `grammatical-expression` / discourse marker | Meaning is procedural, unit is fixed |
| Treating a separable verb's split as two words | one record, split noted | Same lexeme |
| Marking an idiom `neutral` without thinking | check register | Idioms are often informal |
| Assigning `region` from a single spelling | omit or `unverified` | Spelling ≠ regionalism |
| Listing four slang items when only one is real | list one, or say none | Honesty over volume |
