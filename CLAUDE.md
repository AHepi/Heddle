# CLAUDE.md

Read AGENTS.md before doing anything in this repository — it is the
working contract (session-start reading, the instrument owed-when table,
same-commit pin rules, branch rules, ledgers). DISCIPLINE.md is the
underlying requirement; the map/ ledgers are the repo's memory.

Quick orientation:

- Run the gate with `python -m pytest -q`; it must be green before any
  push. The smoke wheel is `python -m pytest tests_heddle/test_smoke.py -q`.
- Skills (skills/<workflow>/<step>.md) pin their inventory in
  tests_heddle/test_smoke.py — any skill/flow add, remove, rename, or
  move updates that pin in the same commit.
- map/PROTECTED.md lists surfaces needing the human's verbatim approval
  before they change. heddle/, map/, and HEDDLE_0_1.md are tripwired.
- Never commit directly to main.
