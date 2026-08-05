---
name: plan
version: 4
steps:
  plan:
    tools: [read_map, read_code, read_tests, write_map, protected_tripwire]
    outcomes: [planned]
---

## plan

Turn the approved requirement into an ordered list of small steps.
Execute will walk the list one item at a time with no memory of your
reasoning, so each item must stand alone:

- One step, one edit. Each item names the file it touches, what changes
  in it, and a runnable done-criterion — a command whose real output
  will be pasted when the step executes. An item touching three files is
  three items.
- Ordered so every prefix is coherent. After any step, the repo should
  build and already-run rings should pass. Test changes go with (or
  before) the code they cover, not batched at the end.
- Bounded. The orchestrator caps execution at eight steps. If the honest
  plan needs more, split the change into ordered sub-tranches, each
  independently deliverable so the ladder stops safely after any — say
  so rather than compressing steps to fit.

Blast-radius census, mechanical: for every symbol the plan changes,
search the tests and the map's check commands for it (read_tests,
read_map), paste the hits into the plan, and classify each as expected
to move or must not move. Forecasting drift by recall fails even for
strong reasoners; a census is a checklist walk.

Then the protected check, which is not optional: run protected_tripwire
and read map/PROTECTED.md (read_map). If any planned step touches a
protected surface, the plan's first line must say so and quote the
protected entry — the approving human is then knowingly authorizing a
protected edit. If the tripwire shows drift your plan does not explain,
that is a stop, not a footnote.

Store the ordered list in the map (write_map) as the plan of record.

Outcome: planned.
