---
name: specify
version: 4
steps:
  specify:
    tools: [read_map, write_map, read_code, read_tests]
    outcomes: [specified]
---

## specify

Write the requirement down before planning. The REQ- doc is the authority
validate will hold the finished change against, so it must be checkable
by someone who did not build the change:

- Behavior: what the system will do, as observables — inputs, outputs,
  side effects. "The validator reports X with file and line" is
  checkable; "validation is improved" is not.
- Inputs and outputs: the domains involved, edge cases included.
- How it will be checked: a machine-decidable acceptance check per
  numbered requirement — which test, which command, what passing output
  looks like. No check = not specified.

Named mechanisms are suggestions, not requirements. If the request names
a fixture, file, or pattern, trace it (read_code, read_tests) to confirm
it actually reaches the code in question. If it cannot, specify the
property the requirement wants and record the contradiction in the REQ-
doc — never adopt unverified, never deviate silently.

Read the relevant code and tests first (read_code, read_tests) so the
spec describes the system that exists, not a remembered version of it.
If the change alters an existing CON- or INV- contract, name the
contract in the REQ- doc — silently rewriting a contract is how ERRATA
entries get born.

Before writing it down, one anti-invention pass: delete anything in the
spec untraceable to a numbered requirement from capture. Then re-read as
a reviewer would; any "no" routes back before the gate sees it.

Write or update the REQ- doc in map/ (write_map, name REQ-*.md). The
human gates on this document next: write it so rejection is as easy as
approval.

Outcome: specified.
