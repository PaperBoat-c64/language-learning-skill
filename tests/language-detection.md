# Test — Language Detection

Verifies that `textLanguage` is identified correctly and that ambiguous input is handled without silent guessing.

## How to run

Paste each input into a fresh session with the skill installed, using the trigger prompt shown. Check the packet's `meta.textLanguage` (or the language line in study mode) and the assumptions line.

## Cases

### T-LD-01 — English with French loanwords

**Input**

> The café's naïve décor and its faux-leather chairs made the résumé-writing session feel oddly theatrical.

**Trigger prompt**: "Help me study this text closely."

**Expected**

- `textLanguage: en`
- Loanwords glossed only if selected; `café`, `naïve`, `décor`, `résumé` keep their diacritics.
- No French language rules applied.

**Fail if**

- Detects `fr` because of the accents.
- Strips diacritics "for English".
- Splits `résumé-writing` incorrectly.

### T-LD-02 — French with English borrowing

**Input**

> On a fait un brainstorming, puis chacun a présenté son pitch devant le groupe.

**Trigger prompt**: "精读这段法语。"

**Expected**

- `textLanguage: fr`
- `brainstorming` and `pitch` treated as borrowings, explained as such, not as French errors.
- French elision and agreement rules applied.

**Fail if**

- Detects `en` because of the two English-looking nouns.
- Flags `brainstorming` as a spelling error.

### T-LD-03 — Spanish questions and exclamations

**Input**

> ¿De verdad vas a venir? ¡No me lo puedo creer!

**Trigger prompt**: "Explain this to me in Chinese."

**Expected**

- `textLanguage: es`
- Two sentences, `¿` and `¡` preserved.
- Register note: informal spoken.

**Fail if**

- Drops `¿`/`¡` or treats them as decoration.
- Splits at `?` then leaves `¡No…` mis-segmented.

### T-LD-04 — German with ß, umlauts, and a separable verb

**Input**

> Er öffnete die Tür, zog die Schuhe aus und stellte sie in den Flur. Draußen war es schon kühl.

**Trigger prompt**: "Study this German text."

**Expected**

- `textLanguage: de`
- `ausziehen` recognized as separable (`zog … aus`), not two unrelated words.
- `ß`/`ü` preserved.

**Fail if**

- Detects `en` or `nl`.
- Translates `zog` alone without the prefix.

### T-LD-05 — Mixed Spanish/English social post

**Input**

> Terminé el proyecto por fin 🎉 so proud of the team!! Mañana celebramos.

**Trigger prompt**: "Help me read this."

**Expected**

- One clarifying question about the primary language **or** a stated assumption ("以西班牙语为主，英语部分作为借语处理"), then proceed.
- Emoji preserved.
- Code-switching noted, not "corrected".

**Fail if**

- Silently picks one language and ignores the other half.
- Deletes the emoji.
- Asks more than one question.

### T-LD-06 — Single ambiguous word

**Input**

> Salut.

**Trigger prompt**: "What does this mean?"

**Expected**

- Recognizes French greeting; gives the contextual meaning and a register note.
- Does not build a full 10-step packet for one word unless asked.
- Does not invent a language when another is plausible; if genuinely ambiguous (e.g. a name), asks once.

**Fail if**

- Produces a full packet with fabricated sentences.
- Confuses it with an English word without saying so.

### T-LD-07 — No text supplied

**Input**: "Help me study something in French."

**Expected**

- Asks the user to paste the text (one short question or instruction).
- Does not fabricate a text or generate a generic lesson.

**Fail if**

- Invents a passage and studies it.
- Runs the full workflow on nothing.

## Pass criteria

All seven cases behave as specified. A detection error in any case fails the suite. Question count: at most one per run, except T-LD-07 where asking for the missing input is the task itself.
