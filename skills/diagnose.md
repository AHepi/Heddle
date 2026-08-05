---
name: diagnose
description: Locate the defect's cause using evidence, not guesses.
steps:
  diagnose:
    tools: [read_code, read_tests, read_map, run_ring]
    outcomes: [located, inconclusive]
---
# Diagnose

## diagnose
Run the relevant test ring and read the implicated code. Name the file, line,
and mechanism of the failure. Instruments name their numbers: cite the exact
test output. If the evidence does not converge on one cause, the outcome is
inconclusive and the flow must stop to ask the human. Outcome: located or
inconclusive.
