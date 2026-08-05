---
name: shared
version: 2
steps:
  navigate:
    tools: [read_map, run_wheel]
    outcomes: [oriented]
  record:
    tools: [read_map, write_map, run_gate]
    outcomes: [recorded]
---

# Shared

Steps that every orchestrator uses. Both flows open with `shared.navigate`
and close — on every path, including refusals and failures — with
`shared.record`. Nothing in this file is optional decoration: navigation is
what makes the map worth keeping, and recording is what makes the next run
cheaper than this one.

## navigate

Orient in the repository before touching anything. You are not being asked
to skim; you are being asked to load the repo's memory so that the rest of
the flow starts from what is already known instead of rediscovering it.

Read in this order, and do not skip a stage because the task looks small:

1. **map/RESULTS.md** — the newest-first narrative. Read at least the top
   entry in full. It ends with residue: the list of things known to be
   unfinished or unproven. If the task in front of you is already named in
   the residue, say so — you are continuing work, not starting it.
2. **map/TRAPS.md** — known failure modes, never deleted. A recurrence is
   the cheapest diagnosis there is. If a symptom you meet later matches a
   trap, the trap wins over your intuition.
3. **The surfaces the task touches** — map/SUB-*.md for the subsystem
   (loader, validate, interpreter, tools, cli), map/SEAM-*.md for any
   boundary you will cross, map/CON-*.md and map/INV-*.md for contracts
   and invariants you must not break.
4. **map/PROTECTED.md** — before you form any intention to edit. Protected
   surfaces move only on the human authority's verbatim recorded words;
   correctness evidence never substitutes. Knowing the protected list
   *before* planning is what keeps proposals honest.

Then spin the smoke wheel (`run_wheel`). It is one fast pass that proves
the harness itself turns: packages load, flows parse to something
non-empty, references resolve. If the wheel does not come back clean, the
repository is broken in a way that will corrupt everything downstream —
stop and report exactly what the wheel printed rather than working around
it.

What "oriented" means: you can name the surfaces the task touches, the
traps that could bite, whether anything protected is nearby, and what the
last RESULTS entry says was left unfinished. If you cannot do those four
things, keep reading; do not report the outcome to escape the step.

Outcome: `oriented`.

## record

Append the outcome to the ledgers. This step runs on every exit path —
success, failed validation, rejected proposal, inconclusive diagnosis,
halted gate. An unrecorded run is a run the repository never learns from,
which is worse than a failed run that was written down.

Write to **map/RESULTS.md**, newest entry first, dated. The entry must
contain, in prose a future reader can act on:

- **What was attempted** — one or two sentences, in terms of intent, not
  file names.
- **What the instruments showed** — the actual output that matters: which
  wheel/ring/gate runs happened and their results, with numbers where
  numbers exist ("gate: 16 passed, 0 failed"), not adjectives
  ("tests fine"). Instruments name their numbers; you do not paraphrase
  them.
- **What residue remains** — everything left unproven, unfinished, or
  parked, stated so the next session can pick it up without archaeology.
  "No residue" is a claim; make it only if it is true.

Then two conditional ledgers:

- **map/TRAPS.md** — if this run hit a failure mode that was new and
  non-obvious (you would not have predicted it from the docs), add an
  entry: symptom, cause, incident, fix or workaround. Entries are never
  deleted, only annotated when fixed.
- **map/ERRATA.md** — if any committed document said something this run
  proved false, append one line in the ledger's format:
  date | document | claim | what is actually true | evidence. State the
  correction plainly and once; do not edit the original document's history
  to hide that it was wrong.

If you have gate output from earlier in the flow, cite it; run the gate
(`run_gate`) only if the entry needs a number you do not already have.

Outcome: `recorded`.
