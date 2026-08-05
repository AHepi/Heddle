---
name: verify
description: Prove the fix works and nothing else broke.
steps:
  verify:
    tools: [run_ring, run_gate]
    outcomes: [green, red]
---
# Verify

## verify
Run the reproduction test, then the full gate. Green means every test passes.
If anything fails, outcome is red and the flow loops back. Two failed
implement-verify cycles mean stop and escalate. Outcome: green or red.
