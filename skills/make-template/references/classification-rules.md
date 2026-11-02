# Classification rules

How to decide, element by element, what a template keeps and what it leaves
to be filled. These are the rules DocForge's own analyst model follows; apply
them when reviewing the proposal from `analyze`.

## The classifications

| classification | Use for | field_type |
|---|---|---|
| `FIXED` | Boilerplate that reads the same in every document: titles, labels, legal clauses, layout tables | none |
| `DYNAMIC_TEXT` | A value or passage that changes per document | `text`, or `multiline_text` for prose |
| `DYNAMIC_DATE` | A date | `date` |
| `DYNAMIC_PERSON` | A person's or organisation's name | `person` |
| `DYNAMIC_NUMBER` | An amount, quantity, rate or percentage | `number` |
| `DYNAMIC_ENUM` | One of a known set of choices (status, priority, region). List them in `enum_values` | `enum` |
| `REPEATABLE_TABLE` | A table whose rows are several of the same kind of thing (line items, revisions, tasks), with a stable header | `table` |
| `REPEATABLE_SECTION` | Consecutive paragraphs or bullets on one topic, whose number varies | `multiline_text` |
| `REPEATABLE_BLOCK` | A heading plus the paragraph under it that repeat as a unit (one per project, finding, milestone) | `table` |
| `AUTO_FIELD` | Page numbers, a table of contents, other Word fields | none |
| `UNKNOWN` | Avoid. Decide instead | none |

## Rules

- **Evidence first.** With two or more examples, the diff evidence is the
  primary signal. Text identical in every sample is `FIXED`. Values that change
  are `DYNAMIC_*`. A table whose header is stable but whose rows or row count
  vary is a `REPEATABLE_TABLE`.
- **One example only.** No evidence of change is not evidence of boilerplate.
  Read the document structurally. Its skeleton is the headings, labels and
  legal boilerplate. Its content (the paragraphs and lists under those
  headings) is what a new document of this type replaces, so make that content
  `DYNAMIC`. A template whose body is all `FIXED` reproduces one document and
  can't be filled.
- **Labels stay, values vary.** When a value follows a label in the same
  paragraph ("Invoice Date: 2026-06-01"), keep the label in `static_prefix`
  ("Invoice Date: ", trailing space included) and make only the value dynamic.
  Use `static_suffix` the same way for trailing text.
- **Word's own content.** Use `AUTO_FIELD` for page numbers, tables of
  contents and Word fields. Never give `FIXED` or `AUTO_FIELD` content a
  `field_name`.
- **Layout tables are fixed.** A table that lays out a page (a cover block, an
  address panel, a signature grid, a logo cell) is `FIXED`, however many cells
  it has. Turning it into a loop destroys the layout when a document has no
  rows for it. `REPEATABLE_TABLE` is only for rows of the same kind.
- **Furniture is fixed.** Short labels that name a part of the document
  rather than say anything ("TABLE OF CONTENTS", "REVISIONS", "APPENDICES",
  "REFERENCES") are `FIXED`.
- **Spacing is fixed.** An empty paragraph is spacing: leave it `FIXED` with no
  `field_name`.
- **Repeated blocks.** When a heading and the paragraph under it clearly repeat
  as a unit across the document, classify both as `REPEATABLE_BLOCK` with the
  same `field_name`. The heading is the item's title and the paragraph its
  body. Use this only for a genuinely repeating group; a one-off heading
  followed by prose is two ordinary elements.
- **Optional content.** Content present in some examples but missing from
  others gets `"optional": true`. The template then has an `include_…` switch
  for it.
- **Required.** Set `"required": false` for fields that are legitimately empty
  in some documents.

## Field names and descriptions

- **`field_name`** is snake_case, unique and short: 1 to 3 words, at most 24
  characters, no section numbers (`key_findings`, not
  `f_1_2_key_findings_identified`). It becomes the tag a person reads in the
  template. Name it after the element's role, not after the example's value.
- Give every dynamic and repeatable field a **description** that says what
  content belongs there and what kind it is, grounded in the example. "The
  session's learning objectives, as 2–3 short bullet points" works; "text
  content for this section" doesn't. Summarize the example's nature instead of
  quoting it at length. Descriptions are what Claude reads later to fill the
  template, so specific ones produce better documents.
- Use the **same name on two nodes** only when they must always show the same
  value (a client name in the header and in the body).

## What to review

Look hardest at the nodes `outline --only review` lists:

- confidence below 0.6
- UNKNOWN
- fields with no description

For those, correct:

- fixed text that should be a field, and fields that should be fixed
- wrong field types
- labels left inside a value (missing `static_prefix`)
- vague descriptions
- duplicate or clumsy names

## Sections

Sections describe the document as a reader would see it, and they make
filling coherent. Each section has:

- `section_key`: snake_case and stable, usually after its heading
- `title`
- `purpose`: what this part of the document is for
- `expected_content`: what belongs in it
- `field_names`: the final field names it holds (use the new names after a rename)
- optionally `related_sections`

A section can be left out of a generated document on purpose (its "toggle"),
so group fields the way the document groups them.

## "Full template" mode

In `--mode full` every text becomes a field and no original text survives:

- Every non-empty text element is `DYNAMIC_*` or `REPEATABLE_*`. Only Word
  auto-fields and pictures stay fixed. Don't change anything back to `FIXED`;
  the toolkit re-applies this rule after your decisions.
- Headings become `DYNAMIC_TEXT` fields named after their role
  (`scope_title`).
- Body paragraphs become `multiline_text`. Consecutive paragraphs on one topic
  under the same heading share one `field_name`, and list items do the same.
- `static_prefix` and `static_suffix` are always empty, so a value holds its
  whole line, label included ("Report Date: 2026-11-02"). Type such fields
  `text`, not `date` or `number`.
- Focus your review on good names, types and specific descriptions.

## Pictures

Every picture is kept exactly as in the example (logos, signatures, stamps).
To make one replaceable per document, list its name from `analyze`'s
`pictures` in `image_fields`.
