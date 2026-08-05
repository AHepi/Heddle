# RESULTS — newest first. The running truth: proven, broken, fixed, parked.

## 2026-08-05 — one skill per step in per-workflow folders; skill-update flow (commit: this one)
The three consolidated skills were re-split on the human's instruction:
one step per file so each skill stays bite-sized for less capable models
and can later be lifted into a tool, grouped one folder per workflow —
skills/shared/ (navigate, record), skills/defect/ (goal, diagnose,
reproduce, propose, implement, verify), skills/change/ (capture, specify,
plan, execute_step, validate, deliver). The expanded prose from the
consolidation survives, compressed per file; skill name = step name =
file name, so references read name.step (diagnose.diagnose). New
orchestrator flows/skill-update.yaml for editing skill files themselves:
survey → human gate → redraft/confirm loop (max 2, wheel-checked) →
record; new skills/skill-update/ (survey, redraft, confirm — redraft.md
carries the house rules for skill files), new tools read_skill/
write_skill rooted at skills/, new role editor. start.yaml routes to all
three orchestrators. Tripwire explanation for the heddle/ diff:
loader.py `load_skills` now discovers skills recursively and errors on
duplicate names — required by the per-workflow folder layout the human
asked for; none of PROTECTED.md items 1–5 are touched. Instruments: gate
21 passed, 0 failed; `heddle check` (installed workaround) on all four
flows — no problems; `heddle show` on skill-update confirms every step
sees its tools. Residue: flows still never run end-to-end with a live
model; summary-form filters still unshipped; validator's vacuous-keys
hole still guarded only by the wheel; HEDDLE_0_1.md §1 still says
`skills/*.md` — the spec is protected, so recording here rather than
editing it: subfolder discovery is a deviation awaiting the human's
verbatim spec decision (HEDDLE_0_2 candidate alongside the self-host
question).

## 2026-08-05 — skills consolidated, flows repaired, smoke wheel added (commit: this one)
The fourteen single-step skills were consolidated into three by discipline
— shared.md (navigate, record), defect.md (goal…verify), change.md
(capture…deliver) — with the prose expanded from one-liners to full step
instructions: purpose, method, quality bar, and outcome semantics for each.
Step names are unchanged, so grants.yaml when-lists carried over. Decision
recorded in README: orchestrators stay in flows/ — control must come only
from flow files (bounded loops, honest conditions, unskippable gates);
prose cannot express or subvert it. The flows themselves were found to be
in a schema the loader does not read (`name:`/`items:` instead of
`flow:`/`steps:`, nested `cond:`, `repeat.body`, and no `as:` roles) — the
previous "no problems" checks were vacuous; see ERRATA and
TRAP-flow-vacuous-keys. All three rewritten to the spec schema with roles
on every step, and human-gate options changed from yes/no (YAML booleans,
which would never equal the condition's string) to approve/reject. New
instrument: the smoke wheel (`run_wheel`, tests_heddle/test_smoke.py) —
flows parse non-vacuously, the root package validates clean from a neutral
copy, every step names a declared role; granted to worker at navigate and
validator at verify/validate. Instruments: gate 19 passed, 0 failed;
`heddle check` (installed workaround) on start/defect/change — no
problems, this time against real content; `heddle show` confirms every
step has visible tools. Residue: flows still never run end-to-end with a
live model; summary-form filters still unshipped; the vacuous-keys hole in
the validator itself is guarded by the wheel but not yet fixed in
heddle/validate.py (protected-adjacent change, needs authorization).

## 2026-08-05 — skills split to one purpose each, router added (commit: this one)
The three multi-step skills (defect.md, change.md, record.md) were replaced
by fourteen single-purpose skills, one step per file, step named after its
purpose. Flows are the orchestrators: defect.yaml and change.yaml rewritten
to the new refs, start.yaml added as the router (navigate, ask purpose,
call one flow). grants.yaml when-lists updated to the new step names. Human
gates now declare explicit options and store_as keys. Flat README.md added
as the entry index for LLMs. Instrument: `heddle check` on start.yaml,
defect.yaml, change.yaml — all print "no problems." (run from an installed
heddle, see TRAPS entry 'self-host-runtime-dir'). Residue: flows still
never run end-to-end with a live model.

## 2026-08-05 — workflow package landed (commit: this one)
The evidence-ledgered workflow package (skills/, flows/, tools.yaml,
grants.yaml, map/) is validated, not yet executed with a live model.
Instrument: `heddle check flows/defect.yaml` and `heddle check
flows/change.yaml` — both print "no problems." (run from an installed
heddle, see TRAPS entry 'self-host-runtime-dir'). Gate: `python -m pytest
-q` — 16 passed, 0 failed. Residue: flows have never been run end-to-end
with a model; the human gates are untested in anger; REC- documents are
unexercised.

## 2026-08-05 — initial build (commit 893044f)
Runtime implements HEDDLE_0_1 stages 1–7. Gate: 16 passed, 0 failed at
893044f. Residue: the §8 rule "every step has at least one usable tool, or
is declared tools: []" is only partially implemented (empty vs missing
tools entry not distinguished); CLI `run` uses a scripted YAML model, not a
live endpoint; `summary` form requires caller-supplied filters and none are
shipped.
