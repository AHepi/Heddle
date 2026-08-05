---
name: goal
version: 3
steps:
  goal:
    tools: [read_map, write_map]
    outcomes: [captured]
---

## goal

State the defect precisely before anyone looks at code. A defect is a gap
between expectation and observation; write both halves:

- Expected: what should happen, and on whose authority. Name the REQ- doc
  if one covers the behavior, or the CON-/INV- contract being violated.
  If the only source is the reporter's words, say "source: reporter" — an
  invented authority is worse than an honest thin one.
- Actual: what happens instead, as an observable — an error message, a
  wrong value, a missing file. Not an interpretation ("it's broken") and
  not a presumed cause ("the loader is wrong"); causes belong to diagnose.

One or two sentences total, written into the map (write_map) so later
steps and the RESULTS entry can quote it. If the expectation has no
written source, note that a REQ- doc should exist — but do not write one
now; that is the change flow's job.

Outcome: captured.
