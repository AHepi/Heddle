# Spec: Evidence-Ledgered Work Discipline

Captured verbatim from the human authority, 2026-08-05. This document is
the requirement; the skills under skills/ implement it. Amendments are
append-only, in the authority's words.

---

A method for navigating, documenting, and changing a complex system such
that every claim is checkable, every decision is traceable to authority,
and mistakes become permanent infrastructure instead of repeated costs.

## 1. Ground rule: evidence over prose

The system of record (logs, test output, committed artifacts, command
output) is the only admissible evidence. Narrative — including your own —
is never evidence.

Every claim must name the instrument that produced its number ("the gate
says 0 failed", not "it works"). Two instruments can disagree and both be
right; cite which one.

"Accepted does not mean true." A result that passed review is still only
as good as what was actually measured. Record the residue: what remains
unproven.

Negative and inconclusive results are recorded as such, never rounded up.

## 2. The map: navigation documents authenticated by re-derivation

Do not scope work by searching a large system; scope it from a map. Five
document kinds, filename = identifier:

- SUB-<unit> — one subsystem: what it owns, entry points, state.
- CON-<slug> — a cross-cutting concept that is not a unit.
- SEAM-<a>-x-<b> — how two of them meet. Read the seam before either
  side: it names the small fraction of each actually involved.
- INV-<slug> — an invariant or protected surface.
- REC-<slug> — a worked recipe for a recurring change.

Rules that keep the map alive:

- Checks, not signatures. Every load-bearing claim carries a runnable
  check that must exit clean. A signature proves who wrote a sentence; a
  check proves it is still true — the property that decays. Audit checks
  for vacuousness (a check that cannot fail proves nothing).
- The map moves in the same commit as the change. A separate "update
  docs" commit is the commit that gets dropped.
- Verification stamps advance only when re-run. A stale stamp is honest;
  a false one is not.
- Every fix earns a Traps entry naming its motivating incident. Traps
  entries are never deleted — only rewritten to say when they were fixed.
  A recurrence is the cheapest diagnosis available, so read Traps before
  investigating.
- A missing seam document means "not yet written," never "these don't
  interact."

## 3. Protected surfaces: authorization is not correctness

Maintain an explicit list of surfaces that must not change without the
human authority's verbatim recorded words (things whose change would
invalidate committed evidence or downstream consumers).

Correctness evidence never substitutes for authorization. A technically
perfect change to a protected surface without recorded approval is
undeliverable by definition.

Forecast protected-surface contact at design time, in writing —
discovering it at validation is several commits too late. Back it with
one mechanical tripwire (a diff over the protected paths, pasted, empty
or explained) so the guarantee doesn't rest on memory.

Prefer fixing readers over changing recorded formats: old evidence must
stay valid forever.

## 4. Two workflows, one phase at a time

All substantive work routes through one of two families; each phase owns
exactly one artifact, committed at every boundary.

Something is broken: goal → diagnose → reproduce → propose fix →
implement → verify.

- Diagnosis comes from the record before code reading. Read the actual
  error artifact before theorizing — recorded misattributions cluster
  exactly where readers skipped it.

Someone requests a change: capture → specify → plan → execute one step →
validate → deliver.

- Capture is verbatim: the requester's words, numbered into requirements,
  amendments append-only. Authority is the ledger, not memory.

Cross-routing is strict: a defect found mid-change is parked, not fixed;
a change wished for mid-defect is parked, not implemented. One tranche,
one goal.

Execution is one step per invocation, each with a runnable done-criterion
whose real output is pasted. Two failures of the same step = stop.

Validation never patches. A failure routes back to planning with
evidence. A validation record that erases the failure it caught is not a
record.

Delivery reconciles requirement-by-requirement against the requester's
words: done / done-with-recorded-deviation / deferred-with-their-words.
Nothing silently dropped.

## 5. Specification discipline (where judgment concentrates)

Every requirement gets a spec item with a machine-decidable acceptance
check. No check = not specified.

Named mechanisms are suggestions, not requirements. A fixture, file, or
pattern the request names must be traced to confirm it actually reaches
the code in question. If it can't, deliver the property the requirement
wants and record the contradiction — never adopt unverified, never
deviate silently.

Blast-radius census, mechanical: grep tests and map checks for every
symbol being changed; paste the hits; classify each expected to move or
must not move. Forecasting drift by recall fails even for strong
reasoners; a census is a checklist walk.

Ambiguity handling: minor forks → choose the smallest reading, record as
an overridable assumption. Material forks → stop and ask, but first route
each question to the cheapest authority (record → framework → human) and
batch survivors with recommendations.

Design-only deliverables (approve-before-build gates): every load-bearing
claim is a pasted measurement, not an argument; every option priced
(files, protected contact, size, risk); every rejection cites a
measurement.

Anti-invention pass: delete anything untraceable to a numbered
requirement. Rubric pass: re-read as a reviewer; any "no" routes back
before commit.

Over a size threshold, split into ordered sub-tranches, each
independently deliverable, the ladder stopping safely after any.

## 6. Instruments and their economy

Distinguish the ring (fast, targeted checks while iterating) from the
gate (the full suite at phase boundaries). Zero failures is the only
acceptable gate result; never weaken an assertion to get green.

Immutable evidence's verdict can only move if a reader moved: when no
reader changed, the previous measurement is the current answer — don't
re-run for comfort.

Every instrument must be named where sessions start, with the rule for
when it's owed. An instrument nothing mentions rots silently (a check
that pins the world as-of its writing fails the first time the world
legitimately grows).

A checker that never looks at new data reports success trivially: every
new observable needs a probe that reads it, landed separately so the
baseline comparison stays meaningful, and mutation-proven non-vacuous.

Proof claims must name the commit they were measured at — a true claim
can silently expire two commits later.

## 7. Durable checks (survive dramatic change, fail only when the claim dies)

Pin only to committed, immutable evidence; name the motivating incident
in the docstring.

Anchor to meaning, not form — behavior, structure, counts; minimal
substrings if text is unavoidable; never line numbers.

Mutation-prove failability before writing down: break the guarded thing,
watch it go red, restore; keep a permanent failing-companion for equality
checks.

Compare typed outcomes with volatile fields (time, randomness) scrubbed
recursively; diagnose flakes to the exact field.

Tolerate absence in old evidence — assert the attribute exists before
reading; absence is valid, and "absent everywhere forever" is a claim
with an expiry date.

## 8. The correction culture

An append-only errata ledger records every discovered falsehood in
committed documents, so no one re-trusts a refuted claim. One writer per
ledger; others contribute via their own artifacts.

Sessions start by reading the newest results narrative and the errata —
the running truth of what is proven, broken, fixed, and parked.

Corrections are stated plainly and once; failures are preserved verbatim
in the record that caught them.

Workflow failures get promoted into the workflow itself: every recurring
miss becomes a mandatory step, named with its motivating incident, so the
process compounds.

## 9. Reporting

Lead with the result in one or two sentences; detail goes in the
artifact, not the reply.

State what the record shows, then the residue. Never claim more than was
measured.
