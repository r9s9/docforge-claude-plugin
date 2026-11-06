---
description: Fill a DocForge template from notes, an email, data, another document or a spreadsheet, in the template's original Word layout.
argument-hint: "[template package] [content, or a spreadsheet for one document per row]"
---

# Fill a DocForge template

Use this plugin's **docforge** skill. If it isn't loaded yet, load it, or read
its `SKILL.md`, before doing anything else. Then follow its "Fill a template"
workflow in `references/fill-template.md`, and run the toolkit the way the
skill says.

The person's request: $ARGUMENTS

If nothing follows the colon, or only a placeholder, use what the person has
said in the conversation. If you still don't have them, ask for:

- the template package: the `.zip` or folder made with the template, or the
  name of one under `docforge-templates/`
- the content to fill it from: notes, an email, data, another document, or a
  spreadsheet for one document per row
