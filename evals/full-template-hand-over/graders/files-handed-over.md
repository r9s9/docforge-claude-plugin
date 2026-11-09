---
type: llm
weight: 2
---

The person asked for a template and should get its files without asking
again.

PASS if the final reply gives the person the template as a Word file and the
readable "with labels" Word file, by path or link (for example
`docforge-templates/report/1/template.docx` and `with-labels.docx`), and
summarizes the fields.

FAIL if the reply only summarizes, or only names the package folder, without
pointing to the two Word files.
