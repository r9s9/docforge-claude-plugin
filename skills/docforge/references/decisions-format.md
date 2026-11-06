# decisions.json

`analyze` writes a starter `decisions.json` into the workspace. Edit it, then
run `review` to check it and `build` to apply it. Every key is optional; an
empty object `{}` builds the proposal exactly as `analyze` made it.

```json
{
  "document_type": "Commercial invoice",
  "sections": [
    {
      "section_key": "header",
      "title": "Invoice details",
      "purpose": "Who is billed, when, and under which number.",
      "expected_content": "Invoice number, issue date, customer",
      "field_names": ["invoice_number", "invoice_date", "customer"]
    }
  ],
  "classifications": [
    {"node_id": "n0004", "field_name": "customer",
     "description": "The company or person being billed."},
    {"node_id": "n0019", "classification": "DYNAMIC_NUMBER", "field_name": "total_due",
     "field_type": "number", "static_prefix": "Total Due: ",
     "description": "Total amount due with currency symbol, e.g. $2,300.00."},
    {"node_id": "n0023", "classification": "FIXED"}
  ],
  "fields": {
    "line_items": {
      "description": "Products or services billed, one row each.",
      "columns": {"qty": {"label": "Quantity", "field_type": "number"}}
    }
  },
  "image_fields": []
}
```

## Keys

**`document_type`.** A plain name for the kind of document.

**`sections`.** Replaces the proposed sections when non-empty. List the
final field names (after any renames); `review` warns about names that don't
exist.

**`classifications`.** Only the nodes you change, by `node_id` from
`outline`. Keys you leave out keep the proposal's value. Allowed keys:

| key | meaning |
|---|---|
| `classification` | one of the classifications in `classification-rules.md` |
| `field_name` | snake_case tag name; required for `DYNAMIC_*` and `REPEATABLE_*` |
| `field_type` | `text`, `multiline_text`, `date`, `person`, `number`, `enum`, `table`, `boolean`. Defaults from the classification |
| `description` | what belongs in the field |
| `static_prefix` / `static_suffix` | label text kept fixed around the value |
| `enum_values` | allowed choices for `DYNAMIC_ENUM` |
| `required` | `false` if documents may leave it empty |
| `optional` | `true` adds an `include_…` switch for content that isn't always present |
| `rationale` | a short note; not shown in the template |

To **remove a field**, set its node's `classification` to `FIXED`: the
example's text stays as-is. To **turn fixed text into a field**, give the
node a dynamic classification and a `field_name`. To **rename**, change
`field_name`.

**`fields`.** Changes to a derived field, by its final name: `label`,
`description`, `required`, `default`, `enum_values`, and `columns` for tables.
Each column is changed by its current name, using `field_name` (rename),
`label`, `field_type` and `required`. To change a field's name or type, edit
its node under `classifications`.

**`image_fields`.** Picture field names (from `analyze`'s `pictures`) that
should be replaceable per document. Unlisted pictures stay as in the example.

## Errors

`review` and `build` reject the file, listing every problem, when:

- a `node_id` is unknown
- a classification or field type is misspelt
- a dynamic node has no `field_name`
- a name isn't snake_case (lowercase letters, digits and `_`, starting with a letter)
- a name is reserved (`item`, `loop`, `if`…)
- one name is used for different kinds of content

Fix the entries and run again.
