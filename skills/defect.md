---
name: defect
version: 1
steps:
  capture_goal:
    tools: []
    outcomes: [done]
  diagnose:
    tools: [read_map, read_code, read_tests, run_ring]
    outcomes: [diagnosed, inconclusive]
  reproduce:
    tools: [read_code, read_tests, write_tests, run_ring]
    outcomes: [reproduced, cannot_reproduce]
  propose:
    tools: [read_map, read_code, run_ring]
    outcomes: [proposed]
  implement:
    tools: [read_map, read_code, read_tests, write_code, write_tests, run_ring]
    outcomes: [done]
  verify:
    tools: [run_ring, run_gate]
    outcomes: [green, red]
---

## capture_goal
State the goal in one sentence: what is broken, for whom, observed where.
One tranche, one goal. If a change is wished for mid-defect, park it by
saying so in the record — do not implement it here.

## diagnose
Diagnosis comes from the record before code reading. Read the actual error
artifact — the log line, the failing test output — before theorizing;
recorded misattributions cluster exactly where readers skipped it. Name the
instrument for every claim ("the gate says 1 failed", not "it seems to be").
Check TRAPS.md for a recurrence before inventing a new cause. Return
'inconclusive' rather than a guess; inconclusive is a result.

## reproduce
Write the smallest test that goes red for the diagnosed cause and paste its
real output. A reproduction that cannot fail proves nothing — mutation-prove
it: break the guarded thing, watch it go red, restore. If you cannot
reproduce, that is the finding; return 'cannot_reproduce' and record what
was tried.

## propose
State the narrowest repair boundary: which files move, which must not move.
Forecast protected-surface contact now, in writing — discovering it at
validation is several commits too late. Prefer fixing readers over changing
recorded formats: old evidence must stay valid forever. Price the fix:
files touched, protected contact, size, risk.

## implement
Make the repair inside the proposed boundary. Keep the reproduction test —
it becomes a durable check pinned to committed evidence, anchored to
meaning (behavior, structure, counts), never to line numbers, with the
motivating incident named in its docstring. Never weaken an assertion to
get green. Run the ring while iterating.

## verify
Run the gate: the full suite, zero failures the only acceptable result.
Paste the real output. Validation never patches — if the gate is red,
return 'red' with the output; the flow routes it back, and the failure is
recorded verbatim. Name the commit the verdict was measured at.
