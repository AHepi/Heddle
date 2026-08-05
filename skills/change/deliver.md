---
name: deliver
version: 4
steps:
  deliver:
    tools: [read_map, write_map]
    outcomes: [delivered]
---

## deliver

Close the change out. Reconcile requirement-by-requirement against the
requester's numbered words from capture: for each REQ, exactly one of
done (name the instrument that shows it), done-with-recorded-deviation
(state the deviation and where it is recorded), or deferred-with-their-
words (quote what is deferred). Nothing silently dropped — a requirement
the reconciliation does not mention is a delivery failure.

Then two obligations, both in the same commit as the change itself — a
map that lags its code is a map ERRATA will eventually catch:

- The summary: one paragraph — what changed, why, and how it was
  validated (name the instruments, their results, and the commit
  measured at). Write it in terms of behavior, not diff hunks; the
  RESULTS entry and future readers rely on it.
- The map moves with the change (write_map): the REQ- doc gains its
  verification stamp (date and instrument output); any SUB-, CON-, or
  INV- doc whose claims this change altered is updated to say what is
  now true; any recorded check output that changed is re-dated. Read the
  touched docs (read_map) rather than trusting memory of what they said.

Delivery is not the record — record runs after this and writes the
ledgers. Deliver is the change-facing close: artifact and documentation,
consistent, in one commit.

Outcome: delivered.
