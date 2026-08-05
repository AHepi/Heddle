---
name: execute
description: Execute one step of the approved plan.
steps:
  execute_step:
    tools: [read_code, write_code, write_tests, run_ring]
    outcomes: [step_done, all_done]
---
# Execute

## execute_step
Take the next item from plan_steps, apply it, and run the ring that covers the
touched files. Outcome: step_done, or all_done when no items remain.
