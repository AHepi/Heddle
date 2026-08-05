---
name: specify
version: 3
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
- How it will be checked: the actual instrument — which test, which
  command, what passing output looks like. If you cannot write this
  section, the requirement is not yet a requirement.

Read the relevant code and tests first (read_code, read_tests) so the
spec describes the system that exists, not a remembered version of it.
If the change alters an existing CON- or INV- contract, name the
contract in the REQ- doc — silently rewriting a contract is how ERRATA
entries get born.

Write or update the REQ- doc in map/ (write_map, name REQ-*.md). The
human gates on this document next: write it so rejection is as easy as
approval.

Outcome: specified.
