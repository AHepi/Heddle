---
name: specify
version: 5
steps:
  specify:
    tools: [read_map, read_code, read_tests, capture]
    outcomes: [specified]
---

## specify

First record the requester's words, then write the requirement down
before planning.

The record is verbatim (capture tool, name REQ-*.md): the requester's
words exactly as given, then numbered into requirements — REQ-1, REQ-2 —
beneath the quote. Authority is the ledger, not memory: everything later
(plan, validation, delivery) reconciles against these numbered words,
and amendments are append-only, never edits to what was already
recorded. For each numbered requirement, note the why if the requester
gave one; if they did not and it matters, that is a question for the
gate, not a blank to fill with your own guess. Handle ambiguity by
size: minor forks get the smallest defensible reading, recorded as an
overridable assumption labeled as such; material forks are not picked —
route them to the cheapest authority (the record, then the framework's
own behavior), and only what survives goes to the human, batched with
your recommendation, at the spec gate.

Check the map first (read_map): does RESULTS residue or an existing
REQ- doc already cover or contradict this request? Note what you find
in the REQ- doc.

The REQ- doc is the authority validate will hold the finished change
against, so it must be checkable by someone who did not build the
change:

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

Before finishing, one anti-invention pass: delete anything in the spec
untraceable to a numbered requirement. Then re-read as a reviewer
would; any "no" routes back before the gate sees it.

The human gates on this document next: write it so rejection is as easy
as approval.

Outcome: specified.
