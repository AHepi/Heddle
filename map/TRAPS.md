# TRAPS — read before investigating. Entries never deleted, only rewritten
# to say when they were fixed. A recurrence is the cheapest diagnosis.

## TRAP-condition-tokenizer-lastgroup — fixed 2026-08-05
Symptom: every `when`/`until` condition raised "bad term in condition".
Cause: `re.Match.lastgroup` reports the LAST named group that participated
in the match — for the `call(...)` alternative that is `arg`, not `call` —
so the tokenizer misclassified tokens. Incident: first test run of the
initial build, 12 of 16 tests failed. Fix: test `m.group("call")` etc.
explicitly (heddle/conditions.py, `tokenize`).

## TRAP-marked-yaml-line-key-leak — fixed 2026-08-05
Symptom: validation crashed with `TypeError: 'int' object is not iterable`.
Cause: the line-number marker (`__line__`) injected into every YAML mapping
leaked into the `roles:` dict; iterating "entries" hit the int. Incident:
same build run. Fix: `load_package` keeps only list-valued role entries
(heddle/loader.py). Any future consumer of marked YAML must strip or filter
markers before iterating.

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
