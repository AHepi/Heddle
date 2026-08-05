---
name: confirm
version: 1
steps:
  confirm:
    tools: [run_wheel]
    outcomes: [confirmed, broken]
---

## confirm

Prove the redrafted skill still fits the harness. Spin the smoke wheel
(run_wheel): it loads every skill, checks front matter against headings,
resolves every flow reference, and validates grants — exactly the ways a
skill edit can silently break the package.

Read the wheel's actual output and quote it:

- Clean wheel → `confirmed`. Also state in your summary what changed at
  the surface level (prose only, or names/outcomes/tools — and if the
  latter, which dependents were updated to match).
- Anything else → `broken`, with the wheel's exact output and your
  reading of which reference or declaration no longer lines up. The flow
  loops back to redraft once; a second `broken` stops the flow, so make
  the failure account precise enough to fix blind.

Do not report `confirmed` on the strength of having re-read the file —
the wheel is the instrument, and instruments name their numbers.

Outcome: confirmed or broken.
