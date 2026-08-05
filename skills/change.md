---
name: change
version: 1
steps:
  capture:
    tools: [write_map]
    outcomes: [done]
  specify:
    tools: [read_map, read_code, read_tests, write_map]
    outcomes: [specified, needs_human]
  plan:
    tools: [read_map, read_code, read_tests, write_map, protected_tripwire]
    outcomes: [planned]
  execute_step:
    tools: [read_map, read_code, read_tests, write_code, write_tests, run_ring]
    outcomes: [step_done, all_done, blocked]
  validate:
    tools: [run_gate, protected_tripwire]
    outcomes: [green, red]
  deliver:
    tools: [read_map, write_map]
    outcomes: [done]
---

## capture
Write the requester's words verbatim into a REQ- document in the map,
numbered into requirements. Amendments are append-only — never edit the
original words. Authority is the ledger, not memory. Return 'done' when the
REQ- doc exists.

## specify
Every numbered requirement gets a spec item with a machine-decidable
acceptance check; no check means not specified. Named mechanisms (a fixture,
a file, a pattern the requester named) are suggestions, not requirements —
trace them to confirm they reach the code in question; if they don't,
deliver the property and record the contradiction. Minor ambiguity: choose
the smallest reading, record it as an overridable assumption. Material
ambiguity: route each question to the cheapest authority (record, then
framework, then human), batch the survivors with recommendations, and return
'needs_human'. Anti-invention pass before finishing: delete anything
untraceable to a numbered requirement.

## plan
Blast-radius census, mechanical: grep tests and map checks for every symbol
being changed, paste the hits, classify each as expected-to-move or
must-not-move. Forecast protected-surface contact and paste the tripwire
output — empty or explained. Over a size threshold, split into ordered
sub-tranches, each independently deliverable, the ladder stopping safely
after any. Write the plan as ordered steps, each with a runnable
done-criterion.

## execute_step
Execute exactly one plan step per invocation, then run its done-criterion
and paste the real output. Return 'step_done' if plan steps remain,
'all_done' when the last step passes, 'blocked' with evidence if stuck.
Two failures of the same step means stop — return 'blocked', do not retry
a third time. A defect found mid-change is parked, not fixed.

## validate
Run the gate and paste the output, then paste the protected-paths tripwire
— empty or explained. Zero failures is the only acceptable gate result, and
correctness evidence never substitutes for authorization: a technically
perfect change to a protected surface without recorded approval is
undeliverable. Validation never patches. Return 'green' or 'red'; a red
result routes back to planning with evidence.

## deliver
Reconcile requirement-by-requirement against the requester's verbatim words:
done, done-with-recorded-deviation, or deferred-with-their-words. Nothing
silently dropped. Then update the map in the same change: SUB/CON/SEAM/INV
documents touched by the work, verification stamps re-run, TRAPS entries for
anything that surprised you. Lead the report with the result in one or two
sentences, state what the record shows, then the residue.
