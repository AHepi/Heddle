---
name: navigate
version: 3
steps:
  navigate:
    tools: [read_map, run_wheel]
    outcomes: [oriented]
---

## navigate

Orient in the repository before touching anything. Load the repo's memory
so the flow starts from what is already known.

Read, in order:

1. map/RESULTS.md — the top entry in full. It ends with residue (known
   unfinished work). If your task is named there, you are continuing work,
   not starting it — say so.
2. map/TRAPS.md — known failure modes. If a later symptom matches a trap,
   the trap beats your intuition.
3. The map docs your task touches: SUB- for surfaces, SEAM- for
   boundaries, CON-/INV- for contracts.
4. map/PROTECTED.md — before forming any intention to edit. Protected
   surfaces move only on the human's verbatim recorded words.

Then spin the smoke wheel (run_wheel). If it is not clean, the harness
itself is broken: stop and report exactly what the wheel printed instead
of working around it.

Report `oriented` only when you can name: the surfaces the task touches,
the traps that could bite, whether anything protected is nearby, and what
the last RESULTS entry left unfinished.

Outcome: oriented.
