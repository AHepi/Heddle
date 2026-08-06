---
name: implement
version: 1
steps:
  implement:
    tools: [read_code, read_note, write_code, write_note]
    outcomes: [implemented, blocked, all_done]
---

## implement

Implement exactly one bounded task — the one the plan note (read_note)
marks as next — and nothing else. If no bounded tasks remain, report
all_done and write nothing.

**The allowlist is a wall.** Change only the task's Allowed files. If
a necessary change falls outside the list, STOP and report blocked —
never widen the list silently. Reuse canonical infrastructure; do not
create parallel storage, routing, validation, transaction, permission,
repair, or packaging mechanisms where shared infrastructure applies.
Keep the change proportional: the smallest change that satisfies the
task's Required behavior.

**Forbidden work stands** (the task note names it): no unrelated
refactoring, opportunistic fixes, excluded systems, broad cleanup,
restoring pre-existing files, unauthorized provider or network calls,
no commits, pushes, resets, or rebases.

**Failures are evidence to classify, not authority to roam.** Repair
implementation-caused focused-test failures within the allowed scope.
When verification exposes an unrelated failure, record it in your
report and STOP — do not follow it into another subsystem. A failure
against a frozen authority (a spec, a pinned fixture, an accepted
contract) is classified before any edit: repair code only when the
authority uniquely determines the expected behavior; route incorrect
fixtures or harness logic to a separate criteria repair; route
ambiguity or contradiction in the authority back through the plan.

**Stop conditions** (report blocked): wrong branch; a needed change
outside the allowlist; the repository contradicting a key assumption;
a test exposing another subsystem's failure; needing credentials,
live providers, destructive repair, or broader authority; user changes
that cannot be preserved safely.

Write the required report to notes/ (write_note): initial and final
branch and HEAD, initial and final status inventory, changed files,
implemented behavior, exact commands, limitations, and confirmation
that no unauthorized action occurred. A green focused test makes the
task ready for review — it does not accept the task and does not make
the repository release-ready.

Outcome: implemented, blocked, or all_done.
