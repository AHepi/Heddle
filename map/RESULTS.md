# RESULTS — newest first. The running truth: proven, broken, fixed, parked.

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
