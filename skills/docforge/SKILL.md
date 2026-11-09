---
name: docforge
description: Make, fill and check Word templates with DocForge, keeping the original layout (fonts, tables, headers, numbering). Use when the user has one to five finished .docx files of the same kind (invoices, contracts, reports, letters, proposals) and wants a reusable template or "more documents like these"; when they have a DocForge template package (a folder or .zip with docforge-template.json) and want a new document from notes, an email, a brief, data, another document of the same kind, or one document per row of a spreadsheet, or want such a draft revised; or when they want an edited or returned .docx checked against its template, a deviation or compliance report, or its boilerplate restored while keeping the filled-in values.
---

# DocForge

DocForge turns finished Word documents into reusable templates, fills them in
the original layout, and checks returned documents against them. It edits the
Word file itself, so fonts, tables, headers, footers and numbering stay exactly
as they were.

DocForge's toolkit (see "Run the toolkit") does the deterministic work: reading, comparing,
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

The deterministic work is done by DocForge's toolkit, the open-source
`docforge-live` package on PyPI. This skill uses version 1.0.0. Below,
`docforge` means:

```bash
python3 -m docforge.toolkit
```

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

### Set it up first

Run `docforge doctor`. When it prints JSON with `"ok": true` and
`"toolkit": "1.0.0"`, the toolkit is ready. Otherwise (no module named
`docforge`, or another version):

1. If the folder `~/.docforge-venv` exists, try its Python:
   `~/.docforge-venv/bin/python -m docforge.toolkit doctor`. If that reports
   `"toolkit": "1.0.0"`, use `~/.docforge-venv/bin/python` instead of
   `python3` from now on.
2. Otherwise tell the person, in one sentence, that you're installing
   DocForge's toolkit (the `docforge-live` package) from PyPI. Then install
   exactly this version:

   ```bash
   python3 -m pip install --quiet "docforge-live==1.0.0"
   ```

3. If pip refuses because the environment is "externally managed", install it
   into a private virtual environment instead, and use that Python instead of
   `python3` from now on:

   ```bash
   python3 -m venv --system-site-packages ~/.docforge-venv
   ~/.docforge-venv/bin/python -m pip install --quiet "docforge-live==1.0.0"
   ```

   On Windows, that Python is `%USERPROFILE%\.docforge-venv\Scripts\python.exe`.
4. Run `docforge doctor` again. If it still reports `"ok": false`, run the
   `install` command it prints, which installs only the missing pieces, and
   if it prints `then_run_with`, use that Python.

If the install can't reach PyPI, stop and tell the person that DocForge's
toolkit couldn't be downloaded here. In Claude chat, network access for
package installs can be off in the settings or turned off by an admin. In
Cowork and Claude Code, they can install `docforge-live==1.0.0` with pip
themselves. Install nothing else, and no other version.

## Where files are

- **Chat:**
  - **Attachments** are in the uploads folder, usually
    `/mnt/user-data/uploads`. If they aren't there, find them with:

    ```bash
    find / \( -path /proc -o -path /sys \) -prune -o \( -name '*.docx' -o -name '*.zip' \) -mmin -720 -print 2>/dev/null | head -20
    ```

  - **Work** in a scratch folder.
  - **Deliver files** in the outputs folder, usually
    `/mnt/user-data/outputs` (see "Hand over the files").
  - A template package arrives as a `.zip`, which every command accepts
    directly.
  - To change a package (its `notes.md`), unzip it into a scratch folder, work
    on the folder, and re-zip it with `docforge zip`.
- **Cowork and Claude Code:** use the working folder. Templates live in
  `docforge-templates/<name>/` unless the person keeps them elsewhere.

Documents stay where they are: the toolkit runs locally and sends nothing
anywhere.

## Hand over the files

Every workflow ends by giving the person its files, in the same reply as your
summary. Never end with only a summary, and don't wait to be asked:

| Workflow | Files |
|---|---|
| Make a template | the template `.docx`, the "with labels" `.docx`, and in chat the package `.zip` (`build` lists them in `hand_over`) |
| Fill a template | the filled `.docx` (and PDF); for a batch, the folder or its `.zip` |
| Check a document | the Markdown report, and the fixed `.docx` when the fix ran |

How:

- **Chat:** the files must be in the outputs folder (usually
  `/mnt/user-data/outputs`); `build --deliver` and `--zip` can write them
  there directly. If the app gives you a tool to present or share files with
  the person (such as `present_files`), call it with every file. Otherwise
  name each file in your reply. If there is no outputs folder, save them
  where the app shows files to the person and say where.
- **Cowork and Claude Code:** if the app gives you a tool to send or present
  files to the person, use it for every file. Otherwise end your reply with
  each file's full path, one per line, as a link where the app shows links.
