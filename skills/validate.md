---
name: validate
description: Validate the finished change against its requirement.
steps:
  validate:
    tools: [run_ring, run_gate, protected_tripwire]
    outcomes: [valid, invalid]
---
# Validate

## validate
Run the full gate. Check the change against its REQ- doc: does the behavior
match what was specified? Run the tripwire to confirm no protected surface
moved without authorization. Update any map doc whose check output changed,
in the same commit. Outcome: valid or invalid.
