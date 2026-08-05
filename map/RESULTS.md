# RESULTS — newest first. The running truth: proven, broken, fixed, parked.

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
