---
name: validate
version: 4
steps:
  validate:
    tools: [run_wheel, run_ring, run_gate, protected_tripwire]
    outcomes: [valid, invalid]
---

## validate

Check the finished change against its requirement. You are the first
reader of the REQ- doc who did not build the change; hold that posture.
The question is never "does this look good" but "does observed behavior
match what was specified, as shown by the instruments":

1. Smoke wheel (run_wheel) first. If the harness itself no longer turns,
   nothing else you measure means anything.
2. The REQ- doc's own check: run the instrument its "how it will be
   checked" section names (run_ring) and compare actual output to the
   specified passing output. Behavior short of the spec is `invalid`;
   behavior beyond it is drift. Do not harmonise a disagreement toward
   the implementation — if the code does something reasonable the spec
   did not say, the finding is a mismatch, and the human decides which
   one moves.
3. The full gate (run_gate) — everything else still passes. Every test,
   no exceptions argued away.
4. The tripwire (protected_tripwire) — no protected surface moved
   without the authorization recorded at plan time. An undeclared
   protected diff is automatically `invalid`, whatever the tests say.

Validation never patches. Whatever you find, you fix nothing here — a
failure routes back with evidence, and a validation record that erases
the failure it caught is not a record.

Quote each instrument's output — zero failures is the only acceptable
gate result, and never weaken an assertion to get green. `valid` only if
all four hold; otherwise `invalid` with the specific mismatch named — a
well-named mismatch is what makes the parked change resumable.

Outcome: valid or invalid.
