---
name: verify
version: 4
steps:
  verify:
    tools: [run_wheel, run_ring, run_gate]
    outcomes: [green, red]
---

## verify

Prove the fix works and nothing else broke. Three instruments, cheapest
first, each one's actual output quoted:

1. The smoke wheel (run_wheel) — proves the harness itself still turns.
   Red wheel means the repo is broken below this defect: report `red`
   with what the wheel printed.
2. The reproduction ring (run_ring) — the failing test from reproduce,
   now expected green. This is the fix's own instrument.
3. The full gate (run_gate) — the entire suite. Zero failures is the
   only acceptable gate result, and never weaken an assertion to get
   green. A failure you believe is pre-existing is still `red` — name
   it and let the human decide what it means.

`green` only if all three are clean; anything else is `red` with the
exact failing output. The flow loops back to implement at most once more,
then stops and escalates. Do not spend the second cycle re-running the
same edit hoping for a different answer — if the failure is not
understood, report red with a clear account of what still fails.

Outcome: green or red.
