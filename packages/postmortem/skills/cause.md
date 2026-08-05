---
name: cause
version: 1
steps:
  cause:
    tools: [read_notes, git_log]
    outcomes: [named, inconclusive]
---

## cause

Name the mechanism, with evidence, or say plainly that you cannot.
Work from the timeline note (read_notes): the cause must explain every
entry in it — a cause that explains the outage but not the delayed
detection is half a cause.

Distinguish layers and name each:
- The defect: what was wrong in the artifact.
- The process miss: which step should have caught it and did not, and
  why it did not (not run? run but couldn't see it? saw it and was
  overridden?).
- The prediction, if any: was this failure mode already recorded
  (a trap, a residue item, a review finding)? A predicted incident is
  a binding failure, not a knowledge failure — say which.

The bar for `named`: each layer cites timeline entries as evidence,
and no plausible alternative survives the evidence. Otherwise
`inconclusive`, with what would settle it — written so the human can
answer with a word.

Outcome: named or inconclusive.
