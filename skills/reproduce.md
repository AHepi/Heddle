---
name: reproduce
description: Write a failing test that demonstrates the defect.
steps:
  reproduce:
    tools: [write_tests, run_ring, read_code]
    outcomes: [reproduced]
---
# Reproduce

## reproduce
Add a test under tests_heddle/ that fails for the diagnosed reason and passes
only when the defect is fixed. Run it and show the failure. Outcome:
reproduced.
