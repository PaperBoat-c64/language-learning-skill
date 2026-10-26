# Proficiency and Difficulty

How to adapt depth to a learner without inventing levels.

## 1. The rule: no unearned labels

Do **not** attach CEFR levels (A1–C2), frequency ranks, or "most common word" claims to vocabulary, expressions, or texts unless:

- the user supplies the label, or
- a cited source states it, in which case record `externalLevel: {value, source}`.

Reasons: CEFR descriptors are holistic and not defined per word; frequency depends on corpus, genre, and region; a wrong label changes what a learner skips. Honest omission beats plausible-looking fabrication.

You may describe **observable difficulty signals** (below) without assigning a level.

## 2. Observable difficulty signals

Report these as descriptions, not labels:

| Signal | What to look at |
|---|---|
| Lexical density | Ratio of content to function words; number of low-transparency words |
| Morphological complexity | Inflection depth, irregular forms, agreement chains, separable verbs |
| Syntactic depth | Embedding, subordinate clauses, inversion, non-finite clauses |
| Ellipsis and fragmentation | Missing subjects/verbs in speech, headlines, lyrics |
| Idiomaticity | Proportion of non-compositional units |
| Register distance | How far the text is from neutral standard prose |
| Cultural reference | Allusions, institutions, shared knowledge required |
| Orthographic load | Diacritics, `ß`, `¿¡`, elision, non-Latin punctuation |

A useful output sentence: "本段句子较短，但习语密度高，且含两处省略主语的口语结构——词汇不难，理解难点在语用。" This says something true without a fake B2.

## 3. Adaptation matrix

The same text yields different packets for different learners. Adapt **depth and exercise type**, not the source.

| Learner stage | Vocabulary | Expressions | Grammar | Exercises |
|---|---|---|---|---|
| Early (A1–A2 behaviour) | Gloss core lexis and function words; include pronunciation where useful | Only high-value, frequent units; explain literally | Basic agreement, word order, tense formation | Recognition, matching, cloze with options |
| Developing (B1 behaviour) | Gloss non-obvious lexis; add collocations | Include idioms and colloquialisms with register | Tense/aspect choice, pronoun systems, valency | Cloze without options, meaning discrimination |
| Proficient (B2 behaviour) | Focus on nuance, connotation, less common senses | Register, regional variation, productivity | Complex syntax, information structure | Rewriting, register shifting |
| Advanced (C1+ behaviour) | Rare lexis, etymology only with evidence | Stylistic effect, dated/regional marking | Rhetorical syntax, marked constructions | Stylistic comparison, translation critique |

Treat stages as **behavioural descriptions**, not labels printed on the learner.

## 4. Default-adaptive policy

When the level is unknown:

1. Do not ask. Do not block.
2. Annotate for a B1 reader: gloss what is not obvious, skip what is.
3. Attach `priority` to every item (`high`/`medium`/`low`) so the packet is filterable.
4. Explain grammar proportionally: one or two notes per paragraph at most, only where a construction would actually block comprehension or production.
5. State the assumption once: "未指定水平，以下按中级（约 B1）读者默认加注。"
6. Adjust on later turns without regenerating silently — say what you changed.

## 5. When the user names a level

- If they say "I'm a beginner" / "我是初学者", follow the behavioural row.
- If they name an exam (`DELF B1`, `DELE A2`, `Goethe B2`, `TOEFL`), align to the exam's **task types**, not to invented word lists. If the exam's word list matters, ask the user to supply it or cite the official source.
- If they name a CEFR level for the **text** ("this is B2"), accept it as the user's label; do not re-label individual words.
- Do not upgrade or downgrade the user's stated level based on your own guess.

## 6. Text difficulty report

Optional short block at the top of a study packet:

```markdown
**难度观察（非等级评定）**
- 句法：中等；含两个从句和一个倒装。
- 词汇：日常词汇为主，`Küchenboden` 等复合词可拆解。
- 习语：`im Handumdrehen` 一处，需专门讲解。
- 语域：口语叙事，非正式但无俚语。
```

This is descriptive and defensible. It contains no fabricated level.

## 7. Pitfalls

- Calling common words "A1" and rare words "C1" as if the mapping were official.
- Using "advanced" to mean "I found it hard".
- Writing "this word is high-frequency" with no corpus.
- Asking a beginner to produce idioms on the first pass.
- Giving an advanced learner a packet that re-explains the present tense.
- Treating the user's self-reported level as a score to correct.
