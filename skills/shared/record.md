---
name: record
version: 4
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
  numbers ("gate: 21 passed, 0 failed"), never adjectives ("tests
  fine"), and the commit they were measured at — a true claim can
  silently expire two commits later. Negative and inconclusive results
  are recorded as such, never rounded up.
- What residue remains — everything unproven or unfinished, stated so the
  next session can resume without archaeology. Accepted does not mean
  true: a result that passed review is only as good as what was actually
  measured. "No residue" is a claim; make it only if true.

Then two conditional ledgers:

- map/TRAPS.md — if this run hit a new, non-obvious failure mode, add an
  entry: symptom, cause, incident, fix or workaround. Never delete
  entries.
- map/ERRATA.md — if a committed document said something this run proved
  false, append one line: date | document | claim | what is actually
  true | evidence.

Cite gate output you already have; run run_gate only if the entry needs a
number you lack. When nothing changed since a measurement, the previous
measurement is the current answer — do not re-run for comfort.

If the same miss has now happened twice, it is a workflow failure, not
bad luck: note in the RESULTS entry that the step which should have
caught it needs updating, naming the incident — that note is what feeds
the skill-update flow.

Outcome: recorded.
