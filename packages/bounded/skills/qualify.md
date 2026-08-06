---
name: qualify
version: 1
steps:
  qualify:
    tools: [read_code, read_note, run_checks, write_note]
    outcomes: [qualified, unqualified]
---

## qualify

The final qualification gate. Broad verification runs only now — after
every core blocker has passed focused verification AND read-only
review. Confirm that precondition from the notes (read_note) before
running anything; if a task skipped review, the work is not ready and
the honest outcome is unqualified.

Define a CORE-ONLY qualification matrix covering, where applicable:
static checks; focused integration suites; core replay or
reconstruction checks; isolation and concurrency checks; historical
read-only checks; supported old-format compatibility; build and
isolated installation of the artifact (smoke tests must import the
INSTALLED artifact, not the source checkout — guard against
repository-working-directory imports, inherited PYTHONPATH, and
previously installed packages); supported entry-point smoke tests;
offline cross-platform checks; and proof that excluded systems are not
required by the core release.

Excluded experimental systems never block core qualification. Report
optional or archived full-suite failures separately, as debt. No live
providers and no token spend without separate authorization.

**Attempt accounting.** Before a qualification campaign starts, record
its attempt family: objective + subject + mutation boundary +
acceptance predicate, plus every prior terminal result in that family.
A terminal FAIL, BLOCKED, or abandonment consumes an attempt — a new
run ID, evidence root, wrapper, or label does not reset the ledger.
Stop after two terminal failed executions in one family; only a new
explicit grant authorizes another attempt, and it does not erase the
family history.

Write the qualification report to notes/ (write_note): the matrix,
each result, pre-existing and excluded failures named separately, and
the attempt ledger.

Outcome: qualified or unqualified.
