---
name: deliver
version: 1
steps:
  deliver:
    tools: [git_status, git_identity, read_code, read_note, write_note]
    outcomes: [ready]
---

## deliver

Prepare delivery. Qualification success does NOT authorize a commit or
push — that authority is the human's gate in the flow, and it is
handled separately from every test result.

Before writing the delivery note:

- Recheck branch, HEAD, and status (git_identity, git_status) against
  the baseline in the scope note (read_note). If the branch or
  repository identity changed unexpectedly, STOP and say so.
- Compare the final status inventory with the baseline and explain
  every entry this task introduced.
- Separate intended changes from unrelated dirty-tree contents; the
  unrelated entries belong to the user and stay untouched.
- Identify every file proposed for inclusion, and confirm excluded
  experiments and fixtures are absent.
- Never use destructive Git cleanup to manufacture a clean worktree.

Write the delivery note to notes/ (write_note): the intended file
list, the summarized test and review evidence, the remaining
limitations and debt, and the exact actions that still require the
user's explicit approval (commit, push, pull request).

Do not call the work complete, release-ready, or safe to push merely
because tests passed. Completion means: every included blocker
implemented, focused-tested, and separately reviewed; the core-only
qualification matrix passed apart from identified pre-existing or
excluded failures; delivery changes separated from unrelated work;
limitations stated; and commit or push authority still with the user.

Outcome: ready.
