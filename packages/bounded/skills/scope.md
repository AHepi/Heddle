---
name: scope
version: 1
steps:
  scope:
    tools: [git_status, git_identity, read_code, write_note]
    outcomes: [scoped]
---

## scope

Establish the scope before any plan exists, and record the repository
baseline before anything is edited. Write both into one scope note in
notes/ (write_note).

**User authority comes first.** The user's requested outcome and
explicit exclusions ARE the scope. Adjacent defects, experiments,
compatibility fixtures, optional workflows, architectural improvements,
and general cleanup are NOT work unless the user explicitly included
them. A test failure is evidence to classify, not authority to repair
that subsystem. Do not edit, restore, delete, commit, push, reset,
clean, migrate, or make provider calls unless the task authorizes it.
For a planning-only request, inspect read-only and return a plan.

**State plainly, in the note:**

- Required outcome.
- Core functionality included.
- Explicit exclusions — these are durable boundaries; never
  reintroduce an excluded system through testing or qualification.
- Compatibility behavior to preserve.
- Whether experiments and optional systems are in scope.
- Whether commits, pushes, provider calls, migrations, or destructive
  operations are authorized.
- Definition of done.

Ask the user only when an unresolved choice would materially change
the result. Otherwise make a conservative assumption and identify it
as one.

**Baseline (git_status, git_identity):** record branch, HEAD, and the
status inventory, tracked modifications separately from untracked
paths. If the user named a required branch and the current branch
differs, STOP — do not switch. Assume every existing change belongs to
the user: never restore, overwrite, reformat, stage, or clean
unrelated files.

Outcome: scoped.
