---
name: change
version: 2
steps:
  capture:
    tools: [read_map, write_map]
    outcomes: [captured]
  specify:
    tools: [read_map, write_map, read_code, read_tests]
    outcomes: [specified]
  plan:
    tools: [read_map, read_code, read_tests, write_map, protected_tripwire]
    outcomes: [planned]
  execute_step:
    tools: [read_code, write_code, write_tests, run_ring]
    outcomes: [step_done, all_done]
  validate:
    tools: [run_wheel, run_ring, run_gate, protected_tripwire]
    outcomes: [valid, invalid]
  deliver:
    tools: [read_map, write_map]
    outcomes: [delivered]
---

# Change

The change discipline: the repository should do something tomorrow that it
does not do today. Where the defect flow works backward from a failure,
this flow works forward from an intent — and the danger is different.
Defects tempt you to fix too little; changes tempt you to build too much,
or to build before anyone has written down what "done" means. So the flow
front-loads the writing: capture the intent, specify the requirement, plan
the steps, and pass two human gates before any code moves. The
orchestrator is flows/change.yaml; each step below is the complete prose
its model receives.

## capture

State what the user wants and why, in one or two sentences, before any
analysis. This is the intent on the record — everything later (the REQ-
doc, the plan, the validation) will be checked against it, so capture the
*want*, not your first idea of the implementation.

- **What:** the behavior or capability being asked for, in the user's
  terms. If the request was vague, write the most defensible concrete
  reading and flag the vagueness rather than silently picking.
- **Why:** the problem it solves or the gap it closes. If you cannot state
  the why, that is worth surfacing now — a change with no why tends to
  fail its own spec gate.

Check the map (`read_map`): does map/RESULTS.md residue already mention
this? Does an existing REQ- doc cover or contradict it? Note what you
find. If the intent implies a new requirement, say that a REQ- doc will be
written at specify time — do not write it yet.

Write the captured intent into the map (`write_map`).

Outcome: `captured`.

## specify

Write the requirement down before planning. The REQ- doc is the authority
that validate will later hold the finished change against, so it must be
checkable by someone who did not build the change:

- **Behavior:** what the system will do, stated as observables — inputs,
  outputs, side effects. "The validator reports X with file and line" is
  checkable; "validation is improved" is not.
- **Inputs and outputs:** the domains involved, edge cases included.
- **How it will be checked:** the actual instrument — which test, which
  command, what the passing output looks like. If you cannot write this
  section, the requirement is not yet a requirement.

Read the relevant code and tests first (`read_code`, `read_tests`) so the
spec describes the system that exists, not a remembered version of it.
Then check the map's contracts: if the change alters an existing CON- or
INV- document's meaning, name the contract in the REQ- doc — a change
that silently rewrites a contract is how ERRATA entries get born.

Write or update the REQ- doc in map/ (`write_map`, name matching
`REQ-*.md`). The flow gates on this document next: the human reads it and
approves or rejects. Write it so rejection is easy — a spec gate that can
only say yes is not a gate.

Outcome: `specified`.

## plan

Turn the approved requirement into an ordered list of small steps. The
execute step will walk this list one item at a time with no memory of your
reasoning, so each item must stand alone:

- **One step, one edit.** Each item names the file it touches and says
  what changes in it and what "done" looks like for that item. An item
  that touches three files is three items.
- **Ordered so every prefix is coherent.** After any step, the repo should
  build and the already-run rings should pass. Put test changes with (or
  before) the code they cover, not batched at the end.
- **Bounded.** The orchestrator caps execution at eight steps. If the
  honest plan needs more, that is a sign the change should be split — say
  so in the plan rather than compressing steps to fit.

Then the protected check, which is not optional: run the
`protected_tripwire` and read map/PROTECTED.md (`read_map`). If any
planned step touches a protected surface, the plan must say so on its
first line and quote the protected entry — the human approving this plan
is then knowingly authorizing a protected edit, which is the only way one
is permitted. If the tripwire output is non-empty for reasons outside
your plan (pre-existing drift), report that too; an unexplained tripwire
is a stop, not a footnote.

Store the ordered list in the map (`write_map`) as the plan of record —
the human gate on this plan reads what you wrote, and execute does exactly
what it says.

Outcome: `planned`.

## execute_step

Take the next unfinished item from the approved plan and do exactly that
item. You are inside a loop: one call, one item. Resist doing the next
item "while you're here" — the loop's bound and the plan's order are the
control structure, and batching work inside one call defeats both.

For the item at hand:

1. Read the file it names (`read_code`) — the plan was written against a
   snapshot, and earlier steps may have moved things.
2. Apply the edit (`write_code`, or `write_tests` for test files),
   matching the surrounding style. If the item as written no longer makes
   sense — the code changed under it, or the item was wrong — do not
   improvise a different edit; report `step_done` with a clear note that
   the item could not be applied as planned, so validation fails honestly
   rather than the plan drifting silently.
3. Run the ring that covers the touched files (`run_ring`) and quote its
   output. A red ring after your edit is information for validate, not
   something to suppress — but if the fix is within the item's own scope
   (you broke what you just wrote), repair it now.

Outcome: `step_done` after completing one item with items remaining;
`all_done` when the plan has no unfinished items left. `all_done` is a
claim about the plan, not about quality — validation is the next step's
job, not yours.

## validate

Check the finished change against its requirement. You are the first
reader of the REQ- doc who did not build the change; hold that posture.
The question is never "does this look good" but "does the observed
behavior match what was specified, as shown by the instruments":

1. **Smoke wheel** (`run_wheel`) — the fast spin first. If the harness
   itself no longer turns, nothing else you measure means anything.
2. **The REQ- doc's own check** — the "how it will be checked" section
   named an instrument; run it (`run_ring`) and compare its actual output
   to the specified passing output. Behavior beyond the spec is drift;
   behavior short of it is `invalid`. Do not harmonise a disagreement
   toward the implementation — if the code does something reasonable that
   the spec did not say, the finding is a mismatch, and the human decides
   which one moves.
3. **The full gate** (`run_gate`) — everything else still passes. Every
   test, no exceptions argued away.
4. **The tripwire** (`protected_tripwire`) — no protected surface moved
   without the authorization recorded at plan time. A non-empty diff
   against a protected path that the approved plan did not declare is an
   automatic `invalid`, whatever the tests say.

Quote each instrument's output. The outcome is `valid` only if all four
hold; otherwise `invalid`, with the specific mismatch named — the flow
parks the change and records, and a well-named mismatch is what makes the
parked change resumable.

Outcome: `valid` or `invalid`.

## deliver

Close the change out. Two obligations, both in the same commit as the
change itself — a map that lags its code is a map ERRATA will eventually
catch:

- **The summary:** one paragraph — what changed, why, and how it was
  validated (name the instruments and their results). This is what the
  RESULTS entry and any human reader will rely on; write it in terms of
  behavior, not diff hunks.
- **The map moves with the change** (`write_map`): the REQ- doc gains its
  verification stamp (date and instrument output); any SUB-, CON-, or
  INV- doc whose claims this change altered is updated to say what is now
  true; any check command whose output changed gets its recorded output
  re-dated. Read the touched docs (`read_map`) rather than trusting
  memory about what they said.

Delivery is not the record — `shared.record` runs after this and writes
the ledgers. Deliver is the change-facing close: the artifact and its
documentation, consistent, in one commit.

Outcome: `delivered`.
