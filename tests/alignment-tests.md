# Test — Segmentation and Alignment

Verifies source preservation, stable IDs, one-to-one alignment, and safe batching.

## How to run

Use the prompts below. Check the aligned section and, for JSON runs, `scripts/validate_learning_document.py`. The validator's source-integrity check is the objective test.

## Cases

### T-AL-01 — Abbreviation must not split

**Input**

> Mr. Okonkwo arrived at 9.30 a.m. and waited for Dr. Silva. They discussed the U.S. proposal, e.g. the funding clause.

**Trigger prompt**: "精读，严格保留原文。"

**Expected**

- Sentences: 2 (or 3 if a defensible boundary is chosen — but never a split inside `Mr.`, `9.30`, `a.m.`, `Dr.`, `U.S.`, or `e.g.`).
- `Mr.`, `Dr.`, `e.g.`, `U.S.` preserved exactly.
- IDs sequential without gaps.

**Fail if**

- Splits after `Mr.` or `e.g.`
- Drops the periods in abbreviations.
- Changes `9.30` to `9:30`.

### T-AL-02 — One-to-one alignment

**Input** (5 sentences, two paragraphs)

> Le train est arrivé avec vingt minutes de retard. Personne ne semblait surpris. Sur le quai, un enfant demandait pourquoi les trains étaient toujours en retard. Sa mère a souri sans répondre. Le contrôleur, lui, a haussé les épaules.

**Expected**

- 5 sentence records, 5 translations.
- No translation covers two sentences; none is split.
- Paragraph structure preserved (if entered as one paragraph, output one).
- IDs `s01-01` … `s01-05`.

**Fail if**

- 4 records (two sentences merged).
- A translation attached to the wrong ID.
- Renumbering after a revision.

### T-AL-03 — Paragraph IDs

**Input**

> First paragraph sentence one. First paragraph sentence two.
>
> Second paragraph sentence one. Second paragraph sentence two.

**Expected**

- IDs `s01-01`, `s01-02`, `s02-01`, `s02-02`.
- `paragraph` values 1, 1, 2, 2.
- Whole-text translation has two paragraphs.

**Fail if**

- Sequential global numbering with paragraph 1 throughout.
- Paragraph 2 merged into paragraph 1.

### T-AL-04 — Quote with internal full stop

**Input**

> « Je ne viendrai pas. », a-t-elle dit, avant de raccrocher.

**Expected**

- One sentence unit (the quotation is embedded; the outer sentence continues).
- `« »`, the internal `.`, and the comma preserved.
- French spacing preserved.

**Fail if**

- Two sentences split at the inner period.
- Quotation marks normalized to `"`.

### T-AL-05 — Lyrics and line breaks

**Input**

> I left the light on
> by the door
> in case you came back
> for more

**Trigger prompt**: "把这四行歌词做成精读。"

**Expected**

- Four line units (or one stanza with the line breaks preserved inside `text`), not reflowed prose.
- Translation preserves line structure or explicitly states that line breaks are semantic.
- `genre: lyrics`.

**Fail if**

- Joins the lines into one sentence and translates as prose.
- Adds punctuation not in the source.

### T-AL-06 — Batch boundary and stable IDs

**Input**: a supplied text of 80+ sentences across 12 paragraphs.

**Expected**

- Batch boundaries announced and placed between paragraphs.
- IDs match absolute paragraph/sentence positions; batch 2 does not restart at `s01-01`.
- Merged document validates with no duplicate or missing IDs.
- State the batch ranges (e.g. `批次 1/3：第 1–4 段`).

**Fail if**

- IDs restart per batch.
- A batch ends mid-sentence.
- The merged output loses a paragraph or duplicates one.

### T-AL-07 — Translation omission

**Input**

> Das Museum öffnet um zehn. Der Eintritt ist frei. Am Montag bleibt es geschlossen.

**Expected**

- Three records, three translations, including the third sentence.
- No "the rest is similar" shortcut.

**Fail if**

- Two translations for three sentences.
- A translation marked "同上".

### T-AL-08 — Source typo preserved

**Input**

> She recieved the letter yesterday.

**Expected**

- `text` keeps `recieved`.
- A note flags the likely typo and gives the correct form, without replacing the source.
- Translation renders the intended meaning and notes the source issue.

**Fail if**

- Silently corrects to `received` in the quoted original.
- Ignores the typo entirely.

### T-AL-09 — Special characters and punctuation preserved

**Inputs** (run each separately)

> FR: « C'est déjà l'heure ; l'œuvre est à côté du théâtre. »
>
> ES: ¿Dónde está el niño? ¡Está en el jardín, junto al árbol!
>
> DE: Die Straße ist schön, aber die Füße tun weh. Größe zählt.
>
> EN: The café’s naïve façade cost €3.50.

**Expected**

- French: `« »`, `'`, `é`, `è`, `à`, `ô`, `œ`, `ç`, and the space before `;` preserved.
- Spanish: `¿`, `¡`, `ñ`, `á`, `é`, `í`, `ó` preserved.
- German: `ß`, `ä`, `ö`, `ü` preserved; no `ss` substitution.
- English: curly apostrophe `’`, `ï`, `é`, `€`, decimal point preserved; no diacritic stripping.
- JSON output remains valid UTF-8; the validator's source-integrity check passes.

**Fail if**

- Any diacritic is removed or transliterated.
- `ß` becomes `ss`, or `¿`/`¡` disappear.
- Curly quotes are replaced by straight quotes inside quoted source text.
- The file is written in a non-UTF-8 encoding.

## Machine check

```bash
python3 scripts/validate_learning_document.py doc.json --source source.txt
```

Pass requires: no errors, and the note `原文完整性通过` present. A whitespace-only warning is acceptable only if the JSON declares `source.integrity: "whitespace-normalized"`.

## Pass criteria

All eight cases pass. T-AL-01, T-AL-02, T-AL-06, and T-AL-08 are blocking: a failure in any of them fails the suite.
