---
name: defect
version: 2
steps:
  goal:
    tools: [read_map, write_map]
    outcomes: [captured]
  diagnose:
    tools: [read_code, read_tests, read_map, run_ring]
    outcomes: [located, inconclusive]
  reproduce:
    tools: [write_tests, run_ring, read_code, read_tests]
    outcomes: [reproduced]
  propose:
    tools: [read_code, read_tests, read_map]
    outcomes: [proposed]
  implement:
    tools: [read_code, write_code, write_tests, run_ring]
    outcomes: [applied]
  verify:
    tools: [run_wheel, run_ring, run_gate]
    outcomes: [green, red]
---

# Defect

The defect discipline: something the repository does today is wrong, and
the job is to fix exactly that thing and prove the fix. The steps are
ordered so that no code moves until the failure is understood (`diagnose`),
demonstrated (`reproduce`), and the fix approved by a human (`propose`).
The orchestrator is flows/defect.yaml; this file is the instruction each
step's model actually receives, one step at a time. No step here sees the
whole file — write each step's work as if it is the only prose you get,
because it is.

## goal

State the defect precisely before anyone looks at code. A defect is a gap
between expectation and observation, so the statement has exactly two
halves:

- **Expected:** what should happen, and on whose authority. If a REQ- doc
  in map/ covers the behavior, name it. If a contract (CON-) or invariant
  (INV-) is being violated, name that. If the expectation comes only from
  the reporter's words or from common sense, say so explicitly — "source:
  reporter" is honest; an invented authority is not.
- **Actual:** what happens instead, as an observable — an error message, a
  wrong value, a missing file — not an interpretation ("it's broken") or a
  presumed cause ("the loader is wrong"). Causes belong to diagnose.

One or two sentences total, written into the map (`write_map`) so the rest
of the flow, and the eventual RESULTS entry, can quote it. If the
expectation turns out to have no written source, note that a REQ- doc
should exist; do not write one now — that is the change flow's job.

Outcome: `captured`.

## diagnose

Locate the cause with evidence, or say plainly that you could not. This
step is the fork in the whole flow: everything after it builds on what you
conclude here, so an honest `inconclusive` is worth more than a confident
guess.

Method:

1. Run the relevant test ring (`run_ring`) against the area the goal
   implicates. The ring's output is your first instrument reading — quote
   it, do not paraphrase it. Instruments name their numbers.
2. Read the implicated code (`read_code`) and its tests (`read_tests`).
   Follow the failure from symptom back to mechanism: which line does the
   wrong thing, and why does doing that produce exactly the observed
   behavior — not merely "a" failure, but *this* failure.
3. Check map/TRAPS.md (`read_map`) before finalizing. If the symptom
   matches a recorded trap, the trap's cause is the leading hypothesis and
   your evidence must either confirm it or explain why this time differs.

The bar for `located`: you can name the file, the line or small region,
and the mechanism, and the evidence converges — the cited test output is
explained by that mechanism and by nothing else you found. Correlation
("it started failing after commit X") is a lead, not a location.

If the evidence does not converge on one cause — two candidate mechanisms
remain, or the symptom will not reproduce under the ring — the outcome is
`inconclusive`. Say what you checked, what each candidate would predict,
and what additional evidence would settle it. The flow will stop and ask
the human; that is the designed behavior, not a failure of yours.

Outcome: `located` or `inconclusive`.

## reproduce

Turn the diagnosis into a failing test. The test is the contract for the
rest of the flow: implement makes it pass, verify checks it stayed passing.
A fix without a reproduction is a claim without an instrument.

Write one test under tests_heddle/ (`write_tests`, file name matching
`test_*.py`) that:

- **Fails now, for the diagnosed reason.** Run it (`run_ring`) and show
  the failure output. The failure message must point at the diagnosed
  mechanism — a test that fails for an unrelated setup error reproduces
  nothing.
- **Will pass when — and only when — the defect is fixed.** Do not write a
  test that the current code could pass by accident, and do not weaken the
  assertion until it "almost fails".
- **Is minimal.** The smallest setup that reaches the mechanism. Read the
  neighboring tests (`read_tests`) first and match their fixtures and
  style; a reproduction that reinvents the harness is harder to trust and
  harder to keep.

Name the test after the defect, not after today's date or ticket number.
Show the failing run's output in your step summary — the red output *is*
the deliverable of this step.

Outcome: `reproduced`.

## propose

Describe the smallest change that fixes the reproduced defect, for a human
to approve or reject. You are writing for someone who will decide without
running anything, so the proposal carries all the evidence:

- **The change itself:** every file it touches, and for each, what changes
  and why that serves the diagnosed mechanism. "Smallest" is a real
  constraint — no drive-by refactors, no renames, no fixing adjacent
  smells. If you noticed something else worth fixing, put it in the
  proposal as a *note for the record*, not as part of the change.
- **The protected check:** read map/PROTECTED.md (`read_map`). If any
  touched file or surface is protected, quote the protected entry verbatim
  in the proposal and say so in the first line — the human must know they
  are being asked to authorize a protected edit, because their verbatim
  recorded words are the only thing that permits one. If nothing protected
  is touched, state that you checked.
- **The blast radius:** which tests cover the touched code, and what the
  verify step will run to prove nothing else broke.

The flow gates on this proposal. Write it so a "no" is as easy to give as
a "yes" — a proposal that buries its risks is asking for a rubber stamp,
not approval.

Outcome: `proposed`.

## implement

Apply exactly the approved change — the one from the proposal, not an
improved version of it. If, mid-edit, you discover the approved change is
wrong or insufficient, stop and report that through your outcome summary
rather than silently substituting a better idea: the approval covered a
specific diff, and anything else is unapproved work.

Mechanics:

- Read the current code first (`read_code`); apply the change with
  `write_code` (and `write_tests` only if the approved proposal includes a
  test change — the reproduction test from earlier is not yours to weaken).
- Match the surrounding code's style, naming, and comment density. A fix
  should read like the file always contained it.
- Run the reproduction test (`run_ring`) before finishing. If it now
  passes, say so with the output. If it still fails, still report
  `applied` honestly with the failing output — verify and the flow's
  bounded retry loop handle the iteration; hiding a red run here only
  costs a loop iteration later.

Outcome: `applied`.

## verify

Prove the fix works and nothing else broke. Three instruments, in order of
increasing cost, and each one's actual output quoted:

1. **The smoke wheel** (`run_wheel`) — the fast spin that proves the
   harness still turns at all. If the wheel is red, the repository is
   broken at a level below this defect; that is `red`, and say what the
   wheel printed.
2. **The reproduction ring** (`run_ring`) — the failing test from
   reproduce, now expected green. This is the fix's own instrument.
3. **The full gate** (`run_gate`) — the entire suite. Green means every
   test passes: no skips explained away, no "unrelated" failures waved
   through. A failure you believe is pre-existing is still `red` — name
   it, and let the record show it; the flow and the human decide what it
   means.

The outcome is `green` only if all three are clean. Anything else is
`red`, with the exact failing output in your summary — the flow loops back
to implement at most once more, and after two red cycles it stops and
escalates to the human. Do not spend the second cycle re-running the same
edit hoping for a different answer; if the first cycle's failure is not
understood, the honest move is a red outcome and a clear account of what
is still failing.

Outcome: `green` or `red`.
