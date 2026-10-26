# Output Formats

Five modes share one document model. Only the rendering changes.

## Contents

1. [Mode selection](#1-mode-selection)
2. [Study mode](#2-study-mode)
3. [Compact mode](#3-compact-mode)
4. [Cards mode](#4-cards-mode)
5. [Exercise-sheet mode](#5-exercise-sheet-mode)
6. [JSON mode](#6-json-mode)
7. [Batch output](#7-batch-output)
8. [Unicode and rendering rules](#8-unicode-and-rendering-rules)

## 1. Mode selection

| User signal | Mode |
|---|---|
| "精读", "讲解", "study this", no constraints | `study` |
| "快速看一下", "简版", very short text | `compact` |
| "复习卡片", "Anki", "flashcards" | `cards` |
| "出题", "练习", "quiz me" | `exercise-sheet` |
| "JSON", "structured data", "export" | `json` |
| Unclear | `study` |

State the mode in one line at the top, e.g. `模式：精读（study）`. Do not ask which mode unless the user's request genuinely supports two incompatible readings.

## 2. Study mode

```markdown
# {Title or first line, truncated}

**语言**：法语 → 中文　**文体**：短篇叙事　**模式**：精读　**水平假设**：未指定，按中级默认加注

## 全文译文

{Paragraph-aligned complete translation. No commentary.}

## 逐句对照

**s01-01** {Original sentence, verbatim}
> {Natural translation}
> *直译*（仅在需要时）：{literal gloss}
> 注：{optional note}

**s01-02** …

## 词汇

### v001 · {surface} → {lemma}
- **词性**：{pos}　**语境义**：{meaningInContext}
- **形态**：{morphology}
- **搭配**：{collocations}
- **例句**：{example} — {translation}
- **易错**：{commonErrors / confusions}
- **优先级**：{priority}　**置信度**：{confidence}{，**待核实** if applicable}

## 固定表达与俚语

### e001 · {text}（{type}）
- **语境义**：{meaningInContext}
- **字面义**：{literalMeaning}
- **语域**：{register}　**地区**：{region or 未标注}
- **例句**：{example} — {translation}
- **替换**：{alternatives}
- **优先级**：{priority}　**置信度**：{confidence}

{If none: 本段未发现需要单独讲解的高价值固定表达或俚语。}

## 语法

### g001 · {title}
{Explanation, applied to s01-03.}
- 句式：`{pattern}`
- 易错：{pitfalls}

## 练习

### x001（{type}）{prompt}
A. …　B. …　C. …

## 答案与解析

**x001** {answer} — {explanation}

## 复习卡片

| 正面 | 背面 |
|---|---|
| {surface / expression} | {meaning · morphology · example} |

## 质量检查

{QA table from quality-assurance.md}
```

Rules:

- The aligned reading is the backbone; do not bury it under vocabulary.
- Quote the original exactly, including punctuation and capitalization.
- Keep translations directly under their sentence, prefixed with `>`.
- Number sections in the user's language; keep IDs stable across renderings.
- Put the answer key after all exercises, not inline.

## 3. Compact mode

```markdown
# {Title}

**{source language} → {explanation language}** · {genre} · 简版

## 对照

| ID | 原文 | 译文 |
|---|---|---|
| s01-01 | … | … |

## 重点词汇

| 词形 | 原形 | 语境义 | 优先级 |
|---|---|---|---|
| … | … | … | high |

## 重点表达

| 表达 | 类型 | 语境义 | 语域 |
|---|---|---|---|
| … | … | … | … |

{Optional one-line grammar note.}
```

No exercises, no examples, no QA table in compact mode — but do a silent QA pass and mention any blocking issue found.

## 4. Cards mode

Two renderings: a Markdown table for reading, and a TSV block for import.

### Markdown cards

```markdown
# 复习卡片 · {Title}

## 词汇

**Q:** {surface}（{sentence context}）
**A:** {lemma} · {pos} · {meaningInContext}
{morphology line}
> {example} — {translation}

## 表达

**Q:** {expression}
**A:** {meaningInContext}（{register}）
> {example} — {translation}
```

### Anki TSV

One card per line, fields separated by a tab. Escape tabs and newlines inside fields.

```text
#separator:tab
#html:false
#columns:Front	Back	Tags
{surface}	{lemma} — {meaningInContext}	lang-{code} vocab {priority}
{expression}	{meaningInContext} ({register})	lang-{code} expression {priority}
```

Escaping rules:

- Replace a literal tab in a field with a space.
- Replace line breaks with `<br>` only if `#html:true`; otherwise one card per line and no line breaks.
- Do not include the source sentence unless it fits the card's purpose; a card that requires the whole paragraph is not a card.
- Tags: ASCII, no spaces, lowercase (`lang-fr`, `vocab`, `high`, `idiom`).
- Never put an answer in the question field, including in the example.

## 5. Exercise-sheet mode

```markdown
# 练习 · {Title}

## 一、词义理解
1. …
## 二、语境填空
…
## 三、搭配选择
…
## 四、句子改写
…
## 五、语法辨析
…
## 六、翻译与仿写
…
## 七、口语情境
…

---

## 答案与评分标准

1. **答案**：…
   **解析**：…
   **评分**：{rubric for open items}
```

- Every item references the item/sentence it tests (`（见 v003）`, `（s02-01）`).
- Closed items: one unambiguous answer.
- Open items: rubric with at least two criteria (e.g. "使用目标表达 / 语法正确 / 语域合适").
- Do not reuse the exact example from the vocabulary section as a test item.

## 6. JSON mode

Emit one object conforming to `schemas/learning-document.schema.json`, with arrays filled. Include `qa` with all eleven checks. Then, outside the JSON block, give a two-line human summary (sentence count, item counts) and the validation command result. Do not wrap the JSON in prose that changes its meaning; use a fenced `json` block or a file.

When the user asks for a file, write `{slug}.json` and the matching `{slug}.source.txt` if the source was pasted, so the validator can check integrity.

## 7. Batch output

```markdown
## 批次 1/3 · 第 1–4 段

{rendered content for this batch}

---
## 批次 2/3 · 第 5–8 段
…
```

- Announce batches before the content.
- Repeat the header (title, language) in each batch so batches can be read independently.
- Keep one glossary decision footnote across batches.
- Merge in order. Do not renumber IDs.
- Final QA runs on the merged document, not per batch.

## 8. Unicode and rendering rules

- Output UTF-8. Never transliterate or strip diacritics.
- Preserve the source's apostrophe and quotation glyphs inside quoted original text. Generated prose may use typographic quotes consistently.
- French: keep the source's spacing before `; : ! ?` and inside `« »`.
- Spanish: always keep `¿` and `¡` in quoted original text and in generated Spanish.
- German: keep noun capitalization and `ß`.
- Markdown: escape a literal `|` in table cells as `\|`; avoid tables for long sentences — use the block layout instead.
- Do not put an RTL or invisible control character into the document unless the source has one.
- Code fences around JSON must specify `json`.
