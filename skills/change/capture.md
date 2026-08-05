---
name: capture
version: 4
steps:
  capture:
    tools: [read_map, write_map]
    outcomes: [captured]
---

## capture

Capture is verbatim. Write the requester's words into the map exactly as
given, then number them into requirements — REQ-1, REQ-2 — beneath the
quote. Authority is the ledger, not memory: everything later (spec, plan,
validation, delivery) reconciles against these numbered words, and
amendments are append-only, never edits to what was already recorded.

For each numbered requirement, note the why if the requester gave one; if
they did not and it matters, that is a question for the gate, not a blank
to fill with your own guess.

Handle ambiguity by size:

- Minor forks: choose the smallest defensible reading and record it as an
  overridable assumption, labeled as such next to the requirement.
- Material forks: do not pick. First route the question to the cheapest
  authority — the record (RESULTS, REQ-, contracts), then the framework's
  own behavior — and only what survives goes to the human, batched, each
  with your recommendation. The spec gate is where that batch lands.

Check the map (read_map): does RESULTS residue or an existing REQ- doc
already cover or contradict this request? Note what you find with the
capture (write_map).

Outcome: captured.
