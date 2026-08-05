---
name: execute_step
version: 3
steps:
  execute_step:
    tools: [read_code, write_code, write_tests, run_ring]
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
3. Run the ring covering the touched files (run_ring) and quote its
   output. A red ring is information for validate, not something to
   suppress — but if you broke what you just wrote, repair that now; it
   is within the item's scope.

Outcome: `step_done` after completing one item with items remaining;
`all_done` when no unfinished items remain. `all_done` is a claim about
the plan, not about quality — validation is the next step's job.
