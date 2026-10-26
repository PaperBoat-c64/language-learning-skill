# Prompt — Quality Review

Used in Step 9. An independent pass over a finished packet. It must not assume the earlier stages were correct.

## When to use

Always, before delivery. Also on request ("check this packet").

## Required inputs

- The full draft packet
- The original source, verbatim
- `{{TEXT_LANGUAGE}}` and language rules
- The document JSON if one exists

## Prompt

```text
You are a reviewer checking a language-learning packet. You did not write it. Your job is to find errors, not to praise it.

Source (verbatim):
"""
{{SOURCE}}
"""

Draft packet:
"""
{{DRAFT}}
"""

Run the eleven checks from references/quality-assurance.md, in order:
C01 source integrity
C02 alignment
C03 lemma and form
C04 contextual sense
C05 grammar accuracy
C06 expression classification
C07 register and region
C08 redundancy
C09 unsupported claims
C10 schema conformance
C11 exercise answerability

For each check output:
| ID | result (pass / fail / unverified / not-applicable) | evidence |

Rules:
- Cite the exact span or ID for every failure. "Some translations seem off" is not a finding.
- Distinguish "wrong" from "I would have chosen differently". Only the former is a failure.
- Do not fix the text in this pass. Report first.
- Do not mark pass if you could not verify (e.g. no access to the source, damaged input).
- Do not invent a native-speaker judgment; if one is needed, mark unverified.

Then produce:
## Blocking issues
1. {check} — {what} — {where} — {suggested stage to fix}

## Major issues
…

## Minor issues
…

## Disclosed uncertainties
…

## Verdict
- ready / ready-with-disclosures / not-ready
- one-paragraph honest summary.

Fix policy: repair the failing stage and re-run only the dependent checks. Do not rewrite verified content.
```

## Output contract

The QA table, ranked issues, disclosures, verdict. No rewritten packet.

## Self-check

- [ ] Every finding cites an ID or exact span.
- [ ] Unverifiable items marked unverified, not pass.
- [ ] No fabricated native-speaker claims.
- [ ] Fix suggestions name the stage, not "rewrite everything".
- [ ] Verdict matches the disclosed result.
- [ ] No praise padding.
