---
name: make-template
description: Turn finished Word documents into a reusable DocForge template. Use when the user has one to five .docx files of the same kind (invoices, contracts, reports, letters, proposals, statements of work) and wants a template, a fillable form, or "more documents like these". It works out what stays fixed, what changes and what repeats, keeps the original fonts, tables, headers and numbering, and saves a versioned template package with {{ tags }}. Also use to update an existing DocForge template with new examples, or to make a "full template" where every text becomes a field.
---

# Make a template

DocForge reads example Word documents, compares them, and builds a template
that keeps the original Word file's design: fonts, tables, headers, footers
and numbering. Only the variable parts become `{{ tags }}`.

The toolkit does the deterministic work: reading, comparing, building. You do
the judgement: deciding what is boilerplate and what is content, naming the
fields, and describing them.

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
  `/mnt/user-data/uploads`). Work in a scratch folder. Deliver files by saving
  them in the outputs folder (usually `/mnt/user-data/outputs`).
- **Cowork and Claude Code:** use the working folder. Keep templates in
  `docforge-templates/<name>/` unless the person says otherwise.

Documents stay where they are: the toolkit runs locally and sends nothing
anywhere.

## Workflow

### 1. Gather the examples

- Get 1–5 finished `.docx` files of the same kind. More examples (2–5) make
  better templates, because DocForge sees what actually changes.
- Convert `.doc` or `.odt` files first with
  `soffice --headless --convert-to docx <file>`.
- Turn PDFs into Word with care: the layout rarely survives, so ask for the
  Word original.

Pick the mode:

- **smart** (default): boilerplate stays fixed and only what varies becomes
  a field.
- **full**: every text becomes a field, for a blank skeleton of the
  document's design.

### 2. Analyze

```bash
docforge analyze example1.docx example2.docx --work <workdir> [--mode full]
```

Use a new scratch folder for `<workdir>`. The summary shows:

- the guessed document type
- how elements were classified
- the proposed fields, each with an example value
- `needs_review`: the elements the deterministic pass was unsure of

### 3. Review the proposal

Read `references/classification-rules.md` before deciding anything. Then:

- `docforge outline --work <workdir>` lists the document in order, with each
  element's proposal and its diff evidence: how it varied across the examples.
  For long documents, page with `--offset`, or start with `--only review`.
- `docforge node --work <workdir> <node_id>` shows full text, formatting and
  evidence.
- `docforge neighbors --work <workdir> <node_id>` shows what surrounds an
  element.
- `docforge evidence --work <workdir> <node_id>` shows every variant across
  the examples.

Check every flagged element and anything the rules say is commonly wrong:

- boilerplate made into a field, or content left fixed
- labels inside values (use `static_prefix`)
- layout tables made repeatable
- vague names and descriptions

Also give the template sections that follow its headings.

### 4. Write decisions

Edit `<workdir>/decisions.json`; the format is in
`references/decisions-format.md`. Record only changes, by `node_id`, plus:

- the document type
- the sections
- field-level edits: labels, descriptions, table columns
- any pictures that should be replaceable

Write a specific description for every field. They guide every document
filled from this template later.

Then check it:

```bash
docforge review --work <workdir>
```

Fix any errors and act on the warnings.

### 5. Confirm with the person

Show the fields as a short table: name, what it holds, type, required, and
the example value. Mention briefly what stays fixed. Ask if anything should
change: renames, a field that should stay fixed, fixed text that should vary,
or required versus optional. Apply changes to `decisions.json` and run
`review` again.

To show the actual template first:

```bash
docforge preview --work <workdir> --out <file>.docx [--tags] [--pdf]
```

### 6. Build the package

```bash
docforge build --work <workdir> --name "<Template name>" --out <package-folder> [--zip <file>.zip]
```

Building into an existing package folder adds the next version; earlier
versions are kept. `references/package-format.md` describes the package.

### 7. Deliver

- **Chat:** save the zip, `template.docx` and `with-labels.docx` in the
  outputs folder. Say: "attach the .zip next time to fill or check documents
  with it".
- **Cowork and Claude Code:** point to the package folder and its
  `with-labels.docx`.

Summarize in two or three sentences: the document type, how many fields
there are, and what stays fixed. Offer to fill a first document with the
fill-template skill.

## Good to know

- `template.docx` is a standard docxtpl template, usable outside DocForge.
- A table of contents follows its headings, and Word refreshes page numbers
  when the document opens.
- Pictures stay exactly as in the example unless listed in `image_fields`.
- Only when the person asks you to remember a preference for documents from
  this template, add it to `notes.md` at the package root and tell them you
  did (see `references/package-format.md`).
