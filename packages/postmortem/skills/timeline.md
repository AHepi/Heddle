---
name: timeline
version: 1
steps:
  timeline:
    tools: [git_log, read_notes]
    outcomes: [reconstructed]
---

## timeline

Reconstruct what happened from the record only — commits (git_log),
the incident note, logs pasted into it (read_notes). No theorizing:
this step establishes WHAT happened and in what order, never WHY.

Write the timeline as dated, ordered entries, each citing its source
(commit hash, note filename, quoted log line). An event you cannot
source is marked "unsourced: <who remembers it>" — memory is admissible
only when labeled as memory.

Include the non-events that matter: the check that did not run, the
review that did not happen, the entry that was not written. Absences
cluster exactly where incidents grow.

Outcome: reconstructed.
