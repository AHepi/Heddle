---
name: implement
version: 3
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

Outcome: applied.
