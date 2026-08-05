---
name: review
version: 1
steps:
  derive:
    tools: [read_authority]
    outcomes: [done]
  check:
    tools: [read_authority, read_code, run_tests]
    outcomes: [ok, problems_found]
  write_finding:
    tools: [write_report]
    outcomes: [done]
---

## derive
Before reading any implementation, write down what the authority requires.
Cite the clause for each expectation. Name the strongest alternative reading.

## check
Compare the implementation against your derivation. Do not harmonise a
disagreement toward the implementation.

## write_finding
One finding. Include expected, observed, and the narrowest repair boundary.
