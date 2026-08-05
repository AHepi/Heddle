# triage — intake for raw requests

Turns "someone said something" into a routed, ready-to-run work item.
Three steps: clarify what is actually being asked, classify it (defect /
change / question), route it with a ready-to-run entry so starting the
work later costs a paste, not an authoring session.

    heddle --root . check flows/triage.yaml
    heddle --root . run   flows/triage.yaml

Requests and routing notes live in notes/ (both tools root there). See
../README.md for how to adopt this into your own package.
