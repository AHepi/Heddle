---
name: plan
description: Plan the change as an ordered list of steps.
steps:
  plan:
    tools: [read_map, read_code, read_tests, write_map, protected_tripwire]
    outcomes: [planned]
---
# Plan

## plan
Produce an ordered list of small steps, each naming the file it touches. Run
the protected tripwire: if any planned step touches a protected surface, the
plan must say so and require explicit human authorization. Store the step list
as plan_steps. Outcome: planned.
