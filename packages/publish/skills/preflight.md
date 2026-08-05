---
name: preflight
version: 1
steps:
  preflight:
    tools: [run_gate, git_status]
    outcomes: [ready, not_ready]
---

## preflight

Prove the release is releasable. Two instruments, both quoted:

1. The gate (run_gate) — the full suite. Zero failures is the only
   acceptable result. A failure you believe is unrelated is still
   `not_ready`; name it and let the human decide on the record.
2. The tree (git_status) — must be clean. An uncommitted change would
   ship silently or not at all; either way the release note would lie.

Report `ready` only when both are clean, quoting both outputs in your
summary. Anything else is `not_ready` with the exact output — never
round up. You prove here; you fix nothing here.

Outcome: ready or not_ready.
