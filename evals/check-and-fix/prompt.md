---
description: Spot an obvious and a subtle change to boilerplate, then restore it.
tags: [check-document]
runs: 1
max_turns: 80
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Skill, Bash, Write, Edit]
---

Make some DocForge demo documents in a folder called `demo`, then build an Invoice template from `demo/invoice_1.docx` and `demo/invoice_2.docx` and save it in `docforge-templates/invoice`. Accept sensible fields with clear descriptions; don't stop to ask me about them.

Then check `demo/invoice_edited.docx` against that template. Tell me what
changed and whether it matters, and save a copy with the template's original
wording restored as `out/invoice_fixed.docx`.
