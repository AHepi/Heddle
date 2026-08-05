---
name: survey
version: 1
steps:
  survey:
    tools: [read_skill, read_map]
    outcomes: [surveyed]
---

## survey

Understand a skill and everything that depends on it before proposing to
change it. A skill file is not freestanding: flows reference its
`skill.step` names, grants key on its step names, and its tool list is
what the model at that step actually receives.

Read:

1. The target skill itself (read_skill) — front matter and prose. Note
   its name, step names, tools, and outcomes: these are its public
   surface.
2. Its dependents, via the map (read_map): which flows call its steps,
   which grants' `when:` lists name its steps, which conditions compare
   against its outcomes. Renaming a step or outcome breaks all of them.
3. map/PROTECTED.md — skills are not protected surfaces today, but the
   contracts they describe may be; note anything nearby.

Then state, for the human gate that follows: what the skill does now,
what should change and why, and whether the change touches the public
surface (names, outcomes, tools — risky, cascades into flows and grants)
or only the prose (safe, contained). One paragraph.

Outcome: surveyed.
