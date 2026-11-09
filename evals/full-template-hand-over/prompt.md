---
description: Make a template from one report with the default mode, and hand over the files unasked.
tags: [make-template, full-template]
runs: 1
max_turns: 60
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Bash, Write, Edit]
---

Make some DocForge demo documents in a folder called `demo`, then make a
template from `demo/project_report_1.docx` and save it in
`docforge-templates/report`. Accept sensible fields with clear descriptions;
don't stop to ask me about them.
