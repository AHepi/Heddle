---
name: changelog
version: 1
steps:
  changelog:
    tools: [git_log, write_note]
    outcomes: [written]
---

## changelog

Write the release note from the record, not from memory. Read the
recent history (git_log) and write one note (write_note, name
release-*.md) containing:

- What ships: the changes since the last release, each in one line of
  behavior ("validator now reports X"), not diff-speak ("refactored
  validate.py").
- Evidence: the preflight results, quoted — gate numbers and clean
  tree — so the note carries its own proof of releasability.
- Anything deliberately NOT shipping that a reader might expect, with
  one line of why. Nothing silently dropped.

The human at the release gate reads only this note before deciding —
write it so an informed "abort" is as easy as a "push".

Outcome: written.
