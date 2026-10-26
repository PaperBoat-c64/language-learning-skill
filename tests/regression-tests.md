# Test — Regression Suite

Reproducible checks for defects found during construction, plus the machine validations that must stay green.

## How to run

From the skill root:

```bash
python3 scripts/check_skill_assets.py
for f in examples/*/example.json; do
  python3 scripts/validate_learning_document.py "$f" --source "${f%/*}/source.txt" || exit 1
done
```

With `jsonschema` installed, the validator additionally performs formal schema validation.

## Machine regressions

### R-01 — Asset tree and frontmatter

**Command**: `python3 scripts/check_skill_assets.py`

**Expected**: `PASS`, 0 errors. Warnings about path casing or description length are defects to fix.

**Recorded 2026-10-26**: `PASS: 0 error(s), 0 warning(s)`, 32 required files checked.

**Fail if**: any required file is missing or empty; `SKILL.md` lacks `name`/`description`; an internal path does not resolve; a schema is not legal JSON; an example folder is incomplete.

### R-02 — Example documents validate

**Command**: the loop above.

**Expected**: `PASS` for all four, with `原文完整性通过` notes.

**Recorded 2026-10-26**: English, French, Spanish, German each pass with 0 errors and 0 warnings under jsonschema 4.25.1.

**Fail if**: any schema error, duplicate ID, dangling reference, surface form not found in its sentence, exercise without an answer, or source mismatch.

### R-03 — Schemas are legal Draft 2020-12 schemas

```bash
python3 - <<'PY'
import json
from pathlib import Path
from jsonschema import Draft202012Validator
for p in sorted(Path('schemas').glob('*.json')):
    Draft202012Validator.check_schema(json.loads(p.read_text(encoding='utf-8')))
    print('OK', p)
PY
```

**Recorded 2026-10-26**: all five schemas valid.

**Fail if**: `SchemaError` for any file, including unresolved relative `$ref` targets.

### R-04 — Surface form must match the actual inflection

**Regression**: an English vocabulary record used `surface: "dug"` for a sentence containing `digging`. The validator's substring check caught it.

**Test**: any vocabulary item whose `surface` is not a substring of the cited sentence must fail validation or be corrected.

**Expected now**: `examples/english/example.json` v003 uses `digging`, with `dug` explained as the irregular past form.

**Fail if**: a record's `surface` is a lemma rather than the text's form, or the validator stops checking substrings.

### R-05 — Sentence-initial capitalization in expressions

**Regression**: Spanish `por si acaso` appeared at the start of a sentence as `Por si acaso`; a case-sensitive substring check rejected the lowercase record.

**Test**: an expression spanning a sentence-initial capital must use the source's capitalization in `text` and note the canonical lowercase form.

**Expected now**: `examples/spanish/example.json` e002 has `text: "Por si acaso"` and a note.

**Fail if**: the record silently lowercases the span, or the validator is loosened to ignore case entirely (that would hide real errors).

### R-06 — Priority distribution warning

**Regression**: French and Spanish examples initially had 2/5 vocabulary items at `high`, exceeding the one-third guideline.

**Test**: the validator warns when more than one third of vocabulary items are `high`.

**Expected now**: no such warning in any example.

**Fail if**: the warning reappears or the rubric is ignored by marking everything `medium` without judgment.

### R-07 — Character and sentence counts

**Regression**: hand-written `characterCount` values drifted from the actual source length.

**Test**: the validator compares `source.characterCount` and `source.sentenceCount` with reality.

**Expected now**: no count warnings.

**Fail if**: counts are decorative rather than computed.

### R-08 — Schema `$ref` resolution

**Regression**: an earlier validator build resolved sibling schema refs through `$id` and failed with `Unresolvable JSON pointer: '$defs/grammarPoint'`.

**Test**: run validation with `jsonschema` installed; the run must report `JSON Schema 校验通过（jsonschema）`, not a warning.

**Expected now**: the script uses the `referencing` registry and falls back to `RefResolver` only on old installs.

**Fail if**: the schema check silently degrades to structural checks while `jsonschema` is installed.

## Manual regressions

### R-09 — No fabricated level or frequency claims

**Test**: search the output for `A1`, `A2`, `B1`, `B2`, `C1`, `C2`, `高频`, `most common`, `high-frequency`, `%`.

**Expected**: every hit is either quoted from a cited source with `externalLevel`, or absent.

**Fail if**: a word is labelled "B2" or "high-frequency" without a source.

### R-10 — QA honesty

**Test**: construct a packet with one deliberate uncertainty (e.g. a regional slang item with no evidence) and run QA.

**Expected**: that check is `unverified`, the summary is not `pass`, and the disclosure appears in the text.

**Fail if**: the summary says `pass` while any row is `unverified`/`not-applicable`, or the disclosure is omitted.

### R-11 — No padding of the idiom section

**Test**: process a plain text with no idioms ("The meeting starts at nine. Please bring the report.").

**Expected**: an explicit "no high-value expressions" line, not invented items.

**Fail if**: slang or idioms are fabricated to fill the section.

### R-12 — Source typo preserved

**Test**: process `She recieved the letter yesterday.`

**Expected**: `recieved` stays in `sentences[].text`; a note flags it; the translation gives the intended meaning.

**Fail if**: the quoted source is silently corrected.

## Pass criteria

All machine regressions (R-01–R-08) must pass on every release. Manual regressions (R-09–R-12) must pass on the test texts in this folder and in `tests/`. A regression failure blocks release until the cause is fixed and the affected checks are re-run.
