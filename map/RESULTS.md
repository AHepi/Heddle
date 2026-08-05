# RESULTS — newest first. The running truth: proven, broken, fixed, parked.

## 2026-08-05 — review-package defects fixed; evidence rules promoted (commit: this one)
Authorization for the heddle/ edits, the human's verbatim words: "Can
you please update workflows to prevent this from happening in the
future?" — following the review that proposed exactly these fixes.
Three defects, each pinned red-then-green in
tests_heddle/test_regressions.py before its fix: (1) `with:` bindings
resolved the parameter NAME in stored values instead of the variable —
write_finding received the literal 'f', never a finding, on every run
of the review flow (interpreter.py `_do_step`; now resolves the stored
value per spec §3); (2) the unstripped `with:` mapping leaked
`__line__` into prompts — a RECURRENCE of
TRAP-marked-yaml-line-key-leak, entry updated (strip_marks now applied
at the consumption point); (3) write receipts crashed on relative
package roots, latent since the initial build
(TRAP-write-receipt-relative-root; tools.py resolves the root).
Protected check: none of PROTECTED.md items 1–5 change semantics —
(1) is code fixed to MEET the spec, (2)/(3) touch no protected
surface; JSONL vocabulary, grant intersection, dispatch order, and the
outcome contract are untouched. Process promotion, one layer per miss:
new TRAP-canned-run-proves-control-flow-only names the vacuous-evidence
mode; ERRATA line corrects 6bd29aa's "end to end" claim; AGENTS.md §2
gains the observation-surface rule (evidence states what it could NOT
see; model-visible content requires a probe) and the trap census
(grep TRAPS for every touched surface before landing, paste the
result); record.md carries the same observation-surface line
in-harness. Instruments: regressions 3 failed at pre-fix code, 3
passed post-fix; gate 25 passed, 0 failed at this commit; `heddle
check` (installed workaround) on all five flows — no problems.
Residue: unchanged from the previous entry; the review package is now
believed functional but has still never run with a live model — the
canned-run trap means only a live run or a fuller probe suite can
claim more; retroactive authorization for 6bd29aa's tools.py change
remains owed.

## 2026-08-05 — post-incident: session contract, mechanical gate, pin grant (commit: this one)
Root-cause pass on the red-main incident. The record shows three
failures stacked: (1) the capture-to-tool change landed directly on
main with the gate unrun and the smoke wheel's SKILLS pin stale
(TRAP-inventory-pin-lags-surface, already fixed); (2) nothing at
session start named the instruments or when each is owed — the exact
gap the discipline-reconciliation entry had recorded as residue, so
the incident was predicted by the ledger and happened anyway because
prose residue binds nobody (new TRAP-gate-rests-on-memory); (3) the
skill-update flow could not have done the removal correctly even if
used — editor held no grant that could move the pin. Fixes, one layer
per failure: AGENTS.md is now the contract for any agent working
outside a running flow (session-start reading order, the owed-when
instrument table closing the §6 residue item, same-commit pin rule,
branch/commit rules, ledger duties), with CLAUDE.md pointing at it and
README naming both; .github/workflows/gate.yml runs the full gate on
every push and pull request so a red gate can no longer land silently
(DISCIPLINE.md §3 — the guarantee no longer rests on memory); redraft
gains write_tests (tool list + editor grant) and the explicit
pin-moves-with-surface rule, so an in-harness skill change can keep
the inventory pin synced in the same redraft. Instruments: gate 22
passed, 0 failed at this commit; `heddle check` (installed workaround)
on all five flows — no problems; wheel clean. Residue: the §6
owed-when item is now closed; still open from before — no live-model
run of defect/change/skill-update, summary filters unshipped,
vacuous-keys validator hole (wheel-guarded), skills/*.md spec wording,
§7 failing-companion convention; new — CI has not yet run on GitHub
(first push of gate.yml will show), and AGENTS.md §2's flow-check row
still requires the installed-heddle workaround, which CI does not
exercise directly (the wheel's neutral-copy validation covers it).

## 2026-08-05 — branch untangled; unstick guardrails ported; red gate fixed (commit: this one)
Three things, one pass. First, the skills-organization branch was
content-identical to what main had already merged (its tip matched the
squash-merge byte for byte) while main had moved on to capture-as-tool —
the "jumble" was stale history, and the branch is restarted from main.
Second, main's gate was RED on a clean checkout: the capture-to-tool
commit deleted the skill but not the smoke test's SKILLS inventory pin,
and no gate ran before it landed (see TRAP-inventory-pin-lags-surface;
pin fixed, gate 21 passed 0 failed at this commit). Third, the four
unstick guardrails from the authority's working repo are ported into
the skills, translated to this harness's grammar: parked notes carry a
ready-to-run entry written at park time (execute_step, implement,
record's residue rule, with a recommended-next when several are
runnable); the plan of record opens with a `State:` line that
execute_step refreshes each call, and execute_step gains write_map to
do it (grants: implementer + write_map at execute_step) — a fresh
session resumes from the plan alone; and every human-facing stop leads
with the decision in one sentence, priced options, and a recommendation
(diagnose inconclusive, verify final red, validate invalid,
execute_step twice-failed). Versions bumped on all seven edited skills.
Instruments: gate 21 passed 0 failed; skill front matter loads (same
gate); tripwire n/a (no protected surface named for skills/tests).
Residue: unchanged from previous entries, plus none new — the
skill-update flow was not used for these edits (they were made directly
on the human's instruction, outside a running harness), which is
consistent with the flow governing model-driven edits, but worth a
thought when the harness starts self-hosting.

## 2026-08-05 — capture.md lifted into a tool (commit: this one)
On the human's instruction, the capture skill became the capture tool — the
README's "one step per file so any skill can later be lifted into a tool"
made concrete for the first time. What moved: tools.yaml gains `capture`
(write_file, root map/, REQ-*.md pattern) — the mechanical act of writing
the requester's verbatim words and numbered requirements; skills/change/
capture.md is deleted; flows/change.yaml drops the capture step (the flow
now runs navigate → specify → spec gate → …); specify.md absorbs the
thinking half (verbatim quote, numbered REQs, append-only amendments,
ambiguity by size, map cross-check) and lists the capture tool; grants
give worker `capture` (write_only) at specify and drop the write_map grant
at capture. No runtime files touched; the tripwire stays clean.
Instruments: `heddle check` (installed workaround, see
TRAP-self-host-runtime-dir) on all four flows — no problems; `heddle show
flows/change.yaml` confirms specify sees read_map, read_code, read_tests,
capture. Residue: unchanged from the previous entry, plus one new item —
the capture tool's pattern overlaps write_map's REQ- branch, so REQ- docs
are now writable through two tools; harmless (both are write_only into
map/), but a future tightening could narrow write_map to exclude REQ-.

## 2026-08-05 — discipline spec captured; skills reconciled against it (commit: this one)
The human authority supplied the Evidence-Ledgered Work Discipline spec;
captured verbatim as DISCIPLINE.md (amendments append-only) and audited
every skill against it. Gaps found and closed, all prose-only (no public
surface — names, steps, outcomes, tools — moved): navigate now reads
ERRATA at session start and carries the seam rules ("read the seam before
either side"; missing seam = not yet written); record now names the
commit measured at, never rounds up negative results, skips re-running
unchanged instruments, and promotes twice-missed workflow failures toward
skill-update; diagnose now reads the error artifact before code
(§4: misattributions cluster where readers skip it); reproduce carries
the durable-check rules (anchor to meaning, never line numbers, scrub
volatile fields); implement and execute_step carry strict cross-routing
(park, don't fix; one tranche, one goal); execute_step pastes the
done-criterion's real output and stops on a twice-failed step; capture is
now verbatim + numbered REQs + append-only amendments + ambiguity routing
(smallest reading recorded as overridable, material forks batched to the
cheapest authority); specify requires machine-decidable checks (no check
= not specified), traces named mechanisms before adopting, and runs the
anti-invention pass; plan requires the mechanical blast-radius census
with pasted hits and orders sub-tranches independently deliverable;
validate never patches; deliver reconciles requirement-by-requirement
(done / done-with-recorded-deviation / deferred-with-their-words);
verify and validate state the zero-failures/never-weaken gate rule.
Instruments: gate 21 passed, 0 failed; `heddle check` (installed
workaround) on all four flows — no problems. Residue: unchanged from the
previous entry (no live-model run, no summary filters, vacuous-keys hole,
spec wording on skills/*.md), plus: DISCIPLINE.md §6's "instrument named
where sessions start with the rule for when it's owed" is only partly
met — README lists the instruments, but per-instrument owed-when rules
are not yet written; and §7's failing-companion convention for equality
checks is not yet practiced in tests_heddle.

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
