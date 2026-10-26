# Translation Principles

Translation here serves comprehension, not publication. The reader must be able to see how the original works — so accuracy of meaning comes first, naturalness second, and style third, in that order of precedence but not in isolation.

## 1. Fidelity hierarchy

When principles conflict, resolve in this order:

1. **Propositional meaning** — who did what, to whom, when, with what modal force (certainty, obligation, permission, doubt).
2. **Illocution** — is the sentence asking, ordering, joking, apologizing, warning?
3. **Register and stance** — formal/informal, affectionate, ironic, dismissive, vulgar.
4. **Imagery and rhythm** — metaphor, sound, line breaks.
5. **Surface form** — word order, sentence length.

A translation that preserves 5 at the cost of 1 is wrong. A translation that preserves 1–3 and loses 4 is acceptable if the loss is noted.

## 2. Natural translation, then literal gloss

- The **main translation** is what a competent speaker of the explanation language would naturally write for this passage in this context. It is not word-for-word.
- The **literal gloss** (optional, `literal` field) shows the source's construction when that construction is the teaching point: `il y a` → literally "there has"; `se me cayó` → literally "it fell itself to-me".
- Never present the literal gloss as the translation. Never omit the natural translation because the literal one is "interesting".

## 3. Contextual sense selection

For a polysemous word, the packet must state which sense is active and why. Signals include:

- collocates (`prendre une décision` vs. `prendre le train`);
- syntactic frame (`il s'agit de` + noun/infinitive);
- aspect/tense (`il a dû partir` = must have left; `il devait partir` = was supposed to leave);
- register and genre (`cap` in a news headline vs. in a hiking text);
- neighbouring discourse (contrast, causation, concession).

If two readings remain possible after analysis, translate the more likely one and record the alternative in `notes` with `confidence: "medium"` or `"low"`. Do not silently choose.

## 4. Idioms and fixed expressions

- Translate the **function**: an idiom of disbelief becomes an idiom of disbelief, not a literal image.
- If the explanation language has an equivalent idiom, use it and mark it as equivalent, not literal.
- If no equivalent exists, translate the meaning plainly and put the image in a note.
- Never split an idiom across sentence translations.
- Regional or dated idioms keep their flavour note even when the translation is plain.

See `idioms-and-slang.md` for classification and register handling.

## 5. Register

Match the source's register in the translation, and say when you cannot.

| Source signal | Translation behaviour |
|---|---|
| Formal written prose | Standard written explanation language; no slang |
| Journalistic neutral | Neutral; keep headline terseness only if it does not distort |
| Spoken dialogue | Natural spoken explanation language; contractions and particles allowed |
| Colloquial / slang | Colloquial equivalent; if none, plain meaning + register note |
| Vulgar | Translate the force honestly; do not sanitize into politeness without a note |
| Literary | Preserve imagery and rhythm where possible; note losses |
| Irony | Preserve the irony; a flat literal translation destroys it |

A common failure is leveling everything to textbook neutrality. That is a translation error, not a style choice.

## 6. Culture-bound terms

For food, institutions, holidays, measures, and titles:

- Keep the original term when it is the referent the learner will meet again (`laïcité`, `comedor popular`, `Feierabend`, `thanksgiving`), with a short gloss on first use.
- Use a functional equivalent when the original term would mislead.
- Do not over-exoticize: a `boulangerie` is a bakery unless the text is about the institution.
- Convert units only in a note; keep the original in the sentence.

## 7. Ambiguity and underspecification

- **Grammatical ambiguity** (Spanish `se`, German `sie`, French `on`): choose the reading supported by context, state the alternative.
- **Scope ambiguity** (`all students did not pass`): translate the reading the context supports; note the other.
- **Unclear referent**: translate with the most likely referent and flag it; do not invent a name.
- **Incomplete sentences** (headlines, notes, lyrics): translate as fragments. Do not complete them.

## 8. Names, numbers, dates, quotations

- Keep proper names in the original script; do not translate people's names.
- Keep numerals, times, and dates as written; explain the convention in a note if it differs.
- Keep quoted material quoted in the translation; do not fold a quotation into reported speech.
- Preserve typographic quotation marks' function even if you normalize their glyph (see §10).

## 9. Literary and lyrical texts

- Preserve line breaks and stanza structure. Do not merge lines into prose.
- Prefer meaning over rhyme. Never invent an image to save a rhyme.
- Mark any loss of sound pattern or double meaning explicitly.
- For poetry where syntax is deliberately broken, keep the brokenness in the aligned translation and explain the syntax in a grammar note.

## 10. Unicode, punctuation, and formatting

- File encoding is UTF-8. Preserve diacritics exactly: `é`, `è`, `ê`, `ë`, `à`, `ç`, `ô`, `œ`, `ñ`, `ü`, `ö`, `ä`, `ß`, `¿`, `¡`, `«»`, `„“`.
- Do not strip accents to make text "searchable". Do not replace `ß` with `ss` except when quoting a source that already did.
- Apostrophes: French elision uses `'` (U+0027) or `’` (U+2019) depending on the source. **Preserve the source's character in `sentences[].text`**; use a consistent apostrophe in your own generated examples and say which if it matters.
- French spacing: a space (ideally narrow no-break) precedes `; : ! ?` and inside `« »`. Preserve the source's convention; do not "fix" it silently.
- Spanish opens questions and exclamations with `¿` and `¡`. Missing them is a source modification, not normalization.
- German nouns are capitalized. Do not lowercase them in notes or examples.
- Hyphens and dashes are different characters: `-` (hyphen), `–` (en dash), `—` (em dash). Keep the source's.

## 11. What not to do

- Do not translate word-for-word and call it "literal accuracy".
- Do not add information the source does not contain to make the translation smoother.
- Do not remove hedges, insults, hesitation, or repetition.
- Do not merge two source sentences into one fluent target sentence in the aligned view. The whole-text translation may flow; the aligned pairs must stay one-to-one.
- Do not translate idioms literally in the main text.
- Do not use the explanation language's cultural defaults to replace the source's.
- Do not translate the source's errors as if they were correct usage — flag them.

## 12. QA hooks

After translating, check:

1. Every sentence has exactly one aligned translation.
2. The whole-text translation covers every paragraph.
3. Idioms are not literal in the main translation.
4. Register is consistent with the source.
5. Names, numbers, and quotations match.
6. No added content.
7. Ambiguities are flagged, not hidden.
8. Unicode is intact.
