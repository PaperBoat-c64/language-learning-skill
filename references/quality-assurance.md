# Quality Assurance

QA is a separate pass with its own output, not a feeling of confidence. Run every check, record the result, fix only what failed, and disclose what could not be verified.

## 1. The eleven checks

| ID | Check | Pass criterion |
|---|---|---|
| C01 | Source integrity | Concatenated sentence text reproduces the source under whitespace normalization; no paragraph, heading, speaker label, or punctuation dropped |
| C02 | Alignment | Exactly one translation per sentence; no merged/split pairs; paragraph translations cover all paragraphs |
| C03 | Lemma and form | Every `surface` exists in its sentence; every `lemma` is a citation form; no inflected form misclassified as a new lexeme |
| C04 | Contextual sense | Each gloss matches this sentence; no dictionary dumps; polysemy resolved with a reason |
| C05 | Grammar accuracy | Each rule is correct for the language and accurately describes this sentence |
| C06 | Expression classification | Type passes the tests in `idioms-and-slang.md`; literal vs. contextual meaning separated for idioms |
| C07 | Register and region | Every expression has a register; regional labels have a basis or are marked `unverified`; sensitivity flagged |
| C08 | Redundancy | No duplicate records for the same lexeme; no over-annotation of trivial words; counts proportionate to text |
| C09 | Unsupported claims | No CEFR/frequency/"most common"/etymology claim without a source |
| C10 | Schema conformance | JSON validates against `schemas/`; IDs unique; references resolve |
| C11 | Exercise answerability | Every exercise has a checkable answer or explicit rubric; each tests a taught item |

## 2. How to run each check

### C01 — Source integrity

Re-read the source and the segmented model side by side. Normalize both by collapsing whitespace. Compare. Then check the things whitespace comparison hides:

- apostrophe style (`'` vs. `’`) — the model must use the source's;
- quotation marks (`« »`, `„ “`, `" "`);
- dashes (`–` vs. `—` vs. `-`);
- Spanish `¿` `¡`;
- German `ß` vs. `ss`;
- emoji, hashtags, mentions, timestamps in social posts;
- headings and list markers.

Machine check: `python3 scripts/validate_learning_document.py doc.json --source source.txt`.

### C02 — Alignment

Read only the translations, in order, without the source. Do they form a coherent text? Then read pairs. Failures: a translation that silently covers two sentences; a sentence with no translation; a translation attached to the wrong ID after batching.

### C03 — Lemma and form

For each vocabulary item, search its `surface` in the sentence. Then verify the lemma by applying the language's inflection rules (`languages/<code>.md`). Watch for:

- separable German verbs (`hin` at the end of the clause);
- French elision (`l'ai` → `le` + `ai`, lemma `avoir`);
- Spanish clitics (`dímelo` → `decir` + `me` + `lo`);
- English contractions (`won't` → `will not`).

### C04 — Contextual sense

For each gloss, ask: could this word mean something else here? If yes, is the chosen sense justified by a collocate, syntax, or discourse signal? Replace any gloss that lists senses instead of selecting one.

### C05 — Grammar accuracy

For every grammar note, verify three things: the rule is true; the rule applies to the quoted span; the metalinguistic terms are the ones used for this language. Common errors: applying English tense labels to Romance aspect; calling German `würde` a future; calling Spanish `se` reflexive when it is passive/impersonal.

### C06 — Expression classification

Re-run the decision procedure for each item. Any item that fails its type tests is reclassified or dropped. Idioms must show literal ≠ contextual.

### C07 — Register and region

Every expression must carry `register`. Check that region claims are either supported by the source's own variety, a cited dictionary, or marked `unverified`. Check sensitivity for vulgar or derogatory items.

### C08 — Redundancy

- Two records for `cobbled` and `cobble`? Merge.
- Glossing `the`, `and`, `very`? Drop.
- Twelve expressions in a six-sentence text? Prune to the real ones.
- Repeating the same grammar note per sentence? Consolidate with multiple refs.

### C09 — Unsupported claims

Search the output for: `A1`, `A2`, `B1`, `B2`, `C1`, `C2`, `高频`, `最常见`, `most common`, `high-frequency`, `%`, `源自`, `词源`. Each hit needs a source or must be removed. Do not replace a fabricated level with a vaguer fabricated claim ("basic", "advanced") attached to a word.

### C10 — Schema conformance

```bash
python3 scripts/validate_learning_document.py path/to/document.json --source path/to/source.txt
python3 scripts/check_skill_assets.py
```

The validator checks structure, ID uniqueness, reference resolution, and source integrity. Schema validation runs when `jsonschema` is installed; otherwise the script's built-in structural checks apply. State which mode ran.

### C11 — Exercise answerability

For each exercise: can a competent speaker mark an answer right or wrong? Open-ended exercises need a rubric with at least two criteria. Every exercise must reference the sentence/vocabulary/expression it tests, and that item must exist in the packet.

## 3. Severity and the fix loop

| Severity | Examples | Action |
|---|---|---|
| Blocking | Source altered; wrong lemma; fabricated fact; misaligned translations; exercise with no answer | Fix before delivery |
| Major | Wrong register label; idiom translated literally; grammar note that misdescribes the sentence | Fix before delivery |
| Minor | Redundant gloss; awkward example sentence; missing optional collocation | Fix if cheap, else disclose |
| Cosmetic | Formatting, ordering, heading style | Fix in rendering |

Fix the **stage** that failed, then re-run the checks that depend on it. Example: a corrected segmentation invalidates C01, C02, and every sentence reference — re-run those, not the vocabulary register check.

Do not rewrite the whole packet to fix one item; that destroys verified work and introduces new errors.

## 4. Report format

Include this at the end of a study packet, or in `qa` for JSON:

```markdown
## 质量检查

| 检查 | 结果 | 说明 |
|---|---|---|
| C01 原文完整性 | 通过 | 字符数 1,204；段落 4；句子 12 |
| C02 对照对齐 | 通过 | 12/12 |
| C03 词形与原形 | 通过 | 2 处不规则形式已注明 |
| C04 语境词义 | 通过 | — |
| C05 语法解释 | 通过 | — |
| C06 表达分类 | 通过 | `cobble together` 判为短语动词 |
| C07 语域与地区 | 部分 | `on first-name terms` 的地区倾向标记为未核实 |
| C08 冗余 | 通过 | — |
| C09 无依据声明 | 通过 | 未标注 CEFR |
| C10 Schema | 通过 | jsonschema 校验 |
| C11 练习可判定 | 通过 | 5 题均有答案 |

未核实项：1 处（表达的地区偏好）。其余检查均已通过。
```

## 5. Honesty rules

- A check you did not run is `unverified`, not `pass`.
- A check that could not run because of input limits (image-only source, truncated text) is `not-applicable` with a reason.
- If `jsonschema` was unavailable, say "结构检查通过；未执行正式 JSON Schema 校验".
- If a native-speaker judgment would be needed, say so and keep `needsVerification: true`.
- Never write "all checks passed" when any row is `unverified`, `partial`, or `not-applicable`.

## 6. Machine validation quick reference

```bash
# required asset tree, frontmatter, internal links
python3 scripts/check_skill_assets.py

# one learning document, with source-integrity check
python3 scripts/validate_learning_document.py examples/english/example.json \
  --source examples/english/source.txt

# every shipped example
for f in examples/*/example.json; do
  python3 scripts/validate_learning_document.py "$f" --source "${f%/*}/source.txt" || exit 1
done
```
