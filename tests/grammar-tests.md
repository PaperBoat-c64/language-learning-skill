# Test — Grammar Explanations

Verifies that explanations are correct for the specific language and sentence, and that English categories are not transferred.

## How to run

Give each text with the prompt "Explain the grammar that matters here." Check the grammar notes against the expected content and the rejection list.

## Cases

### T-GR-01 — French participle agreement with a preceding direct object

**Input**

> Les fleurs que j'ai cueillies ce matin sont déjà fanées.

**Expected**

- Notes `cueillies`: passé composé with `avoir`; the participle agrees with the preceding direct object `que` (= les fleurs), hence feminine plural.
- Does not say the participle agrees with the subject `j'`.

**Fail if**

- "Agrees with the subject."
- Calls it an adjective.
- Ignores the agreement entirely when it is the sentence's main teaching point.

### T-GR-02 — French pronominal agreement: direct vs. indirect reflexive

**Input**

> Elle s'est lavée, puis elle s'est lavé les mains.

**Expected**

- `lavée` agrees because the reflexive pronoun is the direct object.
- `lavé` does not agree because `les mains` is the direct object and `se` is indirect.
- The contrast is stated explicitly.

**Fail if**

- Says both agree with the subject.
- Says neither agrees.
- Explains only one of the two forms.

### T-GR-03 — Spanish accidental se vs. reflexive

**Input**

> Se me rompió el vaso y se lavó las manos.

**Expected**

- First `se`: accidental/benefactive-like `se` with dative `me`; the glass broke unintentionally, the speaker is affected. Not reflexive.
- Second `se`: reflexive/indirect with `las manos` as direct object.
- The two `se` are distinguished.

**Fail if**

- Calls both reflexive.
- Translates the first as "he broke the glass himself" without noting the accident reading.
- Invents an agent.

### T-GR-04 — Spanish deber vs. deber de

**Input**

> Debe de estar en casa, pero debe entregar el informe mañana.

**Expected**

- `debe de estar` = probability ("he's probably at home").
- `debe entregar` = obligation ("he has to submit").
- The presence/absence of `de` is the teaching point.

**Fail if**

- Treats both as obligation.
- Says the difference is only stylistic.
- Calls `deber de` old-fashioned or incorrect (it is standard for probability).

### T-GR-05 — German V2 after a fronted subordinate clause

**Input**

> Als der Regen aufhörte, gingen wir nach Hause.

**Expected**

- `als` clause is verb-final (`aufhörte`).
- The clause occupies position 1, so the main clause inverts: `gingen wir`.
- The rule is stated as word order, not emphasis.

**Fail if**

- Says the main clause subject comes first because it is "more important".
- Explains `gingen` as past tense only, without the inversion.
- Produces `…, wir gingen nach Hause` as correct German.

### T-GR-06 — German separable verb in a subordinate clause

**Input**

> Ich weiß, dass er morgen ankommt, aber er ruft nicht an.

**Expected**

- In the subordinate clause, `ankommt` stays together and is final.
- In the main clause, `ruft … an` is split, prefix final.
- The contrast is explicit.

**Fail if**

- Splits `an…kommt` in the subordinate clause.
- Leaves `anruft` unsplit in the main clause.
- Treats `an` as a preposition in `ruft nicht an`.

### T-GR-07 — English past perfect needs a reference point

**Input**

> By the time the guests arrived, she had finished cooking.

**Expected**

- `had finished` is anterior to `arrived`; `by the time` supplies the reference point.
- Does not say past perfect simply means "a long time ago".

**Fail if**

- "Past perfect is for things that happened longer ago."
- Recommends past perfect for every past action.
- Misses the `by the time` trigger.

### T-GR-08 — No cross-language contamination

**Input**

> Il a plu toute la nuit.

**Expected**

- French: passé composé with `avoir`, impersonal `il`, `pleuvoir`; `toute la nuit` duration.
- No mention of Spanish `se`, German case, or English progressive as if they applied.

**Fail if**

- Explains French `il` as an English dummy subject without noting it is impersonal.
- Applies German word-order rules.
- Introduces a CEFR level.

### T-GR-09 — Grammar point must be instantiated

**Input**

> The cat sat on the mat.

**Trigger prompt**: "Explain the grammar."

**Expected**

- Zero to two notes (e.g. definite article, prepositional phrase), not a survey of English tenses.
- No note about the passive, conditionals, or relative clauses, which do not occur.

**Fail if**

- Produces a general grammar lecture.
- Explains structures absent from the sentence.

## Pass criteria

All nine cases. A grammar error in T-GR-01 through T-GR-06 is blocking. T-GR-09 fails if more than two grammar points are produced for a sentence this simple.
