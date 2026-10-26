# Learning Workflow

The operating procedure behind `SKILL.md`. Read this when you need the detail of a step, not just its name.

## Contents

1. [Scope and output](#1-scope-and-output)
2. [Parameters and defaults](#2-parameters-and-defaults)
3. [Segmentation and stable IDs](#3-segmentation-and-stable-ids)
4. [The ten steps](#4-the-ten-steps)
5. [Batching, resume, and revision](#5-batching-resume-and-revision)
6. [Level adaptation](#6-level-adaptation)
7. [Failure and edge cases](#7-failure-and-edge-cases)
8. [Pre-delivery checklist](#8-pre-delivery-checklist)

## 1. Scope and output

Input: one authentic text in English, French, Spanish, or German — article, news, fiction, dialogue, lyrics, email, social post, poem, transcript.

Output: a learning document. Human-readable Markdown by default; JSON when requested or when the text will be revised across sessions. The document contains:

- source text preserved verbatim, segmented;
- a whole-text translation, plus sentence-aligned original/translation pairs;
- vocabulary records with form, lemma, part of speech, contextual sense, morphology;
- expression records (collocations, phrasal verbs, idioms, colloquialisms, slang, valency patterns);
- grammar notes tied to specific sentences;
- exercises with answer keys;
- a QA record.

The document never replaces the source. It annotates it.

## 2. Parameters and defaults

Resolve before writing anything.

| Parameter | Values | Default |
|---|---|---|
| `textLanguage` | `en`, `fr`, `es`, `de` | detect |
| `explanationLanguage` | any | Chinese (简体中文) |
| `mode` | `study`, `compact`, `cards`, `exercise-sheet`, `json` | `study` |
| `genre` | `news`, `article`, `fiction`, `dialogue`, `lyrics`, `email`, `social-media`, `academic`, `other` | `other` |
| Learner level | user-stated or default-adaptive | default-adaptive |

Language detection cues: function words, diacritics, punctuation, morphology. Do not rely on a single character — `ß` and `ä` point to German, but `ä` also occurs in some names; `¿`/`¡` are strongly Spanish; `ñ` Spanish; accented `à`/`è`/`ç` French; `œ` French. A text with Spanish and English mixed is still one primary language; ask only if the primary is genuinely unclear, and only once.

Do not ask for the explanation language when the user's own message makes it obvious.

## 3. Segmentation and stable IDs

**Paragraphs** are separated by blank lines or the source's own paragraph marks. Number from 1.

**Sentences** are split at `.`, `?`, `!`, `…`, and their Spanish/French equivalents, plus paragraph ends. Do not split:

- after abbreviations (`Mr.`, `Dr.`, `etc.`, `e.g.`, `i.e.`, `M.`, `Mme`, `Sr.`, `Sra.`, `z. B.`, `usw.`, `Dr.`, `bzw.`);
- inside decimal numbers (`3.14`, `1.000,50`) or times (`10.30 Uhr`);
- inside a quote where the sentence continues;
- at an ellipsis used as a hesitation inside a sentence unless it clearly ends it.

When unsure, prefer the larger unit. A slightly long sentence with a correct boundary is safer than a false split that destroys a construction.

**IDs**: `s<paragraph>-<sentence>`, two digits each, e.g. `s01-01`, `s03-12`. Vocabulary `v001`, expressions `e001`, grammar `g001`, exercises `x001`, sequential in document order. IDs never change once assigned.

If the source itself is a list, headings, or dialogue tags, preserve them inside the sentence text or as paragraph text — do not discard them. Missing structural text is a source-integrity failure.

## 4. The ten steps

Each step has an entry condition, an output, and a gate. Do not start a step before its gate passes.

### Step 1 — Analyze

Determine language, genre, register, audience, and where the teaching value lies (dense idioms? tense contrast? formal syntax? dialect?). Output a short plan: 3–6 teaching targets. Gate: the plan names structures that actually occur in the text, with sentence IDs.

### Step 2 — Preserve and segment

Produce the paragraph/sentence model. Gate: concatenating all sentence texts reproduces the source (whitespace normalized); no sentence is empty; no paragraph is absent.

### Step 3 — Translate whole text

Translate into `explanationLanguage` as one coherent text, reading the whole source first. Preserve paragraph structure. Gate: every source paragraph has a translation; no added commentary inside the translation.

### Step 4 — Align

Attach a translation to each sentence. Use a literal gloss only as an extra field where it explains a construction, never as the main translation. Gate: one translation per sentence, no merged or split pairs, no translation that belongs to a neighbouring sentence.

### Step 5 — Annotate vocabulary

Select 5–20 items depending on text length and level. Prioritize: high-frequency useful words, false friends, irregular forms, context-shifted meanings, words whose grammar matters here. Skip proper nouns unless they teach something. Gate: every `surface` is an exact substring of its sentence; every `lemma` is a real citation form; every item has `confidence`.

### Step 6 — Extract expressions

Classify by type using the decision procedure in `idioms-and-slang.md`. Gate: each expression appears verbatim in the text; the type matches the tests; literal and contextual meaning are distinct where relevant; no item was added just to reach a count.

### Step 7 — Explain grammar

Three to six notes, tied to sentence IDs, explaining what a learner cannot get from a dictionary: agreement, case, word order, aspect, pronominal verbs, subjunctive triggers, separable verbs, pronoun reference. Gate: every rule stated is correct for this language and this sentence; no rule is asserted without an example from the text.

### Step 8 — Exercises

Build exercises from the actual items annotated. Cover at least three different exercise types when the text supports it. Gate: every exercise has a checkable answer or rubric; no exercise tests something not taught in the packet.

### Step 9 — QA

Run all eleven checks in `quality-assurance.md`. Fix the failing stage and re-run the affected checks. Gate: no `fail` remains unaddressed; every `unverified` is disclosed.

### Step 10 — Render

Produce the requested mode using `output-formats.md`. Gate: headings, numbering, and IDs match the document model; Unicode is intact.

## 5. Batching, resume, and revision

Batch when the text exceeds roughly 60 sentences or 1,500 words.

- Cut between paragraphs. Record `batch: {index, total}` and paragraph range.
- Never renumber. IDs use absolute positions, so batch 2 starts at `s09-01` if that is where its first paragraph sits.
- Maintain a running terminology decision list: word → chosen gloss. Reuse it; if a later context demands a different gloss, note both and why.
- On revision, change the smallest unit affected. If sentence alignment changed, re-check translation and every reference to that sentence ID.
- On merge, validate the merged document, not each batch alone.

## 6. Level adaptation

Use observable behavior, not labels:

| If the learner is… | Do | Don't |
|---|---|---|
| Beginner | Gloss function words and core vocabulary; explain basic agreement and word order; translations stay close; exercises are recognition-based | Don't explain subordinate-clause nuance; don't leave idioms unexplained |
| Intermediate | Gloss less common lexis; focus on collocation, aspect/tense choice, pronoun systems; exercises mix recognition and production | Don't re-explain the present tense every time |
| Advanced | Focus on register, connotation, regional variation, syntax and rhetoric; exercises are rewriting and nuance discrimination | Don't over-gloss ordinary vocabulary |
| Unknown | Default-adaptive: gloss for B1, priority-rank every item | Don't interrogate the user |

Never print a CEFR label on an item. See `proficiency-and-difficulty.md`.

## 7. Failure and edge cases

- **Poetry/lyrics**: line breaks carry meaning. Keep them; do not reflow into prose sentences. If a line is a fragment, segment as a fragment.
- **Dialogue**: keep speaker labels (`—`, `«`, quotation marks) exactly. Do not merge turns.
- **Mixed language**: analyze the primary; note borrowed segments and explain them as borrowings, not as errors.
- **OCR-noise or typos**: preserve, flag, and only then optionally offer a corrected reading in a note. Never replace the source.
- **Very short text** (1–2 sentences): merge steps, but keep at least vocabulary + one expression or grammar note + one exercise.
- **No high-value slang**: state "本段未发现值得专门学习的高价值俚语/习语" rather than filling the section.
- **Text too long for one pass**: batch and say so.
- **Source supplied as an image**: transcribe first, show the transcription, and mark transcription-dependent checks as unverified unless the user confirms.

## 8. Pre-delivery checklist

- [ ] Source reproduced verbatim; paragraph and sentence order intact.
- [ ] Every sentence has one aligned translation.
- [ ] Every vocabulary surface form exists in its sentence.
- [ ] Lemmas are citation forms; morphology explained only where non-trivial.
- [ ] Expressions classified, literal vs. contextual meanings separated.
- [ ] Grammar notes cite sentence IDs and are correct for the language.
- [ ] Exercises have answers/rubrics and map to taught items.
- [ ] Priority and confidence present on all analysis items.
- [ ] QA report included; unverified items disclosed.
- [ ] Unicode, diacritics, apostrophes, and quotation marks intact.
