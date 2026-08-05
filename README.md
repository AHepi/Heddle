# Heddle

A small harness for skills. A model can only do what it has been granted, and
sees nothing else. If a package will not run, the reason is printed before
anything starts.

## Where to start

Read this file, then enter through flows/start.yaml. Every task is routed to
exactly one orchestrator: defect or change. Each skill below does exactly one
thing. Skill names match their file names; step names match their purpose, so
skills/diagnose.md contains the step diagnose, referenced as diagnose.diagnose.

## Orchestrators (flows/)

- flows/start.yaml — router. Navigates, asks the purpose, calls one flow.
- flows/defect.yaml — goal, diagnose, reproduce, propose, human approval,
  implement, verify, record. Loops implement-verify at most twice.
- flows/change.yaml — capture, specify, spec gate, plan, plan gate, execute
  one step at a time, validate, deliver, record.

## Skills (skills/), one purpose each

- skills/navigate.md — read the map before touching anything.
- skills/goal.md — capture the defect's expected-vs-actual behavior.
- skills/diagnose.md — locate the cause with evidence, or say inconclusive.
- skills/reproduce.md — write the failing test that demonstrates the defect.
- skills/propose.md — propose the minimal fix for approval.
- skills/implement.md — apply exactly the approved fix.
- skills/verify.md — prove the fix works and nothing else broke.
- skills/capture.md — capture the intent of a change.
- skills/specify.md — write the REQ- doc before planning.
- skills/plan.md — plan as ordered steps, run the protected tripwire.
- skills/execute.md — execute one plan step at a time.
- skills/validate.md — check the change against its requirement.
- skills/deliver.md — deliver; map docs move in the same commit.
- skills/record.md — append to the ledgers, always.

## Grants and tools

- tools.yaml — every tool the model may call; a target is never free text.
- grants.yaml — which role may use which tool at which step. Call-time grants
  are the intersection of parent and child, never wider.

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
Tests live in tests_heddle/. Run them with:

    python -m pytest -q

Check a flow before running it:

    python -m heddle --root . check flows/defect.yaml
