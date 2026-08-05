---
name: prevent
version: 1
steps:
  prevent:
    tools: [read_notes, write_notes]
    outcomes: [promoted]
---

## prevent

One prevention per contributing miss from the cause note — no more, no
fewer. A prevention is admissible only if it is one of:

- Mechanical: a check, a CI job, a pin, a limit — something that fires
  without anyone remembering it.
- Owed at a boundary: a named step in a named workflow, so skipping it
  is visible ("the gate runs before every push"), with who owes it.

"Be more careful", "raise awareness", and training are not
preventions; if that is all a miss admits, say so honestly and record
it as an accepted risk instead.

Write the prevention note (write_notes): each prevention names its
motivating incident, its mechanism or boundary, and the single line
you would grep to prove it exists a year from now. If your repo keeps
a traps ledger, this note is the draft entry for it — symptom, cause,
incident, fix — written to be pasted, not rewritten.

Outcome: promoted.
