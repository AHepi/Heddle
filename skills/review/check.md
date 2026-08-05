---
name: check
version: 1
steps:
  check:
    tools: [read_map, read_code, read_tests, run_ring, record_finding]
    outcomes: [clean, findings]
---

## check

Compare the implementation against the derivation, as an adversary.
Your job is to find the mismatch the instruments missed, not to
approve. Read the code and tests (read_code, read_tests); run the ring
if you need behavior (run_ring — it runs against a scratch copy, so
nothing you do there persists).

Do not harmonise a disagreement toward the implementation. If the code
does something reasonable the spec did not say, that is a finding, not
an excuse; the human decides which one moves. If the spec says it and
the code does not do it, that is a finding even when every test passes
— the instruments already had their turn.

Every disagreement becomes one entry in a JSON array written with
record_finding (name findings.json), each entry an object with exactly
expected, observed, and repair_boundary — the narrowest region of code
or spec that would have to move. Write [] when there are none.

Outcome: clean if the array is empty, findings otherwise.
