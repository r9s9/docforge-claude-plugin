# Judging a compliance report

`check` aligns the document with the template's structure and lists every
difference. The score is deterministic; your job is to say which differences
actually matter.

## The score

`score` (0–100) combines three dimensions:

- **structure**: is the fixed boilerplate present and unchanged?
- **fields**: are the required fields present and well formed?
- **tables**: do repeating tables exist with the right shape?

The grade is `pass` at 90 and above, `warning` from 70, otherwise `fail`. When
you supply verdicts, a fourth dimension, **semantic**, shows the share of
differences that are *not* material. The deterministic score itself never
changes.

## Kinds of difference

| kind | default severity | meaning |
|---|---|---|
| `missing_fixed` | error | a boilerplate paragraph is gone |
| `changed_fixed` | warning | boilerplate was reworded (under 90% similar) |
| `changed_fixed_minor` | info | boilerplate differs only slightly (90% similar or more), e.g. "30 days" became "90 days". The score counts it as matching, so judge it carefully |
| `missing_field` | error or info | a required field (error) or optional field (info) has no value |
| `format` | warning | a field's value breaks its rule (not a date, not a number, not an allowed choice) |
| `missing_table` | error | a repeating table is gone |
| `table_shape` | warning | a table's columns changed, or it has no data rows |

## Material or benign

For each difference, decide whether it is a **material** compliance problem or
a benign one, and say why in one specific sentence. Don't restate the
difference.

Your verdicts help a person review the document; they are not legal advice.
Say so when you report on contracts or other legal, financial or regulated
documents, and recommend a qualified review of material changes.

- **Material**:
  - changed obligations, amounts, deadlines, parties or scope
  - missing required content
  - altered legal or boilerplate meaning, including a single changed number
    or negation in a clause
- **Benign**:
  - whitespace, casing, punctuation, reordering
  - synonyms that keep the meaning
  - an expected variable value
- **Usually benign (`info`)**: a changed value in a legitimately variable
  field.
- **Usually material (`error`)**: missing or altered required boilerplate or
  obligations.

Severity: `error` for material problems that make the document
non-compliant, `warning` for material but minor ones, `info` for benign ones.

## Verdicts file

```json
{
  "verdicts": [
    {"index": 0, "material": true, "severity": "error",
     "rationale": "The payment window tripled from 30 to 90 days, changing the customer's obligation."},
    {"index": 1, "material": false, "severity": "info",
     "rationale": "Only the capitalisation of the heading changed."}
  ],
  "summary": "One material change to the payment terms."
}
```

`index` is the difference's `index` in `check`'s output. Then:

```bash
check <package> <document> --verdicts verdicts.json --markdown report.md
```

This merges your verdicts into the report: the severities, your rationale and
the semantic dimension.

## What fix does

`fix` restores **boilerplate only**:

- reworded fixed paragraphs get the template's wording back
- removed ones are re-inserted where they belong

Field values, extra content and formatting are left exactly as they are.

- By default it restores paragraphs under 90% similar to the template, the
  same as the DocForge web app.
- Add `--strict` to also restore `changed_fixed_minor` differences. Use it
  when you judged one of those material and the person wants the template's
  wording back.

Fix can't supply missing field values or rebuild a table. Those need the
author, or the fill-template skill.
