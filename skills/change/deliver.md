---
name: deliver
version: 3
steps:
  deliver:
    tools: [read_map, write_map]
    outcomes: [delivered]
---

## deliver

Close the change out. Two obligations, both in the same commit as the
change itself — a map that lags its code is a map ERRATA will eventually
catch:

- The summary: one paragraph — what changed, why, and how it was
  validated (name the instruments and their results). Write it in terms
  of behavior, not diff hunks; the RESULTS entry and future readers rely
  on it.
- The map moves with the change (write_map): the REQ- doc gains its
  verification stamp (date and instrument output); any SUB-, CON-, or
  INV- doc whose claims this change altered is updated to say what is
  now true; any recorded check output that changed is re-dated. Read the
  touched docs (read_map) rather than trusting memory of what they said.

Delivery is not the record — record runs after this and writes the
ledgers. Deliver is the change-facing close: artifact and documentation,
consistent, in one commit.

Outcome: delivered.
