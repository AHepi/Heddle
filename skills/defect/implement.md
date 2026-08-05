---
name: implement
version: 6
steps:
  implement:
    tools: [read_code, write_code, write_tests, run_ring]
    outcomes: [applied]
---

## implement

Apply exactly the approved change — the one from the proposal, not an
improved version of it. The approval covered a specific diff; anything
else is unapproved work. If mid-edit you find the approved change is
wrong or insufficient, stop and say so in your summary rather than
silently substituting a better idea.

Cross-routing is strict: an improvement you start wishing for mid-defect
is parked — not implemented. Write the parked note for its future
runner, at park time: one line of WHAT, then a ready-to-run entry
(which flow to enter, one-goal statement, evidence pointers, end state)
so starting it later costs a paste, not an authoring session. One
tranche, one goal.

Mechanics:

- Read the current code first (read_code); apply with write_code. Use
  write_tests only if the approved proposal includes a test change — the
  reproduction test is not yours to weaken.
- Match the surrounding style, naming, and comment density. A fix should
  read like the file always contained it.
- Run the reproduction test (run_ring) before finishing. Report its
  actual output either way — if it still fails, still report `applied`
  honestly with the red output; verify and the flow's bounded retry
  handle iteration. Hiding a red run here only costs a loop later.
- If the approved proposal states a size ceiling, compare the ACTUAL
  edit size against it before finishing — the real diff, not the
  proposal's estimate. Exceeding the ceiling is a stop in the standard
  format (decision in one sentence, priced options, recommendation),
  not a footnote: a ceiling checked only against the estimate trips on
  nothing.

Outcome: applied.
