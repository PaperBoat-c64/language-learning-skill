# Language Learning Studio

A Claude Code skill that turns an authentic text in **English, French, Spanish, or German** into a close-reading study packet: full translation, sentence-aligned bilingual reading, contextual vocabulary with morphology, collocations and idioms with register notes, grammar explanations, exercises, and review cards.

It is a study tool, not a translator. The source text stays intact; the packet makes it legible.

## What you get

| Section | Content |
|---|---|
| 全文译文 | Natural, context-aware translation into the explanation language |
| 逐句对照 | Original + translation per sentence, with literal glosses only where useful |
| 词汇 | Surface form, lemma, POS, contextual sense, morphology, collocations, examples, pitfalls, priority, confidence |
| 固定表达与俚语 | Collocations, phrasal verbs, idioms, colloquialisms, slang, valency patterns — typed, register-marked, region-marked where evidenced |
| 语法 | Three to six points tied to specific sentence IDs |
| 练习 | Meaning, cloze, collocation, rewrite, grammar discrimination, translation, imitation, speaking, recall cards |
| 质量检查 | Eleven checks with an honest pass/unverified/not-applicable record |

## Install

The skill is a folder with `SKILL.md` at its root.

**Personal (all projects)**

```bash
cp -R language-learning-skill ~/.claude/skills/
```

**Project only**

```bash
mkdir -p .claude/skills
cp -R language-learning-skill .claude/skills/
```

Claude Code discovers skills in `~/.claude/skills/` and `<project>/.claude/skills/`. No build step, no dependencies. Python 3 is needed only for the optional validation scripts.

## Invoke

Talk to it in plain language; the skill's description handles triggering.

```text
精读这段法语，给我逐句对照和重点词汇：
« ... »
```

```text
Study this Spanish text closely. Focus on the tenses and the colloquial expressions.
```

```text
Make Anki cards from this German paragraph.
```

```text
Review this English article, but explain grammar only where it matters.
```

```text
Turn this into JSON conforming to the schemas.
```

Useful parameters you can state explicitly:

- **explanation language** — defaults to Chinese; say "explain in English" to change it.
- **learner level** — say it if you want; otherwise the skill uses a default-adaptive policy for a B1 reader and tags each item by priority. It will not interrogate you.
- **output mode** — `study` (default), `compact`, `cards`, `exercise-sheet`, `json`.
- **batch size / range** — for long texts, say "only paragraphs 1–4" or let it batch automatically.

## Configuration

There is no config file and no environment variable. Behaviour is set per request, with defaults in `SKILL.md` Step 0.

| Setting | Default | How to change |
|---|---|---|
| Explanation language | Simplified Chinese (`zh-CN`) | Say "explain in English" / "用日语解释" |
| Learner level | `default-adaptive` (gloss for a B1 reader, rank by priority) | State a level or exam; or edit the default policy in `SKILL.md` |
| Output mode | `study` | Ask for `compact`, `cards`, `exercise-sheet`, or `json` |
| Batching | automatic above ~60 sentences / ~1,500 words | Request a paragraph range, or edit the threshold in `references/learning-workflow.md` |
| Schema location | `schemas/` next to the script | `--schema-dir` on the validator |
| Warning policy | warnings do not fail validation | `--strict` makes warnings fail |

To change a default permanently, edit `SKILL.md` Step 0 and the relevant reference file. Keep the schema and `references/annotation-schema.md` in sync when adding fields.

## How it works

1. Detect language, genre, register, and teaching targets.
2. Segment into paragraphs and sentences with stable IDs `s01-03`.
3. Translate the whole text, then align one translation per sentence.
4. Annotate vocabulary with contextual senses and morphology.
5. Extract and classify expressions.
6. Explain only the grammar this text needs.
7. Generate exercises with answer keys.
8. Run eleven QA checks and report honestly.
9. Render in the requested mode.

Detailed rules live in `references/`; language-specific norms in `languages/`; reusable prompt templates in `prompts/`; JSON contracts in `schemas/`.

## Repository layout

```text
language-learning-skill/
├── SKILL.md
├── README.md
├── references/
│   ├── learning-workflow.md
│   ├── annotation-schema.md
│   ├── translation-principles.md
│   ├── idioms-and-slang.md
│   ├── proficiency-and-difficulty.md
│   ├── quality-assurance.md
│   └── output-formats.md
├── languages/
│   ├── english.md
│   ├── french.md
│   ├── spanish.md
│   └── german.md
├── prompts/
│   ├── analyze-text.md
│   ├── translate-contextually.md
│   ├── annotate-vocabulary.md
│   ├── extract-expressions.md
│   ├── explain-grammar.md
│   ├── generate-exercises.md
│   └── quality-review.md
├── schemas/
│   ├── learning-document.schema.json
│   ├── sentence.schema.json
│   ├── vocabulary.schema.json
│   ├── expression.schema.json
│   └── exercise.schema.json
├── examples/
│   ├── english/{source.txt,example.json,example.md,example.en.md}
│   ├── french/{source.txt,example.json,example.md}
│   ├── spanish/{source.txt,example.json,example.md}
│   └── german/{source.txt,example.json,example.md}
├── scripts/
│   ├── validate_learning_document.py
│   └── check_skill_assets.py
└── tests/
    ├── language-detection.md
    ├── alignment-tests.md
    ├── grammar-tests.md
    ├── idiom-tests.md
    └── regression-tests.md
```

## Examples

Each language folder contains a complete, validated packet built from an original short text:

- `examples/english/` — community garden narrative; phrasal verb, understatement, past perfect.
- `examples/french/` — neighborhood narrative; passé composé vs. imparfait, pronominal agreement, `depuis`.
- `examples/spanish/` — pottery workshop; accidental `se`, `deber de`, `lo` + adjective.
- `examples/german/` — bicycle repair; `als` clause inversion, separable verb, relative clause.

Each has `source.txt` (the text), `example.md` (the rendered packet), and `example.json` (the structured document).

`examples/english/example.en.md` is an English-language rendering of the English example: the source is quoted verbatim, and the explanations, paraphrase, exercises, and answer key are in English. It is a demonstration of `explanationLanguage: en`, not a replacement for `example.md` or the validated `example.json`.

## Validation

```bash
# required files, frontmatter, internal links, schema JSON syntax
python3 scripts/check_skill_assets.py

# one document: structure, IDs, references, source integrity
python3 scripts/validate_learning_document.py examples/english/example.json \
  --source examples/english/source.txt

# all examples
for f in examples/*/example.json; do
  python3 scripts/validate_learning_document.py "$f" --source "${f%/*}/source.txt" || exit 1
done
```

When `jsonschema` is installed, the validator also runs formal Draft 2020-12 schema validation. Without it, it falls back to built-in structural checks and says so.

### Results at build time (2026-10-26)

| Check | Result |
|---|---|
| Required file tree | pass |
| `SKILL.md` frontmatter (name, description length, triggers) | pass |
| Internal path references in `SKILL.md` | pass |
| Schema files are legal JSON and legal Draft 2020-12 schemas | pass (checked with jsonschema 4.25.1) |
| Four example JSON documents against schemas | pass |
| ID uniqueness and cross-reference resolution | pass |
| Source integrity (sentence concatenation vs. `source.txt`) | pass for all four |
| Unicode / diacritics / `ß` / `¿¡` preservation | pass for the four examples |
| Explanation quality in all four languages | manually reviewed during authoring; **not** independently native-checked |

Formal schema validation was run in an isolated virtual environment with `jsonschema` 4.25.1; the system Python does not have it installed, so reruns there report structural checks only.

## Design guarantees

- **Source fidelity** — quoted text is verbatim; typos are preserved and flagged, never silently fixed.
- **No fabrication** — no invented definitions, frequency data, CEFR levels, etymology, or regional claims. Uncertain items carry `confidence` and `needsVerification`.
- **Context first** — one contextual sense per vocabulary item, with a reason when the word is polysemous.
- **Layered meaning** — idioms report literal and contextual meaning separately.
- **No padding** — an empty idiom section is an acceptable, explicit result.
- **Honest QA** — unverified checks stay unverified; the report is part of the output.

## Known limitations

- Only the four languages above are supported. Other languages would need their own `languages/*.md` norm.
- The default explanation language is Simplified Chinese; other languages work but the reference templates are written around Chinese output.
- No external dictionary, corpus, or native-speaker verification is performed. Confidence flags reflect that.
- Regional claims about slang are deliberately conservative and often marked unverified.
- CEFR levels are never assigned to texts or words; the skill describes observable difficulty instead.
- Image-only sources require transcription first; transcription-dependent checks are marked unverified.
- Long copyrighted texts are processed from what the user supplies, with excerpts kept proportionate. The skill does not reconstruct texts from memory.
- The bundled schemas enforce structure and references, not linguistic correctness. A schema-valid packet can still contain a bad gloss; the QA and native review are separate.
- `jsonschema` is optional. Without it, formal schema validation is skipped and the validator reports structural checks only.

## Extending

To add a language:

1. Add `languages/<code>.md` with its own morphology, word order, register, segmentation, and error profile. Do not copy another language's rules.
2. Extend the `textLanguage` enum in `schemas/learning-document.schema.json`.
3. Add `examples/<language>/` with `source.txt`, `example.json`, `example.md`.
4. Add it to `LANGUAGES` and `REQUIRED_FILES` in `scripts/check_skill_assets.py`.
5. Add detection and grammar cases to the test files.

To add a new schema field, update the schema and `references/annotation-schema.md` together; the validator's structural checks may need the same change.
