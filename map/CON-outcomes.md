# CON-outcomes — the only channel from model to flow.

A step returns one string from its declared outcome list; the interpreter
rejects anything else (`outcome_rejected`, then HeddleError). Conditions
read outcomes, counts, and stored human answers — never prose. This is
what keeps `when:` honest: the model cannot talk the flow into a branch,
it can only pick a declared result. When adding a step, declare outcomes
that a reviewer could machine-check were possible; a step with one outcome
is a step whose result is ignored, and that's fine if honest.
