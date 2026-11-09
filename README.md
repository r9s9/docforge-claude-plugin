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

The plugin teaches Claude to use the open-source
[DocForge](https://github.com/r9s9/docforge) engine, which Claude installs from
PyPI as the `docforge-live` package the first time it's needed. There is
nothing to sign up for and no server: Claude does the AI work, and your
documents stay in Claude's sandbox or on your computer.

## What it does

The plugin has one skill, **docforge**, that covers three workflows. Claude
picks the right one from your request. In Cowork and Claude Code you can also
pick the workflow yourself with its command, such as
`/docforge-live:make-template invoice_1.docx invoice_2.docx`. In Claude chat,
just ask in plain words.

| Workflow | Command | What it does |
|---|---|---|
| **Make a template** | `/docforge-live:make-template` | Builds a template from example documents. Claude proposes the fields, you confirm them, and you get the template as Word files plus a versioned template package. |
| **Fill a template** | `/docforge-live:fill-template` | Fills a template from notes, data or another document. It also revises drafts conversationally and makes many documents at once from a spreadsheet. |
| **Check a document** | `/docforge-live:check-document` | Scores a returned document against its template and lists every difference. Claude explains which differences matter, and the boilerplate can be restored. |

Templates come in the DocForge app's two modes:

- **Full template** (the default): every text becomes a field, including
  the text in cover blocks and other tables. New documents get all-new text
  in the original design.
- **Smart detect:** boilerplate stays fixed and only what varies becomes a
  field. Ask for it ("keep the boilerplate fixed") when you'll check returned
  documents against the template, since the check compares their wording
  with the template's fixed text. It works best with two to five examples.

## Example prompts

Each of these works as written, using the sample documents from the first one:

1. "Make some DocForge demo documents, then build an **Invoice** template that
   keeps the boilerplate fixed, from invoice_1.docx and invoice_2.docx."
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
  under **Customize > Plugins**. Or upload a zip of this repository (GitHub's
  **Code > Download ZIP**) with **Customize > Plugins > Add > Upload plugin**.
- **claude.ai, as a single skill:** if your account can't upload plugins,
  upload just the skill with **Customize > Skills > Upload a skill**. That
  uploader needs a zip with `docforge/SKILL.md` at the top: zip the
  `skills/docforge` folder of this repository. The repository zip won't work
  there, because it is a plugin. The skill on its own has no commands, but
  asking in plain words does the same.
- **Claude Code:**
  ```
  /plugin marketplace add r9s9/docforge-claude-plugin
  /plugin install docforge-live@docforge-live
  ```
  The skill appears as `/docforge-live:docforge`, next to the three workflow
  commands, though asking in plain words works just as well. A plugin
  you added on claude.ai also appears in Claude Code automatically.

In Claude chat, turn on code execution and file creation. The toolkit needs
Python 3.10 or newer, and access to PyPI the first time it's installed (see
below).

## How to use it

1. **Make a template.** Give Claude one to five finished documents of the
   same kind, and say if the boilerplate should stay fixed (Smart detect).
   It proposes the fields, with names, types and descriptions, and asks you to
   confirm or change them.
2. **Keep the package.** When the template is built, Claude gives you the
   template as Word files, one with tags and one with readable «Labels». In
   chat you also get a `.zip` to keep. In Cowork and Claude Code the package
   is saved under `docforge-templates/` in your folder.
3. **Fill it.** Give Claude the package and the content. You get a `.docx`, or
   a PDF when LibreOffice is available. Ask for changes in plain words.
4. **Check it.** Give Claude the package and a returned document. You get a
   score, a report and, if you want it, a copy with the boilerplate restored.

## What it runs, and what it sends

- **Runs locally.** The skill runs DocForge's toolkit, the open-source
  `docforge-live` package (MIT; source at
  [github.com/r9s9/docforge-toolkit](https://github.com/r9s9/docforge-toolkit)),
  in Claude's code sandbox or on your computer. It holds DocForge's document
  engine and the command line the skill calls. The plugin itself contains only
  instructions.
- **Downloads one pinned package.** The first time the toolkit is needed,
  Claude tells you, then installs `docforge-live` version 1.0.0 from PyPI with
  the libraries it depends on: python-docx, docxtpl, lxml, Jinja2, pydantic
  and python-dateutil. In Claude chat that happens once per conversation; in
  Cowork and Claude Code once per computer, in a private virtual environment
  when the system's Python requires one.
- **Sends nothing.** Documents are read and written locally. Neither the
  plugin nor the toolkit sends anything to DocForge or to anyone else, and
  there's no telemetry. The download above is the only network use, and it
  sends none of your documents.
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
- **Field detection (Smart detect):** two to five examples give the best
  results. With one example, Claude reads the document's structure instead of
  comparing versions. Review the proposed fields before building either way.
- **Checking a Full template:** a Full template has no fixed wording, so a
  check against it covers structure, formatting and fields, not wording. Make
  a Smart template to check wording.
- **Internet on first use:** installing the toolkit needs access to PyPI.
  Where package downloads are blocked, for example by an organization's
  settings for Claude chat, the plugin can't run.
- **What stays as-is:** text boxes, shapes, charts and embedded objects stay
  exactly as they are, but their contents don't become fields. Pictures stay
  as in the example unless you choose to make them replaceable (PNG or JPEG).
- **The fix:** it restores boilerplate only and doesn't create tracked
  changes. It can't invent missing values.

## Troubleshooting

| Problem | What to do |
|---|---|
| Claude doesn't use the skill in chat | Turn on code execution and file creation in settings, check the plugin or skill is enabled, and mention a template or DocForge in your request. |
| "A skill cannot contain a plugin manifest" or "SKILL.md … not nested deeper" | You uploaded the repository zip to **Customize > Skills**. Upload it to **Customize > Plugins** instead, or upload the skill-only zip (see Install). |
| The toolkit can't be installed | Claude couldn't reach PyPI. In Claude chat, allow network access for package installs in the settings, or ask your admin. In Cowork or Claude Code, install the `docforge-live` package (version 1.0.0) with pip yourself. |
| "not a DocForge template package" | Attach the `.zip` (or folder) that making the template produced, not just `template.docx`. The package also holds the field definitions. |
| Too few or wrong fields | Add more examples (two to five), or tell Claude which parts change. You can rename, retype or remove fields before building. |
| A cover block or another table kept its text | Ask for a Full template, or tell Claude which parts of the table change. Every paragraph in a table cell can be a field, including tables inside cells. |
| Claude finished without giving you the files | Ask for them once, and tell us at support@docforge.live: every workflow should end by handing over its files. |
| A value lands in the wrong place, or is missing | Ask Claude to fix that field, or improve the field's description and rebuild the template. |
| No PDF | LibreOffice isn't installed. Open the `.docx` and export it to PDF. |
| Page numbers or a table of contents look stale | Word refreshes them when the document opens; accept its prompt to update fields. |

## What's in this repository

- `skills/docforge/`: the skill: its instructions and the workflow and
  reference rules.
- `commands/`: the three workflow commands. Each one starts its workflow in
  the skill.
- `evals/`, `.github/`: eval cases and CI. See [DEVELOPMENT.md](DEVELOPMENT.md).

The code the skill runs is in
[r9s9/docforge-toolkit](https://github.com/r9s9/docforge-toolkit).

## Links

- Website and tutorial: [docforge.live](https://www.docforge.live)
- The DocForge app: [github.com/r9s9/docforge](https://github.com/r9s9/docforge)
- Support: [support@docforge.live](mailto:support@docforge.live) or
  [docforge.live/contact](https://www.docforge.live/contact/)
- Security reports: see [SECURITY.md](SECURITY.md)
- Privacy: [docforge.live/privacy](https://www.docforge.live/privacy/)

## License

[MIT](LICENSE) © The DocForge Authors. The `docforge-live` toolkit it installs
is MIT too; its dependencies come from PyPI under their own licenses (docxtpl
is LGPL-2.1).
