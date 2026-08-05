---
name: execute_step
version: 5
steps:
  execute_step:
    tools: [read_code, write_code, write_tests, run_ring, write_map]
    outcomes: [step_done, all_done]
---

## execute_step

Take the next unfinished item from the approved plan and do exactly that
item. You are inside a loop: one call, one item. Do not do the next item
"while you're here" — the loop's bound and the plan's order are the
control structure.

For the item at hand:

1. Read the file it names (read_code) — the plan was written against a
   snapshot, and earlier steps may have moved things.
2. Apply the edit (write_code, or write_tests for test files), matching
   the surrounding style. If the item as written no longer makes sense,
   do not improvise a different edit; report `step_done` with a clear
   note that it could not be applied as planned, so validation fails
   honestly instead of the plan drifting silently.
3. Run the item's done-criterion and the ring covering the touched files
   (run_ring); paste the real output. A red ring is information for
   validate, not something to suppress — but if you broke what you just
   wrote, repair that now; it is within the item's scope. If the same
   item has now failed twice, stop reporting progress on it — and the
   stop leads with the decision needed in ONE sentence, the candidate
   routes priced, and a recommendation with its reason. A stop that
   must be interrogated is half a stop.
4. Mark the item in the plan of record (write_map) — done with its
   pasted output, or failed with the mismatch — and refresh the plan's
   `State:` line (next item, blockers). A fresh session resumes from
   the plan of record alone, with no memory of this one; if it could
   not, this session under-recorded.

Cross-routing is strict: a defect discovered mid-change is parked — not
fixed. Write the parked note for its future runner, at park time, while
the context is free: one line of WHAT, then a ready-to-run entry (which
flow to enter, one-goal statement, evidence pointers, end state), so
starting the follow-up costs a paste, not an authoring session. One
tranche, one goal.

Outcome: `step_done` after completing one item with items remaining;
`all_done` when no unfinished items remain. `all_done` is a claim about
the plan, not about quality — validation is the next step's job.
