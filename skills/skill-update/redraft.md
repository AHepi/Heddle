---
name: redraft
version: 2
steps:
  redraft:
    tools: [read_skill, write_skill]
    outcomes: [redrafted]
---

## redraft

Write the updated skill file (write_skill), exactly the change the human
approved at the gate. House rules for every skill in this repository:

- One file, one step. The file lives in its workflow's folder
  (shared/, defect/, change/, skill-update/, review/). Front matter
  declares `name`, `version` (bump it), and one entry under `steps:`
  with the step's `tools` and `outcomes`; the `## <step>` heading must
  match the step name exactly.
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

Read the current file first (read_skill); rewrite it whole rather than
patching fragments.

Outcome: redrafted.
