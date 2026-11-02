---
name: check-document
description: Check an edited or returned Word document against its DocForge template, and put its boilerplate back in shape. Use when the user wants to know whether a .docx still matches its template, asks for a compliance or deviation report, wants to see what someone changed in the fixed wording (terms, clauses, disclaimers, standard sections), or wants the template's boilerplate restored while keeping the filled-in values. Needs the DocForge template package (folder or .zip) the document was made from, usually built with the make-template skill.
---

# Check a document

DocForge aligns a document with its template's structure and scores three
things: whether the fixed boilerplate is intact, whether the required fields
are present and well formed, and whether repeating tables have the right
shape. You judge which differences actually matter. The toolkit can then
restore the boilerplate without touching anything else.

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
  folder (usually `/mnt/user-data/outputs`). A template package arrives as a
  `.zip`; commands accept it directly.
- **Cowork and Claude Code:** packages are usually in
  `docforge-templates/<name>/` in the working folder.

You need the template package and the document to check, as `.docx`. If the
person only has the original template as a Word file, build a package first
with the make-template skill, using that file as the example.

## Workflow

### 1. Check

```bash
docforge check <package> <document>.docx
```

This prints:

- the score and grade
- the dimensions: structure, fields, tables
- whether the document is `fixable`
- the differences, each with an `index`, `kind`, `severity`, and
  `expected`/`found` text

`references/judging-rules.md` explains each kind.

### 2. Judge each difference

Read `references/judging-rules.md`. For each difference, decide whether it is
material or benign, with one specific sentence of rationale. Look hardest at:

- `changed_fixed_minor`: small edits to boilerplate that the score counts as
  matching, such as a changed number, date or negation in a clause.
- `missing_fixed`: removed clauses.

Write the verdicts file, then produce the final report:

```bash
docforge check <package> <document>.docx --verdicts verdicts.json --markdown <name>-report.md
```

### 3. Report

Lead with the answer: compliant or not, the score and grade, and how many
material problems there are. Then:

- **Material problems:** list each in plain words. Say what the template
  requires and what the document says instead.
- **Benign differences:** summarize in one line.
- **The report file:** deliver the Markdown report. Its side-by-side table
  shows every changed part.

Say plainly what the check is: a comparison with the template that helps a
person review the document. Your verdicts are not legal advice. For contracts
and other legal, financial or regulated documents, recommend that a qualified
person review any material change before the document is relied on, signed
or sent.

### 4. Offer the fix

If the report is `fixable`, offer the fix and run it only when the person
agrees:

```bash
docforge fix <package> <document>.docx --out <document>-fixed.docx [--strict]
```

- **What it restores:** the template's boilerplate only. Field values, extra
  content and formatting stay as they are.
- **When to add `--strict`:** when a `changed_fixed_minor` difference was
  judged material and should be reverted too.
- **What it reports:** how many fixes it applied, and the score before and
  after.

Deliver the fixed document. Mention anything fix can't repair (missing
values, table problems) and who needs to supply it.

## Good to know

- **Deterministic score:** the same document always gets the same score.
  Your verdicts add the "semantic" dimension and the rationale; they never
  change the deterministic score.
- **No tracked changes:** fix doesn't add tracked changes. To show the
  restorations as revisions, compare the fixed and original files in Word
  (Review > Compare).
- **Extra content:** content the template doesn't have appears as `extra` in
  the side-by-side table. It isn't penalized; mention it if it looks
  significant.
