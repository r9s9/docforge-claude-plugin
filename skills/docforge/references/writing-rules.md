# Writing rules

How to write the values for a document. These are the rules DocForge's own
document writer follows. The goal is one coherent document, not a form
filled in field by field.

## Write the document, not the fields

- **Read everything first**, then decide what belongs where. A field's place
  tells you what it is for: its section, the heading above it, the label
  beside it. `fields` reports these as `section`, `under_heading` and
  `label_before`. The section's `purpose` tells you what to write there.
- **Say each thing once.** Never repeat the same sentence, fact or phrasing in
  two fields. A summary summarises what the body says; it doesn't copy it.
- **Keep one voice** across the document: consistent tense, person and
  register, so the result doesn't read as assembled fragments.
- **Fit the neighbours.** Write each section so it follows from the one before
  it, without restating what that section established.
- **Skip, don't pad.** A section with no real content goes in
  `skip_sections` with a reason. Never fill it with filler or with content
  restated from elsewhere.
- **Use `include_…` switches.** A boolean field named `include_…` turns an
  optional block on or off. Set it to `false` when the content clearly has
  nothing for that block; otherwise leave it out.
- **Use only the template's field names.** Never invent fields; `render` lists
  unknown keys.

## Facts

- **Never invent specific facts** the content doesn't support: names, dates,
  totals, quantities, prices, commitments or contact details. Leave the field
  out and list it in `missing`.
- **Drafting is allowed when there is a basis.** If the content supports a
  required passage but doesn't spell it out (a summary, a short description of
  scope), write it from the content and list the field in `drafted`. Prefer a
  clearly marked draft over an empty required section, because an empty
  required field leaves a gap in the document.
- **Read the template's own text.** A field with a `default` already holds the
  template's own wording (a section label); leave it out to keep that wording.

## Types and shapes

- **Dates** as YYYY-MM-DD, unless the field's description asks for another
  format.
- **Numbers and amounts** normalised and consistent, keeping the currency
  symbol if the description or example shows one.
- **Enum fields** take only a value from `allowed_values`.
- **Repeatable tables** take a list of rows, each keyed by the table's
  `columns` field names.
- **Repeatable sections** take a list of strings, one per distinct point or
  paragraph, when the content naturally breaks into more than one.
- **Repeatable blocks** take a list of `{"title", "body"}` objects, one per
  repeated item. The body may use the formatting below.

## Formatting inside a text value

Kept simple on purpose:

- Separate paragraphs with a blank line. Don't write one long run-on block.
- Start a line with "- " for a bullet, or "1. " for a numbered item.
- Wrap words in **double asterisks** for bold, *single asterisks* for italic.
- Nothing else: no headings, tables, links or code. The template supplies the
  design; the value supplies only the words and their structure.

## Read it back (once)

After `render --blocks`, read the document the way its recipient would. Fix
only what would actually bother them:

- a section that promises content and delivers none
- the same substance said twice (two mentions of one subject are fine)
- content under the wrong heading
- text whose shape is wrong for its place: a paragraph where a short value
  belongs, or a run-on block where there should be points

Don't count the template's fixed boilerplate as a problem, and don't polish
wording. If something needs fixing, make **one** corrective pass and render
again. Rewrite loops chasing taste cost time and converge on nothing.

## Refining a draft

When the person asks for a change ("shorten the summary", "more formal",
"move the vendor risk into scope"):

- **Change only what was asked.** "Shorten the summary" means rewriting that
  one field, not every field.
- **If the request is ambiguous**, make the smallest reasonable change and say
  what you assumed.
- **If it can't be done** (the content doesn't support it, or no such field
  exists), change nothing and say why.
- **Keep the established voice**, and don't restyle untouched parts by side
  effect.
- **Reply in one or two sentences** about what changed. Don't paste the
  document back.
