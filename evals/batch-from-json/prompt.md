---
description: Make one document per record.
tags: [fill-template, batch]
runs: 1
max_turns: 80
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Skill, Bash, Write, Edit]
---

Make some DocForge demo documents in a folder called `demo`, then build an Invoice template that keeps the boilerplate fixed, from `demo/invoice_1.docx` and `demo/invoice_2.docx`, and save it in `docforge-templates/invoice`. Accept sensible fields with clear descriptions; don't stop to ask me about them.

Then make one invoice per record below, saved in `out/batch/`:

```json
[
  {"invoice_number": "INV-301", "invoice_date": "2026-11-03", "customer": "Acme & Co",
   "line_items": [{"description": "Audit", "qty": "1", "unit_price": "$800.00", "amount": "$800.00"}],
   "total_due": "$800.00"},
  {"invoice_number": "INV-302", "invoice_date": "2026-11-04", "customer": "Globex LLC",
   "line_items": [{"description": "Training", "qty": "3", "unit_price": "$300.00", "amount": "$900.00"}],
   "total_due": "$900.00"},
  {"invoice_number": "INV-303", "invoice_date": "2026-11-05", "customer": "Initech",
   "line_items": [{"description": "Support", "qty": "2", "unit_price": "$400.00", "amount": "$800.00"}],
   "total_due": "$800.00"}
]
```
