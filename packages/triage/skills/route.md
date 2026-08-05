---
name: route
version: 1
steps:
  route:
    tools: [write_notes]
    outcomes: [routed]
---

## route

Write the routing note (write_notes): a ready-to-run entry the future
runner can start from with a paste, not an authoring session. It
contains, in order:

1. One line of WHAT — the goal in one sentence.
2. The classification, and which workflow to enter (your repo's defect
   or change flow; for a question, who answers it and by when).
3. Evidence pointers — the request note's filename, plus any file,
   log, or record the clarify step named.
4. End state — one sentence describing what "done" observably looks
   like, so the runner knows when to stop.
5. Open assumptions and unanswered forks from clarify, labeled, so the
   runner inherits them knowingly.

Do not begin the work here. Routing that drifts into diagnosing or
planning has left its tranche.

Outcome: routed.
