---
description: Check an edited or returned Word document against its DocForge template, explain what changed, and restore the boilerplate if the person agrees.
argument-hint: "[returned .docx] [template package]"
---

# Check a document against its DocForge template

Use this plugin's **docforge** skill. If it isn't loaded yet, load it, or read
its `SKILL.md`, before doing anything else. Then follow its "Check a document"
workflow in `references/check-document.md`, and run the toolkit the way the
skill says. Change the document only when the person agrees to the fix.

The person's request: $ARGUMENTS

If nothing follows the colon, or only a placeholder, use what the person has
said in the conversation. If you still don't have them, ask for:

- the returned or edited `.docx`
- its template package: the `.zip` or folder made with the template, or the
  name of one under `docforge-templates/`
