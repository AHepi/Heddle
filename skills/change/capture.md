---
name: capture
version: 3
steps:
  capture:
    tools: [read_map, write_map]
    outcomes: [captured]
---

## capture

State what the user wants and why, in one or two sentences, before any
analysis. This is the intent on the record — the REQ- doc, the plan, and
validation will all be checked against it. Capture the want, not your
first idea of the implementation.

- What: the behavior or capability asked for, in the user's terms. If the
  request was vague, write the most defensible concrete reading and flag
  the vagueness rather than silently picking.
- Why: the problem it solves. If you cannot state the why, surface that
  now — a change with no why tends to fail its own spec gate.

Check the map (read_map): does map/RESULTS.md residue already mention
this? Does an existing REQ- doc cover or contradict it? Note what you
find. If the intent implies a new requirement, note that a REQ- doc will
be written at specify time — do not write it yet.

Write the captured intent into the map (write_map).

Outcome: captured.
