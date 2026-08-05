---
name: inspect
version: 1
steps:
  inspect:
    tools: [read_tools, read_grants, show_flow]
    outcomes: [inspected]
---

## inspect

Read the permission system and measure it against actual use. You change
nothing — grants.yaml is human-written and runtime-enforced, and an audit
that edits what it audits is worthless. You report.

1. Read tools.yaml (read_tools) and grants.yaml (read_grants). These are
   fixed commands, not file reads: no tool may root at the package root,
   and a mirror copy would go stale, so the command reads the live file
   and nothing you say can change what it reads.
2. Run show_flow for EVERY flow in flows/ — including review.yaml, which
   no router names; an audit that walks only routed flows misses the
   called ones. The quoted visibility per step is your ground truth: a
   grant is only real where a skill's tool list makes the tool visible.
3. Cross-reference and report four finding classes, measuring each
   grant against the steps ITS role actually runs (an `always` grant
   whose role runs steps that never list the tool is over-broad even
   though invisibility makes it harmless — `always` also covers every
   step the role is ever assigned in the future):
   - **Over-broad always** — a grant `when: always` whose tool is listed
     only by named steps across all skills. Recommend the named steps.
   - **Unlimited write** — a write_file or command-with-side-effects
     grant carrying no limit. Writes are the irreversible class; each
     should say how many.
   - **Dead tool** — a tool no skill's step lists AND no flow's
     `collect ... from: tool(...)` sources (the show output prints
     collect lines — check them before calling a tool dead). A truly
     unreachable tool's grants are fiction either way. Recommend
     deletion, or the step that should expose it.
   - **Splittable role** — a role whose steps use disjoint tool sets;
     two narrow roles audit better than one wide one.
4. Every finding quotes its evidence: the grant line, the show output,
   the skill's tool list. A finding without a quoted line is an opinion,
   not an audit. Findings are proposals for the human — grants.yaml is
   theirs to edit, never yours, and never a skill's.

Note the findings in full in your summary; write_audit turns exactly
that summary into the report.

Outcome: inspected.
