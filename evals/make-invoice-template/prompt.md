---
description: Build a template from two example invoices.
tags: [make-template, smoke]
runs: 1
max_turns: 60
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Bash, Write, Edit]
---

Make some DocForge demo documents in a folder called `demo`, then build an Invoice template from `demo/invoice_1.docx` and `demo/invoice_2.docx` and save it in `docforge-templates/invoice`. Accept sensible fields with clear descriptions; don't stop to ask me about them.
