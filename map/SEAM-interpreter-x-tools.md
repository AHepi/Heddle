# SEAM-interpreter-x-tools — read before either side.

The whole seam is three calls: the interpreter computes the visible set and
checks (1) visibility, (2) `check_domain` per param, (3) the limit; then
`run_tool` executes; then `shape_result` applies the grant's form. Only
shaped results re-enter the interpreter, and they land in the model reply
path — never in Ctx, never in a condition. The small fraction of tools.py
the interpreter touches: `check_domain`, `run_tool`, `make_scratch`,
`shape_result`, `Denied`. The small fraction of interpreter.py tools.py
touches: nothing — tools.py never imports the interpreter. If you are
changing denial semantics, both sides move in the same commit as the map
update.
