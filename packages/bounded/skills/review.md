---
name: review
version: 1
steps:
  review:
    tools: [read_code, read_note, write_note]
    outcomes: [accept, findings]
---

## review

A separate, strictly read-only review of the task that just passed
focused verification. You have no write access to the code — the grant
enforces it. Read the task definition and the verification report
(read_note), then examine the changed files and the named integration
boundary (read_code). Nothing else: no unrelated investigation, no
full-suite execution, no provider calls, no edits, no commits.

Check, through the real execution path:

1. The behavior works through the public integration path, not just
   in private helpers.
2. Enforcement happens BEFORE mutation, dispatch, or any irreversible
   action, where relevant.
3. Fail-closed behavior: a missing input, permission, or authority
   stops the operation rather than waving it through.
4. Supported behavior is preserved — the compatibility obligations
   from the audit still hold.
5. Platform-sensitive edge cases that apply to this change.
6. False-positive tests: tests that cannot fail, or that bypass the
   real integration path.

Return only actionable findings, each with an exact file and line
reference; write the review report to notes/ (write_note). With no
actionable findings, RECOMMEND acceptance — you do not mark the task
accepted and you do not authorize its successor. Acceptance is the
human's gate in the flow.

**Two tiers.** This checklist is the task-level tier. A review that
precedes flipping a phase-completion or verification flag, or that
precedes an acceptance decision, is phase-level: it needs an
independent reviewer reading the controlling authorities and fixture
negative space, beyond the changed files, with no acceptance
authority. Route that to a separate independent review rather than
using this checklist.

Outcome: accept (a recommendation) or findings.
