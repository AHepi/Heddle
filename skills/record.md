---
name: record
version: 1
steps:
  read_record:
    tools: [read_map]
    outcomes: [done]
  record:
    tools: [read_map, write_map, run_gate]
    outcomes: [done]
---

## read_record
Sessions start here. Read RESULTS.md first, then ERRATA.md, then TRAPS.md —
the running truth of what is proven, broken, fixed, and parked. A recurrence
is the cheapest diagnosis available; if TRAPS names your symptom, quote the
entry before doing anything else. Narrative is not evidence: treat every
claim in the record as only as good as the instrument it names.

## record
Update the record in the same change as the work — a separate "update docs"
pass is the one that gets dropped. Prepend the newest results narrative to
RESULTS.md: what was measured, which instrument produced each number, the
commit it was measured at, and the residue (what remains unproven). Every fix
earns a TRAPS.md entry naming its motivating incident; trap entries are never
deleted, only rewritten to say when they were fixed. If any committed
document was found false, append to ERRATA.md plainly and once. Advance a
verification stamp only by re-running its check and pasting the output; a
stale stamp is honest, a false one is not. Negative and inconclusive results
are recorded as such, never rounded up. If the run failed, the failure is
preserved verbatim — a record that erases the failure it caught is not a
record.
