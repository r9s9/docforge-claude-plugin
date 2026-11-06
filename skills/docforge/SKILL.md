---
name: docforge
description: Make, fill and check Word templates with DocForge, keeping the original layout (fonts, tables, headers, numbering). Use when the user has one to five finished .docx files of the same kind (invoices, contracts, reports, letters, proposals) and wants a reusable template or "more documents like these"; when they have a DocForge template package (a folder or .zip with docforge-template.json) and want a new document from notes, an email, a brief, data, another document of the same kind, or one document per row of a spreadsheet, or want such a draft revised; or when they want an edited or returned .docx checked against its template, a deviation or compliance report, or its boilerplate restored while keeping the filled-in values.
---

# DocForge

DocForge turns finished Word documents into reusable templates, fills them in
the original layout, and checks returned documents against them. It edits the
Word file itself, so fonts, tables, headers, footers and numbering stay exactly
as they were.

The toolkit in `scripts/` does the deterministic work: reading, comparing,
building, rendering, scoring. You do the judgement: what is boilerplate and
what is content, what to write in each field, and which differences matter.

## Pick the workflow

Read the one that fits the request before running anything:

| The person wants to… | Read |
|---|---|
| Make a template from example documents, or add a new version | `references/make-template.md` |
| Fill a template: from notes, data, another document or a spreadsheet; or revise a draft | `references/fill-template.md` |
| Check a document against its template, get a report, or restore its boilerplate | `references/check-document.md` |

A request can span several, such as making a template and then filling it.
Follow them in order.

The workflows point to these reference files at the step that needs each one:

- `references/classification-rules.md`: what becomes a field and what stays
  fixed, plus field names and descriptions (making a template)
- `references/decisions-format.md`: the `decisions.json` file you write when
  reviewing a template
- `references/package-format.md`: what a template package holds, versions,
  and `notes.md`
- `references/writing-rules.md`: how to write field values, read the result
  back and refine a draft (filling)
- `references/values-format.md`: the values file, value shapes, and batch rows
- `references/judging-rules.md`: kinds of difference, material versus benign,
  and what the fix does (checking)

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
- Commands that help in any workflow:
  - `docforge demo --out <folder>` writes sample documents (invoices,
    reports, and an edited invoice) for trying DocForge without your own
    files.
  - `docforge read <document>.docx` prints a block-id outline of any
    document.
  - `docforge sample <package> --out <file>.docx` shows a template with
    «Label» values.
  - `docforge pdf <file>.docx` converts to PDF when LibreOffice is
    installed.

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
  - A template package arrives as a `.zip`, which every command accepts
    directly.
  - To change a package (its `notes.md`), unzip it into a scratch folder, work
    on the folder, and re-zip it with `docforge zip`.
- **Cowork and Claude Code:** use the working folder. Templates live in
  `docforge-templates/<name>/` unless the person keeps them elsewhere.

Documents stay where they are: the toolkit runs locally and sends nothing
anywhere.
