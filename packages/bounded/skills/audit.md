---
name: audit
version: 1
steps:
  audit:
    tools: [read_code, write_note]
    outcomes: [audited]
---

## audit

A read-only scope audit (read_code only — this step writes nothing but
its note). Inspect the existing public APIs, shared infrastructure,
integration boundaries, tests, packaging rules, and compatibility
paths relevant to the requested outcome BEFORE anyone designs
abstractions. Write the findings to notes/ (write_note).

Classify every finding into exactly one class:

1. **Core blocker** — a defect or missing behavior that directly
   prevents the requested outcome. Only these enter the implementation
   sequence.
2. **Compatibility obligation** — existing behavior that must remain
   functional but needs no redesign. These get preservation checks,
   not tasks.
3. **Optional or experimental work** — campaigns, demonstrations,
   archived fixtures, research workflows, prototypes, broad stress
   exercises. Document them; do not turn them into tasks.
4. **Unrelated or pre-existing work** — dirty-tree changes and
   failures outside scope. Document them; do not touch them.

When uncertain whether an item is a core blocker, EXCLUDE it and
explain why. An audit that derives an exact implementation allowlist
is still read-only: a recommended next gate or command is not
permission to implement or execute it.

Outcome: audited.
