# Values files

`render` takes the values for one document from a JSON file:

```json
{
  "values": {
    "invoice_number": "INV-2026-101",
    "invoice_date": "2026-11-02",
    "customer": "Initech & Partners",
    "line_items": [
      {"description": "Discovery workshop", "qty": "2", "unit_price": "$900.00", "amount": "$1,800.00"}
    ],
    "summary": "Highlights this month:\n\n- Pilot finished **two weeks early**\n- 140 users trained",
    "include_appendix": false
  },
  "drafted": ["summary"],
  "skip_sections": [{"section_key": "risks", "reason": "No risks were reported this month."}],
  "missing": ["purchase_order"]
}
```

- **`values`.** Field name to value. Leave a field out (or `null`) to leave it
  empty; a field with a `default` keeps the template's own wording.
- **`drafted`.** Fields you wrote from context rather than found in the
  content. Reported back so you can flag them to the person.
- **`skip_sections`.** Sections to leave out of this document on purpose, by
  `section_key`, with a reason. A section toggle hides the whole span.
- **`missing`.** Required fields the content gave no basis for.

A flat object of field values (no `values` key) also works, as does DocForge's
writer format (`{"placements": [{"field_name", "value", …}]}`).

## Shapes by field

`fields` prints each field's `value_shape`. In short:

| field | value |
|---|---|
| text | a string; `multiline_text` may use blank lines, `- ` bullets and `**bold**` |
| date | `"2026-11-02"`, unless the description asks for another format |
| number | `"1250.00"`, or a formatted amount such as `"$1,250.00"` if the template shows one |
| enum | one of `allowed_values` |
| person | a name |
| table | a list of row objects keyed by the column `field_name`s |
| repeatable section | a list of strings, one per paragraph or point |
| repeatable block | a list of `{"title": …, "body": …}` |
| boolean (`include_…`) | `true` or `false` |
| image | a path to a PNG or JPEG file (relative paths resolve from the values file's folder). Leave it out to keep the original picture |

## Shared values (project metadata)

`--defaults shared.json` takes a flat object of values used for every
document unless the values file sets them, such as a client's name and
address. Keys that aren't fields pass through as extra template variables.

## Many documents at once

`render <package> --batch <rows> --out-dir <folder>` makes one document per
row, with no AI involved. It reads three kinds of rows file:

- **CSV**: one column per field. A cell holding JSON (a list of table rows, or
  a list of points) is parsed, e.g.
  `"[{""description"": ""Audit"", ""qty"": ""1""}]"`.
- **JSON**: a list of objects, or `{"rows": [...]}`.
- **JSONL**: one object per line.

`--name-pattern '{invoice_number}-{customer}'` names files from row values;
otherwise they are numbered. Each row may also use the full values-file shape
above. The summary lists rows that failed validation with the reasons.
