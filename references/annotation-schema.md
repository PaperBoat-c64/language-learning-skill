# Annotation Schema

The canonical record model. JSON Schemas in `../schemas/` enforce the shapes; this file explains the judgment behind each field.

## Contents

1. [Record model](#1-record-model)
2. [IDs and cross-references](#2-ids-and-cross-references)
3. [Vocabulary records](#3-vocabulary-records)
4. [Morphology rules](#4-morphology-rules)
5. [Priority rubric](#5-priority-rubric)
6. [Confidence and verification](#6-confidence-and-verification)
7. [Expression records](#7-expression-records)
8. [Grammar records](#8-grammar-records)
9. [Optional and empty fields](#9-optional-and-empty-fields)
10. [Anti-patterns](#10-anti-patterns)

## 1. Record model

A learning document has one `meta`, one `source`, and ordered collections:

| Collection | ID | One record per… |
|---|---|---|
| `sentences` | `s01-03` | sentence |
| `vocabulary` | `v001` | word or fixed lexical unit worth learning |
| `expressions` | `e001` | multi-word unit with a meaning or use worth learning |
| `grammar` | `g001` | grammar point actually instantiated in the text |
| `exercises` | `x001` | exercise item |
| `qa.checks` | `c01`…`c11` | quality check |

Records refer to each other by ID. A sentence lists the vocab/expression/grammar it contains; an exercise lists what it tests. References must resolve — `scripts/validate_learning_document.py` checks this.

## 2. IDs and cross-references

- Sentence IDs encode absolute position: paragraph and sentence, two digits each. Never renumber after batching.
- The other collections are sequential in reading order: first item encountered in paragraph 1 gets `v001`, and so on. If you later insert an item, give it the next unused number and keep reading order approximate — do not renumber existing records, because exercises and notes point at them.
- A word may appear in several sentences. Create one record and list all `sentenceRefs`; do not duplicate the record.

## 3. Vocabulary records

| Field | Required | Rule |
|---|---|---|
| `id` | yes | `v001` format |
| `surface` | yes | Exact substring of the sentence, including inflection and any attached apostrophe/clitic (`l'ai`, `dímelo`) |
| `lemma` | yes | Dictionary citation form. For verbs in Romance/German, the infinitive. For nouns, the singular (German: with article information in notes or `gender`) |
| `pos` | yes | One of the enum values in the schema. Choose the POS *in this sentence* |
| `meaningInContext` | yes | One sentence, in `explanationLanguage`, giving the meaning here — not a list of dictionary senses |
| `morphology` | no | Required in practice for any inflected form that is not predictable from the lemma |
| `pronunciation` | no | IPA when it disambiguates or when the learner cannot infer it; do not guess |
| `gender` | no | Nouns in gendered languages; include plural strategy in notes when irregular |
| `collocations` | no | Two to four high-value partners, all natural |
| `examples` | no | One or two sentences, original, natural, level-appropriate, with translation |
| `commonErrors` | no | Real learner errors, not invented ones |
| `confusions` | no | Near-synonyms or false friends, with the distinction stated |
| `sentenceRefs` | yes | At least one existing sentence ID |
| `priority` | yes | See rubric |
| `confidence` | yes | `high` / `medium` / `low` |
| `needsVerification` | yes | `true` when a native speaker or dictionary should confirm |
| `region` | no | Only when the usage is regionally restricted, and with evidence |
| `externalLevel` | no | Only when a source states it; include `source`. Never assign CEFR yourself |
| `tags` | no | Free tags for filtering (`false-friend`, `irregular`, `colloquial`) |

Good vs. bad:

- Good: `surface: "cobbled"`, `lemma: "cobble"`, `pos: "verb"`, `morphology.description: "past simple of cobble; here part of the phrasal verb cobble together"`.
- Bad: `lemma: "cobbled together"` for the verb `cobble` (the phrasal verb is an expression record), or `pos: "phrase"` when the item is a single inflected verb.
- Bad: `meaningInContext: "to make (a shoe); to assemble"` — that is a dictionary dump, not a contextual gloss.

## 4. Morphology rules

Only explain what is not obvious from the lemma, and explain it precisely.

- **English**: irregular past/participle (`dug` ← `dig`); third-person `-s`; comparative forms when irregular. Do not explain regular `-ed`.
- **French**: gender/number of nouns; verb group; tense/mood/person; auxiliary (`avoir`/`être`); participle agreement (especially with pronominal verbs and preceding direct objects); elision and contraction (`du` = `de + le`); `-er`/`-ir`/irregular patterns. State the agreement trigger, not just the result.
- **Spanish**: gender/number; verb tense/mood/person; stem changes; irregular preterites; participle agreement; clitic pronouns and their order (`dímelo` = `di + me + lo`); `se` type (reflexive, reciprocal, passive, impersonal, accidental).
- **German**: gender; case; strong/weak/mixed adjective declension; plural class; verb tense/person; separable prefix position; participle formation; `Konjunktiv II`; article contraction (`zum` = `zu + dem`).

Never call an inflected form a different lexeme. `Schläuche` is `Schlauch` (plural), not a new word. `fuisteis` is `ir`/`ser` (2pl preterite), not a separate entry unless disambiguation is the teaching point.

## 5. Priority rubric

`priority` is a teaching decision, **not** a frequency claim.

| Value | Meaning | Typical cases |
|---|---|---|
| `high` | A learner at the target level should be able to use this after studying the text | Common word with a context-specific sense; irregular form; idiom that recurs in everyday speech; false friend |
| `medium` | Worth recognizing; productive use is optional | Register-marked but common; collocation that aids naturalness; semi-technical term |
| `low` | Nice to know; passive recognition only | Rare literary word; brand name; highly specific jargon |

Rules:

- At most one third of vocabulary items may be `high`.
- Do not write "most common", "high frequency", or percentage claims. If you have corpus data from the user, cite it; otherwise say nothing.
- An item that is `low` and also `needsVerification` should usually be omitted entirely.

## 6. Confidence and verification

| Value | Use when |
|---|---|
| `high` | Standard, well-attested meaning; you would defend it to a native speaker |
| `medium` | Correct in this context but nuance or register may vary; or the form is ambiguous |
| `low` | Plausible but unverified; regional, dated, or highly colloquial usage; possible OCR corruption |

Set `needsVerification: true` whenever: the item is slang or regionally marked, the translation depends on a disputed parsing, the text is damaged, or your confidence is `low`. These items remain in the output — with a visible marker — rather than being silently promoted or deleted.

Do not use confidence as a hedge for laziness: a standard word you simply did not check is still `high` if you are sure. Reserve `low` for genuine uncertainty.

## 7. Expression records

Required: `text`, `type`, `meaningInContext`, `register`, `priority`, `confidence`, `needsVerification`, `sentenceRefs`.

- `text` must appear verbatim, with the same inflection as in the source. If you generalize to a lemma form, add the observed form in `notes`.
- `literalMeaning` is required for idioms and slang where the literal reading differs; optional elsewhere.
- `type` uses the taxonomy in `idioms-and-slang.md`, with the decision tests applied.
- `register` is required even when `neutral` — silence about register is a common source of learner error.
- `region` + `regionCertainty` only when regional. Never assert "used everywhere" without a reason.
- `sensitivity` for anything potentially offensive, vulgar, or derogatory. `none` is the default for neutral material.

## 8. Grammar records

Required: `id`, `title`, `explanation`, `sentenceRefs`, `confidence`, `needsVerification`.

- `title` names the phenomenon in the learner's terms (`passé composé vs. imparfait`, `se accidental`, `分离动词的框型结构`).
- `explanation` states the rule, then applies it to the quoted sentence. No rule without an in-text example.
- `pattern` is optional: a short schematic (`avoir/être + participe passé`).
- `pitfalls` lists errors learners actually make with this structure in this language.
- Do not include a grammar point merely because it is famous. It must matter for reading this text or for producing similar sentences.

## 9. Optional and empty fields

Optional fields may be omitted entirely or set to `null`/`[]` where the schema allows. Do not populate fields with filler ("N/A", "none", "—") to look complete. An absent field is honest; a filled meaningless field is noise.

Conversely, do not omit required fields because they are hard. If you cannot determine `meaningInContext`, you cannot annotate the item — drop it or mark it `low` with an explicit note.

## 10. Anti-patterns

- Dictionary dump in `meaningInContext`.
- Lemma mistaken for surface form or vice versa.
- Two records for the same lexeme in different inflections.
- Idiom translated word-for-word in the aligned translation.
- `register` given as `formal` for anything written in a newspaper.
- `region` guessed from the spelling of one word.
- CEFR label attached to a word with no source.
- Grammar note with no sentence reference.
- Every item marked `high` priority.
- Slang section padded with standard colloquialisms.
- Confidence `high` on a disputed parsing.
