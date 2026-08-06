---
name: verify
version: 1
steps:
  verify:
    tools: [read_code, read_note, run_checks, write_note]
    outcomes: [verified, failed, blocked]
---

## verify

Run the focused verification named in the bounded task (read_note) —
only the tests and static checks relevant to this change
(run_checks), exercising the real public integration path where
practical, not private helpers. No full-suite execution: broad
verification is the qualification gate's job, after every core
blocker has passed focused verification and review.

Write the verification report to notes/ (write_note): exact commands,
test totals and outcomes, and limitations.

- All named checks pass: report verified. A green run makes the task
  READY FOR REVIEW — it does not accept the task, and it does not make
  the repository release-ready.
- A named check fails on this task's change: report failed; the
  failure goes back for a bounded repair within the allowlist.
- A check fails in an unrelated subsystem: record it verbatim, report
  blocked, and stop — a test failure is evidence to classify, not
  authority to repair that subsystem.
- Verification needs credentials, live providers, or destructive
  repair: report blocked. Do not spend tokens or call providers
  without explicit authorization.

Outcome: verified, failed, or blocked.
