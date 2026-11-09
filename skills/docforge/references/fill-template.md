# Fill a template

A DocForge template package holds a Word template plus a description of
every field: what it holds, where it sits, its type and rules. You write the
values; the toolkit renders them into the template. Fonts, tables, headers
and numbering stay exactly as designed, and repeating table rows are added
per item.

Run every command as described under "Run the toolkit" in SKILL.md, and run
`docforge doctor` first.

If there is no template package yet, only finished examples, make one first
(`references/make-template.md`). A `.docx` with `{{ tags }}` alone isn't a
package: the package also carries the field definitions.

## 1. Learn the template

```bash
docforge fields <package>
```

This shows the document type, its sections with their purpose, and every
field with:

- its type
- whether it's required
- its `value_shape`
- its description
- where it sits: `section`, `under_heading`, `label_before`

It also shows any `notes`, the person's standing preferences; follow them.

## 2. Get the content

What to do depends on what the person gave you:

- **Another document of the same kind** (last month's report, a filled copy):

  ```bash
  docforge route-doc <package> <document>.docx --out values.json
  ```

  With `"method": "structural"`, the values were read field by field. Check
  them, and fill any `missing_required` or `rejected` fields from the
  `outline` it includes.

  With `"method": "outline"`, the document is a different kind. Read the
  outline and write the values yourself.

- **Notes, an email, a brief, the conversation, other files:** write the
  values yourself (step 3).

- **Structured data** (JSON, a spreadsheet row): map its keys onto the field
  names.

- **Many records:** see Batch below.

## 3. Write the values

Read `references/writing-rules.md` first. Write a values file in the format
in `references/values-format.md`:

- `values`
- `drafted`: what you wrote from context rather than found
- `skip_sections`: sections deliberately left out, with a reason
- `missing`: required fields with no basis in the content

Never invent names, dates, amounts or other specific facts. Leave them out
and list them as missing.

## 4. Render and read it back

```bash
docforge render <package> --values values.json --out <name>.docx --blocks
```

Check the result:

- `validation`
- `missing_required`
- `unknown_keys` (typos in field names)
- `empty`

Read `blocks` once as the recipient would (see "Read it back" in the writing
rules). If something is wrong, fix the values and render again, but only
once. Add `--pdf` when the person wants a PDF; it needs LibreOffice.

## 5. Hand over the document

Give the person the `.docx` (and PDF) in this same reply, as
"Hand over the files" in SKILL.md describes. In chat, render straight into
the outputs folder. Then tell them, in a few lines:

- which fields you drafted rather than found
- which required facts are missing, and what you need from them to fill those
- which sections you left out, and why

## Refine

When the person asks for changes:

- Edit only the fields concerned in the values file, following "Refining a
  draft" in the writing rules.
- Render again and hand over the new version, the same way.
- Reply with one or two sentences about what changed.

## Batch

For many documents from a spreadsheet or list:

```bash
docforge render <package> --batch rows.csv --out-dir <folder> --name-pattern "{invoice_number}-{customer}"
```

- Check that the column names match the field names first. `fields` lists
  them; rename columns or build a JSON rows file if needed.
- Table and list fields go in as JSON inside a CSV cell.
- Report how many documents were made, and list the rows that failed
  validation with their reasons.
- Hand over the documents: in chat, zip the folder into the outputs folder
  (`docforge zip` works on any folder) and give the person the zip.

## Shared values

Values that apply to every document for one client or project (name,
address, project code) can live in a defaults file. Pass it with
`--defaults shared.json`; per-document values win over it.

## Good to know

- Rendering is deterministic: the same values always produce the same
  document.
- Structured prose survives: blank lines become paragraphs, "- " lines become
  real Word bullets, and `**bold**` becomes bold.
- `include_…` fields switch optional blocks on or off. Sections can be
  skipped whole.
- **Remembered preferences:** only when the person asks you to remember
  something for this template ("always use British spelling"), add it to
  `notes.md` at the package root and tell them you did. It's a plain text file
  in their package that they can read, edit or delete. In chat, re-zip the
  package and deliver it.
