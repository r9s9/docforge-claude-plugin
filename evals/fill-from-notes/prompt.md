---
description: Build the invoice template, then fill it from a short brief.
tags: [fill-template]
runs: 1
max_turns: 80
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Skill, Bash, Write, Edit]
---

Make some DocForge demo documents in a folder called `demo`, then build an Invoice template that keeps the boilerplate fixed, from `demo/invoice_1.docx` and `demo/invoice_2.docx`, and save it in `docforge-templates/invoice`. Accept sensible fields with clear descriptions; don't stop to ask me about them.

Then fill it for Initech & Partners: invoice INV-2026-200, dated 2 November
2026, with two line items. The first is a discovery workshop, 2 at $900 for
$1,800; the second a prototype build, 1 at $4,500. The total is $6,300.
Save the document as `out/INV-2026-200.docx` and keep the values file you
rendered from as `out/values.json`.
