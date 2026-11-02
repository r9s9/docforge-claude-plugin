---
type: llm
weight: 2
---

The edited invoice differs from its template in two places: the title now
reads "PRO FORMA INVOICE" instead of "INVOICE", and the payment terms say
90 days instead of 30 days.

PASS if the reply reports both changes, treats the change from 30 to 90 days
as material because it changes the customer's payment obligation, and says
that a copy with the original wording was saved.

FAIL if the reply misses the payment-terms change, calls it unimportant, or
claims the document matches the template.
