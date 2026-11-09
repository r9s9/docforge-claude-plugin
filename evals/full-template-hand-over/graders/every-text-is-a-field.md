---
type: llm
weight: 2
focus:
  source: file
  path: docforge-templates/report/1/field_definitions.json
---

These are the fields of a template made from one monthly project status
report, in DocForge's default mode ("Full template"), where every text in the
document becomes a field.

PASS if there are fields for the report title, the project name, the report
date, the author, the introduction, the summary and the confidentiality
note, and the task-status table is one table field.

FAIL if the title, the summary or the confidentiality note is missing, which
would mean text was left fixed, or if descriptions are empty or generic.
