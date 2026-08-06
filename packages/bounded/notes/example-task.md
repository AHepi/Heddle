# Example bounded task (template)

## Objective
Add a `farewell(name)` function to repo/seed.py returning
`"goodbye, {name}"`, with one focused test.

## Allowed files
- repo/seed.py
- repo/test_seed.py

## Required behavior
`farewell("bounded")` returns `"goodbye, bounded"`. `greet` keeps its
exact current behavior.

## Forbidden work
No refactoring of `greet`, no new modules, no packaging changes, no
full-suite execution, no commits or pushes.

## Verification
`python -m pytest repo/ -q` (the package's run_checks command).

## Stop conditions
A needed change outside the allowed files; the repo contradicting the
task's assumptions; a failure in an unrelated subsystem.

## Required report
Initial and final branch and HEAD, status inventory, changed files,
exact commands, test totals, limitations, and confirmation that no
unauthorized action occurred.
