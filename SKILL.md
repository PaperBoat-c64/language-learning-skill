---
name: language-learning-skill
description: Builds close-reading study packets from authentic English, French, Spanish, or German texts. Produces a full translation, sentence-aligned bilingual reading, contextual vocabulary with morphology, collocations/idioms/slang with register and regional notes, grammar explanations, exercises, and review cards. Use when the user pastes, uploads, or points to a text in one of these languages and asks to study it, read it closely, translate it with explanations, annotate vocabulary, learn expressions, explain grammar, or make exercises or flashcards from it.
---

# Language Learning Studio

Turn an authentic text into a study packet: faithful translation, sentence-by-sentence bilingual reading, vocabulary, expressions, grammar, exercises, and cards. The learner reads the original; the packet makes it legible.

## Non-negotiables

1. **Source fidelity.** Quote the source verbatim in `sentences[].text`. Never delete, reorder, merge, correct, modernize, or sanitize it. Keep paragraph order, punctuation, capitalization, and sentence boundaries. If a typo or oddity is in the source, keep it and flag it in `notes` — do not silently fix it.
2. **No invention.** Never fabricate definitions, frequency data, CEFR levels, etymology, regional use, or grammar rules. If a claim cannot be grounded in the text plus reliable knowledge, omit it or mark `confidence: "low"` and `needsVerification: true`.
3. **Context over dictionary.** Every gloss answers "what does it mean *here*". For multi-sense words, say why this sense applies in this sentence.
4. **Layer meanings.** For idioms and slang, report literal meaning, contextual meaning, and connotation separately. Never translate an idiom word-for-word as if it were literal.
5. **No padding.** Extract only what is worth learning for this text and level. If there is no high-value slang or idiom, say so explicitly rather than inventing items.
6. **Flag uncertainty as content.** Low-confidence items stay in the packet with their flags; silent confidence is a defect.

## Step 0 — Parameters (decide, don't interrogate)

Determine these from the request; do not run a questionnaire.

| Parameter | Source | Default |
|---|---|---|
| `textLanguage` | The text itself | Detect silently; if genuinely mixed, ask once which is primary |
| `explanationLanguage` | User's language | Chinese (简体中文); follow the user if they write in another language |
| Learner level | User statement | **Default-adaptive** (below) |
| Output mode | User request | `study` |
| Genre | The text | `other` |

**Default-adaptive level policy** (when level is unspecified): do not ask "what is your level?" and do not stall. Instead:

- Gloss everything non-obvious for a B1 reader, but keep notes tight.
- Explain grammar only where the text actually hinges on it (tense choice, word order, agreement, pronoun reference).
- Give every item a `priority` so a stronger reader can skip the basics, and every analysis item a `confidence`.
- If the user later reveals a level, adjust depth on the next pass; do not silently regenerate prior output.

Ask at most one clarifying question per run, and only when ambiguity would corrupt the output (primary language of a mixed text; whether lyrics should be treated as poetry). Otherwise proceed and state assumptions in one line.

## Step 1 — Workflow

Run these in order. Each step names the file to read when it is needed — do not preload everything.

1. **Analyze** — language, genre, register, difficulty signals, teaching targets. Read `prompts/analyze-text.md`; load `languages/<code>.md` for the detected language.
2. **Preserve & segment** — split into paragraphs and sentences; assign stable IDs `s<paragraph>-<sentence>` (e.g. `s01-03`). Read `references/learning-workflow.md`.
3. **Translate whole** — natural, context-aware full translation. Read `references/translation-principles.md` and `prompts/translate-contextually.md`.
4. **Align** — per-sentence original + translation, with a literal rendering only where it clarifies.
5. **Annotate vocabulary** — surface form, lemma, POS, contextual sense, morphology, collocations, examples, pitfalls, priority, confidence. Read `references/annotation-schema.md` and `prompts/annotate-vocabulary.md`.
6. **Extract expressions** — collocations, phrasal verbs, idioms, colloquialisms, slang, valency patterns, grammatical fixed expressions. Read `references/idioms-and-slang.md` and `prompts/extract-expressions.md`.
7. **Explain grammar** — only structures that matter for understanding or production here. Read `prompts/explain-grammar.md`.
8. **Exercises** — grounded in this text's actual teaching points. Read `prompts/generate-exercises.md`.
9. **QA** — run every check in `references/quality-assurance.md`; fix the failing stage only.
10. **Output** — render in the requested mode. Read `references/output-formats.md`.

For very short texts (a sentence or two) merge steps 2–4 and 6–7. For long texts, batch by paragraph blocks (below).

## Language files

Load exactly one, matching `textLanguage`:

- `languages/english.md`
- `languages/french.md`
- `languages/spanish.md`
- `languages/german.md`

They carry language-specific morphology, agreement, word-order, register, and segmentation rules. Never apply one language's grammar rules to another.

## Batching and ID stability

For long texts (roughly >60 sentences or >1,500 words), process in paragraph-aligned batches:

- Batch boundaries fall between paragraphs, never inside a sentence.
- IDs derive from absolute paragraph/sentence position, so they never shift between batches. Never renumber after the fact.
- Keep one shared terminology note across batches: if a word is glossed one way in batch 1, reuse it in batch 5 unless context genuinely differs (then say why).
- Merge batches in document order; run QA on the merged document.
- State batch boundaries in the output (`批次 1/3：第 1–4 段`).

## Output modes

| Mode | Use when | Contents |
|---|---|---|
| `study` (default) | User wants to learn the text | Full translation, aligned reading, vocabulary, expressions, grammar, exercises, cards |
| `compact` | Quick read, short text | Aligned reading + top-priority vocabulary/expressions only |
| `cards` | User wants review material | Review table/cards only, export-ready |
| `exercise-sheet` | Practice focus | Exercises + answer key only |
| `json` | User wants structured data | Learning document JSON conforming to `schemas/` |

Details and templates: `references/output-formats.md`.

## Quality gate

Before delivering, run the eleven checks in `references/quality-assurance.md`: source integrity, alignment, lemma/form correctness, contextual sense, grammar accuracy, expression classification, register/region claims, redundancy, unsupported level/frequency claims, schema conformance, exercise answerability.

Fix only the failing stage, then re-run the affected checks. Report the QA result honestly: name anything marked `unverified` rather than implying it passed. If validation is impossible (e.g. the source was supplied only as an image), say what could not be verified.

## Structured output

When producing JSON, conform to:

- `schemas/learning-document.schema.json` (top level)
- `schemas/sentence.schema.json`
- `schemas/vocabulary.schema.json`
- `schemas/expression.schema.json`
- `schemas/exercise.schema.json`

Validate with:

```bash
python3 scripts/validate_learning_document.py path/to/document.json --source path/to/source.txt
```

The script uses `jsonschema` when installed and falls back to structural checks; it also verifies ID uniqueness, cross-references, and source-text integrity.

## Copyright and length

Work from the text the user supplies. Do not reconstruct from memory lyrics, book passages, or articles the user has not provided. For long copyrighted works, quote only the passages under study and keep analysis proportionate.

## What this skill must not do

- Produce a translation without the aligned original.
- Present a "literal" gloss as the natural translation.
- Invent a CEFR level, frequency count, or "most common" claim.
- Assign a regional label to slang without evidence; when unsure, mark `regionCertainty: "unverified"`.
- Flatten a literary, ironic, or vulgar passage into neutral textbook prose without saying so.
- Rewrite the source into "better" language.
