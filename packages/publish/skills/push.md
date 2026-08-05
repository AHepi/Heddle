---
name: push
version: 1
steps:
  push:
    tools: [git_push]
    outcomes: [pushed, failed]
---

## push

Push once (git_push) and quote the receipt — the actual command output
naming what moved where. That output is the deliverable of this step.

Your grant allows exactly one call; the runtime enforces it. If the
push fails (rejected, network, auth), the outcome is `failed` with the
exact error quoted — do not retry here, and do not try another route.
A failed push goes back to the human with evidence; a flow that
improvises around a bounded grant has defeated the reason the bound
exists.

Outcome: pushed or failed.
