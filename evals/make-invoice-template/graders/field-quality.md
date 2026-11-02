---
type: llm
weight: 2
focus:
  source: file
  path: docforge-templates/invoice/1/field_definitions.json
---

These are the fields of a template built from two sample invoices.

PASS if all of these hold:
- there is a field for the invoice number, the invoice date, the customer being billed, and the total due
- the line items are one table field whose columns cover description, quantity, unit price and amount
- every field has a specific description of what belongs in it, not a generic phrase
- field names are short snake_case names (one to three words)

FAIL if any required field is missing, if fixed text such as the "INVOICE" title,
the "Line Items" or "Terms" headings, or the payment-terms sentence became a
field, or if descriptions are empty or generic.
