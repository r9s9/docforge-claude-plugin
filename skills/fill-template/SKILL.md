---
name: fill-template
description: Fill a DocForge template to produce a finished Word document in the template's exact layout. Use when the user has a DocForge template package (a folder or .zip with docforge-template.json, usually made with the make-template skill) and wants a new document from notes, an email, a brief, a conversation, JSON or spreadsheet data, or another document of the same kind; when they want to revise a generated draft ("shorten the summary", "make it more formal"); or when they want many documents at once from a CSV or JSON list (mail merge).
---

# Fill a template

A DocForge template package holds a Word template plus a description of
every field: what it holds, where it sits, its type and rules. You write the
values; the toolkit renders them into the template. Fonts, tables, headers
and numbering stay exactly as designed, and repeating table rows are added
per item.

## Run the toolkit

Below, `docforge` means:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/docforge_cli.py
```

- If `${CLAUDE_SKILL_DIR}` appears literally in this text, use the path of
  the folder this SKILL.md is in. The CLI is at `scripts/docforge_cli.py`
  there.
- On Windows, use `python` instead of `python3`.
- Every command prints one JSON object. Errors come back as
  `{"ok": false, "error", "hint"}`.

**First run `docforge doctor`.** It normally reports `"ok": true`, because the
plugin bundles the one package Claude's sandboxes tend to lack. If it reports
`"ok": false`:

1. Tell the person which packages are missing and why they're needed.
2. Run the `install` command it prints. It installs only those packages, in a
   virtual environment when the system's Python requires one.
3. If the result includes `then_run_with`, use that Python instead of
   `python3` for every later command.

Don't install anything else.

## Where files are

- **Chat:** attachments are in the uploads folder (usually
  `/mnt/user-data/uploads`). Deliver files by saving them in the outputs
  folder (usually `/mnt/user-data/outputs`).
  - A template package arrives as a `.zip`. You can pass the zip straight to
    any command.
  - To change the package (its `notes.md`), unzip it into a scratch folder,
    work on the folder, and re-zip it with `docforge zip`.
- **Cowork and Claude Code:** packages are usually in
  `docforge-templates/<name>/` in the working folder.

If there is no template package yet, only finished examples, make one first
with the make-template skill. A `.docx` with `{{ tags }}` alone isn't a
package: the package also carries the field definitions.

## Workflow

### 1. Learn the template

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

### 2. Get the content

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

### 3. Write the values

Read `references/writing-rules.md` first. Write a values file in the format
in `references/values-format.md`:

- `values`
- `drafted`: what you wrote from context rather than found
- `skip_sections`: sections deliberately left out, with a reason
- `missing`: required fields with no basis in the content

Never invent names, dates, amounts or other specific facts. Leave them out
and list them as missing.

### 4. Render and read it back

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

### 5. Deliver

Save the `.docx` (and PDF) where the person can get it. Then tell them, in a
few lines:

- which fields you drafted rather than found
- which required facts are missing, and what you need from them to fill those
- which sections you left out, and why

### Refine

When the person asks for changes:

- Edit only the fields concerned in the values file, following "Refining a
  draft" in the writing rules.
- Render again and deliver the new version.
- Reply with one or two sentences about what changed.

### Batch

For many documents from a spreadsheet or list:

```bash
docforge render <package> --batch rows.csv --out-dir <folder> --name-pattern "{invoice_number}-{customer}"
```

- Check that the column names match the field names first. `fields` lists
  them; rename columns or build a JSON rows file if needed.
- Table and list fields go in as JSON inside a CSV cell.
- Report how many documents were made, and list the rows that failed
  validation with their reasons.
- In chat, zip the folder for download.

### Shared values

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
