---
name: record
version: 3
steps:
  record:
    tools: [read_map, write_map, run_gate]
    outcomes: [recorded]
---

## record

Append the outcome to the ledgers. This step runs on every exit path —
success, failure, rejection, halt. An unrecorded run is one the repository
never learns from.

Write to map/RESULTS.md, newest entry first, dated, containing:

- What was attempted — one or two sentences of intent, not file names.
- What the instruments showed — the actual wheel/ring/gate results with
  numbers ("gate: 19 passed, 0 failed"), never adjectives ("tests fine").
  Instruments name their numbers; do not paraphrase them.
- What residue remains — everything unproven or unfinished, stated so the
  next session can resume without archaeology. "No residue" is a claim;
  make it only if true.

Then two conditional ledgers:

- map/TRAPS.md — if this run hit a new, non-obvious failure mode, add an
  entry: symptom, cause, incident, fix or workaround. Never delete
  entries.
- map/ERRATA.md — if a committed document said something this run proved
  false, append one line: date | document | claim | what is actually
  true | evidence.

Cite gate output you already have; run run_gate only if the entry needs a
number you lack.

Outcome: recorded.
