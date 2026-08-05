---
name: redraft
version: 4
steps:
  redraft:
    tools: [read_skill, write_skill, write_tests]
    outcomes: [redrafted]
---

## redraft

Write the updated skill file (write_skill), exactly the change the human
approved at the gate. House rules for every skill in this repository:

- One file, one step. The file lives in its workflow's folder
  (shared/, defect/, change/, skill-update/, review/, cartography/).
  Front matter declares `name`, `version` (bump it), and one entry under
  `steps:` with the step's `tools` and `outcomes`; the `## <step>`
  heading must match the step name exactly.
- Keep the public surface stable unless the approved change says
  otherwise: skill name, step name, outcomes, and tools are referenced
  by flows, grants, and conditions. Prose is yours; names are shared.
- Bite-sized but directive. The prose is the complete instruction a
  model receives at that step — state the purpose, the method as
  numbered points, the quality bar, and how to choose the outcome. Cut
  anything a less capable model could misread as optional flavor.
- Prose is advice; the tool list is enforced. Never write "remain
  read-only" as prose while listing a write tool — align the list with
  the intent.
- End with the outcome line: `Outcome: <name>.` (or `x or y`).
- **Every pin moves with its surface.** Adding, removing, renaming, or
  moving a skill changes the smoke wheel's inventory pin (`SKILLS` in
  tests_heddle/test_smoke.py); update the pin in the same redraft
  (write_tests). A pin left stale is exactly how main went red on
  2026-08-05 (TRAP-inventory-pin-lags-surface) — confirm's wheel will
  catch it, but catching is the backstop, not the plan.

Read the current file first (read_skill); rewrite it whole rather than
patching fragments.

Outcome: redrafted.
