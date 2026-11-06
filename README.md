# DocForge.live for Claude

Turn finished Word documents into reusable templates, then let Claude fill
them and check them, in Claude chat, Cowork and Claude Code.

DocForge reads one to five `.docx` files of the same kind and works out what
stays fixed, what changes and what repeats. Fonts, tables, headers and
numbering stay exactly as they were, because DocForge edits the Word file
itself instead of redrawing it. Claude then fills the template from your notes,
an email, a spreadsheet or another document, and the result is a finished
`.docx` in the same layout. When a document comes back edited, Claude checks
it against its template, explains what changed and why it matters, and can put
the boilerplate back.

The plugin packages the open-source [DocForge](https://github.com/r9s9/docforge)
engine for Claude. There is no account, no API key and no server: Claude does
the AI work, and your documents stay in Claude's sandbox or on your computer.

## What it does

The plugin has one skill, **docforge**, that covers three workflows. Claude
picks the right one from your request.

| Workflow | What it does |
|---|---|
| **Make a template** | Builds a template from example documents. Claude proposes the fields, you confirm them, and it saves a versioned template package. |
| **Fill a template** | Fills a template from notes, data or another document. It also revises drafts conversationally and makes many documents at once from a spreadsheet. |
| **Check a document** | Scores a returned document against its template and lists every difference. Claude explains which differences matter, and the boilerplate can be restored. |

## Example prompts

Each of these works as written, using the sample documents from the first one:

1. "Make some DocForge demo documents, then build an **Invoice** template from
   invoice_1.docx and invoice_2.docx."
2. "Fill the Invoice template for Initech & Partners: invoice INV-2026-200,
   dated 2 November 2026, with two line items: a discovery workshop, 2 × $900
   = $1,800, and a prototype build, 1 × $4,500 = $4,500. The total is $6,300."
3. "Check invoice_edited.docx against the Invoice template and tell me what
   changed. Then put the original wording back."
4. "Make a status report template from project_report_1.docx and
   project_report_2.docx, then write this month's report from these notes:
   <your notes>."
5. "Make one invoice per row of this CSV with the Invoice template."

## Try it with sample data

You don't need documents of your own. Ask Claude to "make DocForge demo
documents" and the toolkit writes seven files to try every skill on:

- two invoices
- two project status reports
- two compliance reports
- an invoice whose title and payment terms were edited, for the compliance
  check

## Install

- **claude.ai and Cowork:** find **DocForge.live** in the plugin directory
  under **Customize > Plugins**. Or upload a zip of this repository with
  **Add > Upload plugin**.
- **Claude Code:**
  ```
  /plugin marketplace add r9s9/docforge-claude-plugin
  /plugin install docforge-live@docforge-live
  ```
  The skill appears as `/docforge-live:docforge`, though asking in plain words
  works just as well. A plugin
  you added on claude.ai also appears in Claude Code automatically.

In Claude chat, turn on code execution and file creation. The toolkit needs
Python 3.10 or newer.

## How to use it

1. **Make a template.** Give Claude a few finished documents of the same kind.
   It proposes the fields, with names, types and descriptions, and asks you to
   confirm or change them.
2. **Keep the package.** In chat you get a `.zip` to keep, plus the template
   as Word files. In Cowork and Claude Code it is saved under
   `docforge-templates/` in your folder.
3. **Fill it.** Give Claude the package and the content. You get a `.docx`, or
   a PDF when LibreOffice is available. Ask for changes in plain words.
4. **Check it.** Give Claude the package and a returned document. You get a
   score, a report and, if you want it, a copy with the boilerplate restored.

## What it runs, and what it sends

- **Runs locally.** The skills run a Python toolkit that ships inside the
  plugin, in Claude's code sandbox or on your computer. It contains three
  things, all as readable source:
  - DocForge's document engine
  - a command-line wrapper
  - docxtpl, an open-source library for filling Word templates (see
    [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md))
- **Sends nothing.** Documents are read and written locally. The plugin sends
  nothing to DocForge or to anyone else, has no telemetry and makes no network
  calls.
- **Installs nothing, normally.** Claude's sandboxes normally have the
  packages the toolkit needs. If one is missing, Claude tells you, then installs only
  that package at the version pinned in `skills/docforge/scripts/requirements.txt`
  from PyPI. It uses a virtual environment when the system's Python requires
  one.
- **Keeps nothing.** The plugin writes files only where you ask (templates,
  documents, reports) and a scratch folder for the work in progress. It
  retains nothing else.
  - Preferences go into a template's `notes.md`, but only when you ask Claude
    to remember them. It's a plain text file you can edit or delete.
- **Checks uploads.** Files get the same checks as in the DocForge web app:
  type and size limits, zip-bomb and path-traversal guards, and safe XML
  parsing. Templates render in a sandboxed Jinja environment.
- **PDF export** is optional and uses LibreOffice (`soffice`) when it is
  installed.

## Not legal advice

The compliance check compares a document with its template. Claude's
judgement of which differences matter helps you review the document, but it
isn't legal advice. For contracts and other legal, financial or regulated
documents, have a qualified person review material changes before the
document is relied on, signed or sent. Nothing is changed in a document
unless you ask for the fix.

## Limitations

- **Input:** `.docx` only. Convert `.doc` or `.odt` files first; PDFs rarely
  keep their layout, so use the Word original.
- **Size:** one to five examples per template, up to 25 MB per file.
- **Field detection:** two to five examples give the best results. With one
  example, Claude reads the document's structure instead of comparing
  versions. Review the proposed fields before building either way.
- **What stays as-is:** text boxes, shapes, charts and embedded objects stay
  exactly as they are, but their contents don't become fields. Pictures stay
  as in the example unless you choose to make them replaceable (PNG or JPEG).
- **The fix:** it restores boilerplate only and doesn't create tracked
  changes. It can't invent missing values.

## Troubleshooting

| Problem | What to do |
|---|---|
| Claude doesn't use the skills in chat | Turn on code execution and file creation in settings, check the plugin is enabled, and mention a template or DocForge in your request. |
| `doctor` reports missing packages | Let Claude install them; it installs only what is missing. If your organization blocks package downloads, use Claude Code or Cowork on your computer, or ask an admin. |
| "not a DocForge template package" | Attach the `.zip` (or folder) that making the template produced, not just `template.docx`. The package also holds the field definitions. |
| Too few or wrong fields | Add more examples (two to five), or tell Claude which parts change. You can rename, retype or remove fields before building. |
| A value lands in the wrong place, or is missing | Ask Claude to fix that field, or improve the field's description and rebuild the template. |
| No PDF | LibreOffice isn't installed. Open the `.docx` and export it to PDF. |
| Page numbers or a table of contents look stale | Word refreshes them when the document opens; accept its prompt to update fields. |

## What's in this repository

- `skills/docforge/`: the skill. It holds the instructions, the workflow and
  reference rules, and the toolkit in `scripts/`.
- `tools/`, `tests/`, `evals/`, `.github/`: development files. These are the
  build and upstream-sync tools, tests, eval cases and CI. The skill never
  runs them. See [DEVELOPMENT.md](DEVELOPMENT.md).

## Links

- Website and tutorial: [docforge.live](https://www.docforge.live)
- The DocForge app: [github.com/r9s9/docforge](https://github.com/r9s9/docforge)
- Support: [support@docforge.live](mailto:support@docforge.live) or
  [docforge.live/contact](https://www.docforge.live/contact/)
- Privacy: [docforge.live/privacy](https://www.docforge.live/privacy/)

## License

[MIT](LICENSE) © The DocForge Authors. The bundled docxtpl is LGPL-2.1; see
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
