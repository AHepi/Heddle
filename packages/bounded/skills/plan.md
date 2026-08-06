---
name: plan
version: 1
steps:
  plan:
    tools: [read_code, read_note, write_note]
    outcomes: [planned]
---

## plan

Decompose the core blockers from the audit note (read_note) into the
smallest independently reviewable tasks, in dependency order, and
write the plan to notes/ (write_note). Show the complete sequence, but
mark ONLY the next task as executable — never issue executable prompts
for the whole sequence at once.

Never combine unrelated production changes, packaging changes,
cleanup, compatibility repair, and broad qualification into one task.

**Every bounded task must carry these sections:**

- **Objective** — one observable outcome.
- **Allowed files** — the exact files that may change. The implementer
  must stop if a necessary change falls outside the list; the list is
  never widened silently.
- **Required behavior** — precise behavior and invariants.
- **Forbidden work** — unrelated refactoring, opportunistic fixes,
  excluded systems, broad cleanup, restoring pre-existing files,
  unauthorized provider or network calls, full-suite execution before
  final qualification, and unauthorized commits, pushes, resets,
  rebases, or pull requests.
- **Verification** — only the focused tests and static checks relevant
  to this change, exercising real public integration paths where
  practical rather than private helpers.
- **Stop conditions** — wrong branch; a needed change outside the
  allowlist; the repository contradicting a key assumption; a test
  exposing another subsystem's failure; verification needing
  credentials, live providers, destructive repair, or broader
  authority; user changes that cannot be preserved safely.
- **Required report** — initial and final branch and HEAD, initial and
  final status inventory, changed files, implemented behavior, exact
  commands, test totals and outcomes, limitations, and confirmation
  that no unauthorized action occurred.

For every nonterminal task, record the immediate successor's exact
mutation boundary and the contract by which it consumes this task's
outputs. Do not accept an intermediate task whose gate freezes a path
its declared successor is authorized to modify.

Outcome: planned.
