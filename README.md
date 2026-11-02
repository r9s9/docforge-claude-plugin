# DocForge for Claude

Turn finished Word documents into reusable templates, then let Claude fill
them and check them, in Claude chat, Cowork and Claude Code.

DocForge reads one to five `.docx` files of the same kind and works out what
stays fixed, what changes and what repeats. Fonts, tables, headers and
numbering stay exactly as they were, because DocForge edits the Word file
itself instead of redrawing it. Claude then fills the template from your notes,
an email, a spreadsheet or another document, and the result is a finished
`.docx` in the same layout. When a document comes back edited, Claude checks
it against its template, explains what changed and why it matters, and can
put the boilerplate back.

This plugin is the open-source [DocForge](https://github.com/r9s9/docforge)
engine packaged for Claude. There is no account or API key: Claude itself does
the AI work.

## Skills

| Skill | What it does | Try saying |
|---|---|---|
| **make-template** | Builds a template from example documents. You review the fields, and it saves a versioned template package. | "Make a template from these three invoices" |
| **fill-template** | Fills a template from notes, data or another document. It also edits drafts conversationally and makes many documents from a spreadsheet. | "Fill the invoice template for Initech from this email" |
| **check-document** | Scores a returned document against its template and lists every difference. Claude says which ones matter, and it can restore the boilerplate. | "Does this contract still match our template?" |

Every skill works in Claude chat (with code execution turned on), in Cowork,
and in Claude Code.

## Install

- **claude.ai and Cowork:** find **DocForge** in the plugin directory under
  **Customize > Plugins**. Or upload a zip of this repository with
  **Add > Upload plugin**.
- **Claude Code:**
  ```
  /plugin marketplace add r9s9/docforge-claude-plugin
  /plugin install docforge@docforge
  ```
  A plugin you added on claude.ai also appears in Claude Code automatically.

## How to use it

1. **Make a template.** Attach (or point Claude at) a few finished documents
   of the same kind and ask for a template. Claude proposes the fields, with
   names, types and descriptions, and asks you to confirm.
2. **Keep the package.** In chat you get a `.zip` to keep, plus the
   template as Word files. In Cowork and Claude Code it is saved under
   `docforge-templates/` in your folder.
3. **Fill it.** Give Claude the package and the content. You get a `.docx`, or
   a PDF when LibreOffice is available. Ask for changes in plain words.
4. **Check it.** Give Claude the package and a returned document. You get a
   score, a report and an optional fixed copy.

To try it without documents of your own, ask Claude to "make DocForge demo
documents". The toolkit can write sample invoices, reports and an edited
invoice for the compliance check.

## What it runs, and what it sends

- **Processing:** the skills run a Python toolkit that ships inside the
  plugin, in Claude's code sandbox or on your computer. It is DocForge's own
  document engine plus a command-line wrapper, as readable source.
- **What it sends:** documents are read and written locally. The plugin sends
  nothing to DocForge or to anyone else, has no telemetry, and makes no
  network calls of its own.
- **What it installs:** the engine needs `python-docx`, `docxtpl`, `lxml`,
  `Jinja2`, `pydantic` and `python-dateutil`. Most sandboxes already have all
  but `docxtpl`. When something is missing, Claude installs exactly the
  pinned versions listed in `skills/*/scripts/requirements.txt` from PyPI,
  which is the only network access involved. On your own computer it uses a
  virtual environment when the system Python is managed.
- **PDF export:** optional, using LibreOffice (`soffice`) when it is
  installed.
- **Security:** uploaded files are checked the same way the DocForge web app
  checks them: type and size limits, zip-bomb and path-traversal guards, and
  safe XML parsing. Templates render in a sandboxed Jinja environment.

Requirements: Python 3.10 or newer. In Claude chat, turn on code execution and
file creation.

## Links

- Website and tutorial: [docforge.live](https://www.docforge.live)
- The DocForge app (self-hosted or hosted): [github.com/r9s9/docforge](https://github.com/r9s9/docforge)
- Support: [support@docforge.live](mailto:support@docforge.live)
- Developing this plugin: [DEVELOPMENT.md](DEVELOPMENT.md)

## License

[MIT](LICENSE) © The DocForge Authors
