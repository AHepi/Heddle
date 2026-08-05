---
name: classify
version: 1
steps:
  classify:
    tools: [read_notes]
    outcomes: [defect, change, question]
---

## classify

Read the clarified note (read_notes) and pick exactly one:

- `defect` — behavior that is wrong today: there is an expectation with
  a source, and observed behavior that misses it.
- `change` — behavior that should be different tomorrow: new or altered
  functionality, with no claim that anything is currently broken.
- `question` — the requester wants an answer, not a change to the
  system. Answering is the whole deliverable.

Decide from the clarified words, not from what you suspect the code
looks like. If the note contains both a defect and a change, classify
the one the requester led with — the other becomes a second triage
pass, not a blended ticket. One tranche, one goal.

Outcome: defect, change, or question.
