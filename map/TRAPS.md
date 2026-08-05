# TRAPS — read before investigating. Entries never deleted, only rewritten
# to say when they were fixed. A recurrence is the cheapest diagnosis.

## TRAP-inventory-pin-lags-surface — fixed 2026-08-05
Symptom: the gate is red on a clean checkout of main
(test_skills_load_from_workflow_folders: "Extra items in the right set:
'capture'"). Cause: the capture-to-tool commit deleted
skills/change/capture.md but did not update the smoke test's SKILLS
inventory pin in the same commit, and the gate was not run before that
commit landed — its RESULTS entry cites `heddle check` and the tripwire
only. Incident: found 2026-08-05 during the skills-organization pass.
Fix: pin updated; the general rule is the same one the discipline
already states for the map — an instrument that pins a surface moves in
the SAME commit as the surface, and the gate runs before anything
lands. An instrument nobody re-runs rots silently.

## TRAP-condition-tokenizer-lastgroup — fixed 2026-08-05
Symptom: every `when`/`until` condition raised "bad term in condition".
Cause: `re.Match.lastgroup` reports the LAST named group that participated
in the match — for the `call(...)` alternative that is `arg`, not `call` —
so the tokenizer misclassified tokens. Incident: first test run of the
initial build, 12 of 16 tests failed. Fix: test `m.group("call")` etc.
explicitly (heddle/conditions.py, `tokenize`).

## TRAP-marked-yaml-line-key-leak — fixed 2026-08-05; RECURRED 2026-08-05, fixed again
Symptom: validation crashed with `TypeError: 'int' object is not iterable`.
Cause: the line-number marker (`__line__`) injected into every YAML mapping
leaked into the `roles:` dict; iterating "entries" hit the int. Incident:
same build run. Fix: `load_package` keeps only list-valued role entries
(heddle/loader.py). Any future consumer of marked YAML must strip or filter
markers before iterating.
Recurrence: the review package's `with:` mapping was consumed unstripped in
`_do_step`, so models received `__line__=27` in their prompt — exactly the
consumer this entry warned about, missed because nobody ran a trap census
at implement time. Fixed with strip_marks at the consumption point; probe
pinned in tests_heddle/test_regressions.py. The census rule is now in
AGENTS.md §2.

## TRAP-cli-flow-path-cwd — fixed 2026-08-05
Symptom: `heddle --root PKG run flows/x.yaml` reported "flow does not
parse: No such file or directory". Cause: flow and script paths resolved
against the process cwd, not `--root`. Fix: `_flow_path` in heddle/cli.py
resolves relative paths against `--root`.

## TRAP-self-host-runtime-dir — open, documented workaround
Symptom: validating a package whose tools legitimately target `heddle/`
(the runtime's own source, e.g. developing heddle itself) is rejected:
"root 'heddle/', which is not permitted". Cause: §8 rejects any root equal
to the running interpreter's directory, and running `python -m heddle` from
the repo puts the repo's `heddle/` on `sys.path`. Workaround: install
heddle elsewhere (`pip install --target=/tmp/heddle-lib .`) and run with
that on PYTHONPATH from a neutral cwd — the tool root then differs from the
runtime dir and the guard stands down. Open question: whether self-hosting
deserves a principled exception in the spec; that is a HEDDLE_0_2 decision,
not something to hack around in validate.py.

## TRAP-flow-vacuous-keys — open at the validator, guarded by the smoke wheel
Symptom: `heddle check` prints "no problems" for a flow that could never
run. Cause: `load_flow` (heddle/loader.py) reads the top-level keys
`flow:` and `steps:`; a file using anything else (`name:`/`items:`) loads
as `(None, [])`, and validation passes because there is nothing to check.
Incident: 2026-08-05 — the root flows were committed in a schema of their
own (`items:`, nested `cond:`, `repeat.body`, no `as:` roles) and their
"no problems" results were recorded as validation (see ERRATA). Guard:
tests_heddle/test_smoke.py (the smoke wheel) asserts every root flow
parses with a name and non-empty steps, validates clean, and assigns a
declared role to every step. Real fix — the validator complaining about
unrecognized top-level keys — is a heddle/validate.py change and needs
authorization; open.

## TRAP-gate-rests-on-memory — fixed 2026-08-05
Symptom: a red gate lands on main and nobody notices until the next
session checks out clean. Cause: the discipline's rules bind a model
running inside a flow (verify/validate own the gate there), but most
real work on this repo happens in sessions editing files directly —
and nothing at session start named the instruments or when each is
owed, and nothing mechanical ran them. The gap was even on the record:
the 2026-08-05 discipline-reconciliation RESULTS entry listed
"per-instrument owed-when rules are not yet written" as residue, and
that exact gap produced the incident (capture-to-tool landing with the
gate unrun; see TRAP-inventory-pin-lags-surface). Fix, three layers:
AGENTS.md is the session-entry contract (owed-when table, same-commit
pin rule, branch rules) with CLAUDE.md pointing at it;
.github/workflows/gate.yml re-runs the gate on every push and PR so
the guarantee no longer rests on memory (DISCIPLINE.md §3); and the
skill-update flow can now actually keep the pin synced — redraft
gained write_tests, which it previously lacked, so an in-harness skill
removal could not have moved the pin at all.

## TRAP-canned-run-proves-control-flow-only — recorded 2026-08-05
Symptom: a defect ships in a path a RESULTS entry claims was "exercised
end to end". Cause: scripted/canned model runs return fixed replies that
ignore the prompt, so they verify control flow (which steps ran, in what
order) and nothing about what any step's model received — prompt content,
`with:` bindings, and visible-tool lists are unobserved. Incident: the
review package's `with: {finding: f}` handed write_finding the literal
string 'f' (and a leaked __line__ marker) through a run recorded as end
to end; found only by a prompt-capturing probe. Fix: interpreter binding
corrected (value of stored name, marks stripped); permanent probes in
tests_heddle/test_regressions.py; AGENTS.md and record.md now require
evidence to name its observation surface.

## TRAP-write-receipt-relative-root — fixed 2026-08-05
Symptom: every write-tool call crashes with ValueError ("is not in the
subpath of ''") when the package root is relative (`heddle --root . run`).
Cause: the write_file receipt compared a resolved path against the
unresolved effective root (heddle/tools.py). Latent since the initial
build; surfaced by the review-package probe. Fix: resolve the root in the
receipt; regression test in tests_heddle/test_regressions.py.
