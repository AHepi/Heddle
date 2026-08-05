# Heddle

A small harness for skills. A model can only do what it has been granted, and
sees nothing else. If a package will not run, the reason is printed before
anything starts.

## Where to start

Read this file, then enter through flows/start.yaml. Every task is routed to
exactly one orchestrator: defect, change, or skill-update.

The working method the skills implement is specified in DISCIPLINE.md
(Evidence-Ledgered Work Discipline), captured verbatim from the human
authority. When a skill's prose and the discipline disagree, the
discipline is the requirement and the skill is the defect.

Working on this repo directly — as an agent or a human — rather than
through a running flow? AGENTS.md is the contract: session-start reading
order, which instrument is owed when, the same-commit pin rule, branch
rules. CLAUDE.md points there. CI (.github/workflows/gate.yml) re-runs
the gate on every push and pull request as the mechanical backstop.

## Orchestrators live in flows/, and only there

The split is deliberate and load-bearing. A skill is prose plus a tool list —
advice for one step. A flow is control — order, conditions, bounded loops,
human gates. The interpreter reads control from nowhere except the flow file
it loaded at start, which is what makes `when:` conditions honest, loops
bounded, and gates unskippable: prose cannot express any of those, and prose
cannot be talked into rerouting them. If orchestration ever migrates into
skill prose, both properties are gone. So:

- **flows/start.yaml** — router. Asks the purpose, calls one orchestrator.
- **flows/defect.yaml** — goal, diagnose, reproduce, propose, human approval,
  implement, verify. Loops implement-verify at most twice.
- **flows/change.yaml** — specify (recording the requester's words verbatim
  via the capture tool), spec gate, plan, plan gate, execute one step at a
  time (at most eight), validate, deliver.
- **flows/skill-update.yaml** — survey a skill and its dependents, human
  approval, redraft, confirm with the smoke wheel (at most two cycles).

Every orchestrator records on every exit path. Flow files use the spec's
schema (`flow:` / `steps:`, `as:` for the role, `when:` with sibling
`then:`/`else:`, `repeat:` with `steps:`). The smoke wheel asserts they parse
non-vacuously — see TRAP-flow-vacuous-keys for why that check exists.

## Skills (skills/): one step per file, one folder per workflow

Each skill file is a single step — bite-sized on purpose, so a less capable
model gets one complete, unambiguous instruction, and so any skill can later
be lifted into a tool without untangling it from siblings. Skill name = step
name = file name; references read `name.step` (e.g. `diagnose.diagnose`).
Expand a skill by growing its prose in place; its public surface (name, step,
outcomes, tools) is what flows, grants, and conditions depend on.

- **skills/shared/** — `navigate`, `record`. Used by every workflow.
- **skills/defect/** — `goal`, `diagnose`, `reproduce`, `propose`,
  `implement`, `verify`.
- **skills/change/** — `specify`, `plan`, `execute_step`, `validate`,
  `deliver`.
- **skills/skill-update/** — `survey`, `redraft`, `confirm`. The workflow
  for editing skill files themselves; redraft.md carries the house rules
  every skill must follow.

## Instruments, cheapest first

- **The smoke wheel** (`run_wheel`) — one fast spin proving the harness
  itself turns: packages load, flows parse non-vacuously, references resolve,
  every step has a role. Backed by tests_heddle/test_smoke.py. Run at
  navigate, verify, validate, and confirm, always before heavier instruments.
- **The ring** (`run_ring`) — targeted tests for the touched area.
- **The gate** (`run_gate`) — the full suite. Green means every test passes.
- **The tripwire** (`protected_tripwire`) — the diff against protected
  surfaces; non-empty means human authorization is required or something is
  wrong.

## Grants and tools

- tools.yaml — every tool the model may call; a target is never free text.
  Skill files are reachable only through `read_skill`/`write_skill`, rooted
  at skills/. The `capture` tool is the mechanical half of recording a
  change's intent: it writes the requester's verbatim words into a REQ- doc;
  specify wields it.
- grants.yaml — which role (worker, implementer, validator, editor,
  recorder) may use which tool at which step. Call-time grants are the
  intersection of parent and child, never wider.

## The map (map/)

The map is the repo's memory. It is updated in the same commit as every
change.

- map/RESULTS.md — newest-first narrative of what was done and what remains.
- map/TRAPS.md — failure modes, never deleted.
- map/ERRATA.md — where the map itself was wrong.
- map/PROTECTED.md — surfaces that need verbatim human authorization to touch.
- map/SUB-*.md — surfaces (loader, validate, interpreter, tools, cli).
- map/SEAM-*.md — boundaries between surfaces.
- map/CON-*.md, map/INV-*.md — contracts and invariants.
- map/REC-*.md — recipes for recurring changes.
- map/REQ-*.md — requirements written by the change flow.

## The runtime (heddle/)

The interpreter and validator live in heddle/. The spec is HEDDLE_0_1.md.
The example package under examples/heddle/ mirrors the spec's own text and
stays as-is for that reason. Tests live in tests_heddle/. Run them with:

    python -m pytest -q

Check a flow before running it (from an installed heddle — validating this
repo from inside itself trips the self-host guard, see
TRAP-self-host-runtime-dir):

    python -m heddle --root . check flows/defect.yaml
