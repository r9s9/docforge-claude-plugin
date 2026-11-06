# Make a template

DocForge reads example Word documents, compares them, and builds a template
that keeps the original Word file's design: fonts, tables, headers, footers
and numbering. Only the variable parts become `{{ tags }}`.

The toolkit does the deterministic work: reading, comparing, building. You do
the judgement: deciding what is boilerplate and what is content, naming the
fields, and describing them.

Run every command as described under "Run the toolkit" in SKILL.md, and run
`docforge doctor` first.

## 1. Gather the examples

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

## 2. Analyze

```bash
docforge analyze example1.docx example2.docx --work <workdir> [--mode full]
```

Use a new scratch folder for `<workdir>`. The summary shows:

- the guessed document type
- how elements were classified
- the proposed fields, each with an example value
- `needs_review`: the elements the deterministic pass was unsure of

## 3. Review the proposal

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

## 4. Write decisions

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

## 5. Confirm with the person

Show the fields as a short table: name, what it holds, type, required, and
the example value. Mention briefly what stays fixed. Ask if anything should
change: renames, a field that should stay fixed, fixed text that should vary,
or required versus optional. Apply changes to `decisions.json` and run
`review` again.

To show the actual template first:

```bash
docforge preview --work <workdir> --out <file>.docx [--tags] [--pdf]
```

## 6. Build the package

```bash
docforge build --work <workdir> --name "<Template name>" --out <package-folder> [--zip <file>.zip]
```

Building into an existing package folder adds the next version; earlier
versions are kept. `references/package-format.md` describes the package.

## 7. Deliver

- **Chat:** save the zip, `template.docx` and `with-labels.docx` in the
  outputs folder. Say: "attach the .zip next time to fill or check documents
  with it".
- **Cowork and Claude Code:** point to the package folder and its
  `with-labels.docx`.

Summarize in two or three sentences: the document type, how many fields
there are, and what stays fixed. Offer to fill a first document
(`references/fill-template.md`).

## Good to know

- `template.docx` is a standard docxtpl template, usable outside DocForge.
- A table of contents follows its headings, and Word refreshes page numbers
  when the document opens.
- Pictures stay exactly as in the example unless listed in `image_fields`.
- Only when the person asks you to remember a preference for documents from
  this template, add it to `notes.md` at the package root and tell them you
  did (see `references/package-format.md`).
