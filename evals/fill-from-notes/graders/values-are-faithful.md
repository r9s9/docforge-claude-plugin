---
type: llm
weight: 2
focus:
  source: file
  path: out/values.json
---

These are the values used to fill an invoice. The brief said: Initech &
Partners, invoice INV-2026-200, dated 2 November 2026; a discovery workshop,
2 at $900 = $1,800; a prototype build, 1 at $4,500 = $4,500; total $6,300.

PASS if the values contain that invoice number, that date (any clear format,
including 2026-11-02), Initech & Partners as the customer, exactly those two
line items with matching quantities and amounts, and the $6,300 total.

FAIL if any of those is wrong or missing, or if the values add specific facts
the brief did not give, such as an address, a purchase-order number, tax, or
extra line items.
