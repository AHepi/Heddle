# AGENTS.md — the contract for working in this repository

This file exists because of a recorded incident, not as decoration. On
2026-08-05 a change deleted a skill, left the smoke test's inventory pin
stale, and landed directly on main without running the gate — main was
red on a clean checkout until the next session found it
(TRAP-inventory-pin-lags-surface). The skills under skills/ bind a model
running *inside* a flow; nothing bound a session working on the repo
directly. This file is that binding. DISCIPLINE.md is the requirement it
implements; where they disagree, DISCIPLINE.md wins.

## 1. Session start — before any work

Read, in order: **map/RESULTS.md** (top entry in full — it ends with
residue), **map/ERRATA.md** (refuted claims; do not re-trust them),
**map/TRAPS.md** (known failure modes — a recurrence is the cheapest
diagnosis). Then the map docs your task touches (SUB-, SEAM-, CON-,
INV-) and **map/PROTECTED.md** before forming any intention to edit.

## 2. Instruments, and when each is owed

Evidence over prose: every claim names the instrument that produced its
number, and the commit it was measured at. Never claim more than was
measured.

| Instrument | Command | Owed |
|---|---|---|
| Smoke wheel | `python -m pytest tests_heddle/test_smoke.py -q` | At session start, and after any edit to skills/, flows/, tools.yaml, or grants.yaml. |
| Ring | `python -m pytest <target> -q -x` | While iterating on code or tests. |
| Gate | `python -m pytest -q` | Before **every** commit that will be pushed, and before any commit message that cites results. Zero failures is the only acceptable result; never weaken an assertion to get green. |
| Flow check | `heddle check flows/<f>.yaml` from an installed heddle (see TRAP-self-host-runtime-dir) | After any edit to flows/, skills/ front matter, tools.yaml, or grants.yaml. |
| Tripwire | `git diff --name-only HEAD -- heddle/ map/ HEDDLE_0_1.md` | At plan time and before push. Non-empty means explained in the commit or authorized in advance — never retroactively. |

CI (.github/workflows/gate.yml) re-runs the gate on every push and pull
request. CI going red after you pushed means you skipped an owed
instrument — fix forward immediately and record the miss.

Two rules about what evidence *means*, from the 2026-08-05 review-package
incident (a "scripted live run … end to end" shipped a step that never
received its input, because a canned model's replies ignore the prompt):

- **Evidence names its observation surface.** State what the instrument
  could NOT see, next to what it showed. A scripted/canned run proves
  control flow only — it can never verify what a step's model receives.
  Any claim about model-visible content (prompts, bindings, visible
  tools) requires a probe that captured it; if no probe exists for an
  observable, write one before claiming it works
  (tests_heddle/test_regressions.py is the pattern).
- **Trap census before landing.** Grep map/TRAPS.md for every surface
  and mechanism your change touches; a matching entry's rule binds you
  (the `with:` leak was a recurrence of marked-yaml-line-key-leak, whose
  entry already named the exact obligation). Paste the census result —
  "no matching traps" is a claim, make it checkable.

## 3. Same-commit rules

- The map moves in the same commit as the change it describes. A
  separate "update docs" commit is the commit that gets dropped.
- **Every pin moves with its surface.** The smoke test pins the skill
  inventory (`SKILLS`) and the flow list (`FLOWS`) in
  tests_heddle/test_smoke.py. Adding, removing, renaming, or moving a
  skill or flow changes those pins in the same commit — then the wheel
  proves it. This rule is the fix for the motivating incident above.
- DISCIPLINE.md is verbatim authority: amendments append-only, never
  edits to what was recorded.

## 4. Branch and commit rules

- Never commit directly to main. Work on a branch; the gate is green
  before merge.
- A merged branch is finished. Follow-up work restarts the branch from
  main; never stack on merged history.
- Commit messages state what changed and cite the instruments run with
  their numbers. Never an empty body for a non-trivial change, never
  the branch name as the message.

## 5. Protected surfaces

map/PROTECTED.md lists surfaces that move only on the human authority's
verbatim recorded words, obtained **before** the change. Correctness
evidence never substitutes for authorization; a technically perfect
unauthorized change is undeliverable by definition.

## 6. Ledgers — every session that lands work writes them

- **map/RESULTS.md**: newest-first entry — what was attempted, what the
  instruments showed (numbers + commit), what residue remains. Negative
  and inconclusive results recorded as such, never rounded up.
- **map/TRAPS.md**: a new, non-obvious failure mode earns an entry
  naming its motivating incident. Entries are never deleted.
- **map/ERRATA.md**: a falsehood discovered in any committed document
  earns one line. Append-only.
- Cross-routing is strict: a defect found mid-change is parked with a
  ready-to-run note, not fixed. One tranche, one goal.

## 7. Inside vs outside the harness

Flows (flows/*.yaml) govern model-driven runs and enforce grants
mechanically. This file governs everything else — direct edits by
agents or humans. The evidence bar is identical; only the enforcement
differs, which is exactly why the instruments above are owed, not
optional.
