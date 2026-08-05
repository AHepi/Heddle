---
name: reproduce
version: 3
steps:
  reproduce:
    tools: [write_tests, run_ring, read_code, read_tests]
    outcomes: [reproduced]
---

## reproduce

Turn the diagnosis into a failing test. The test is the contract for the
rest of the flow: implement makes it pass, verify checks it stayed
passing. A fix without a reproduction is a claim without an instrument.

Write one test under tests_heddle/ (write_tests, name matching
test_*.py) that:

- Fails now, for the diagnosed reason. Run it (run_ring) and show the
  failure output. The message must point at the diagnosed mechanism — a
  test failing on an unrelated setup error reproduces nothing.
- Passes only when the defect is fixed. Do not write a test the current
  code could pass by accident, and do not weaken the assertion.
- Is minimal. Smallest setup that reaches the mechanism. Read the
  neighboring tests (read_tests) first and match their fixtures and
  style.

Name the test after the defect, not a date or ticket number. The red
output is the deliverable of this step — include it in your summary.

Outcome: reproduced.
