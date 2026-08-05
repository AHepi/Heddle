---
name: propose
version: 3
steps:
  propose:
    tools: [read_code, read_tests, read_map]
    outcomes: [proposed]
---

## propose

Describe the smallest change that fixes the reproduced defect, for a
human who will approve or reject without running anything. The proposal
carries all the evidence:

- The change: every file it touches, and for each, what changes and why
  that serves the diagnosed mechanism. "Smallest" is a real constraint —
  no drive-by refactors, renames, or fixing adjacent smells. Anything
  else worth fixing goes in as a note for the record, not as part of the
  change.
- The protected check: read map/PROTECTED.md (read_map). If any touched
  surface is protected, say so in the first line and quote the protected
  entry verbatim — the human must know they are authorizing a protected
  edit. If nothing protected is touched, state that you checked.
- The blast radius: which tests cover the touched code, and what verify
  will run to prove nothing else broke.

Write it so a "no" is as easy to give as a "yes". A proposal that buries
its risks is asking for a rubber stamp, not approval.

Outcome: proposed.
