---
name: diagnose
version: 3
steps:
  diagnose:
    tools: [read_code, read_tests, read_map, run_ring]
    outcomes: [located, inconclusive]
---

## diagnose

Locate the cause with evidence, or say plainly that you could not. An
honest `inconclusive` is worth more than a confident guess — everything
after this step builds on it.

Method:

1. Run the relevant test ring (run_ring) against the area the goal
   implicates. Quote its output; do not paraphrase it.
2. Read the implicated code (read_code) and tests (read_tests). Follow
   the failure from symptom back to mechanism: which line does the wrong
   thing, and why does that produce exactly the observed behavior — this
   failure, not merely "a" failure.
3. Check map/TRAPS.md (read_map). If the symptom matches a recorded trap,
   that cause is the leading hypothesis; confirm it or explain why this
   time differs.

The bar for `located`: you can name the file, the line or small region,
and the mechanism, and the evidence converges on it and nothing else.
Correlation ("started failing after commit X") is a lead, not a location.

If two candidate mechanisms remain, or the symptom will not reproduce,
report `inconclusive`: say what you checked, what each candidate would
predict, and what evidence would settle it. The flow then stops and asks
the human — that is designed behavior, not your failure.

Outcome: located or inconclusive.
