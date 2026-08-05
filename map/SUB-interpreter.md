# SUB-interpreter — heddle/interpreter.py

Owns: walking the flow; the seven item types; per-step visible-tool
computation; the three-check dispatch (visible → domain → limit); grant
intersection on `call`; limits accounting; outcome capture.
Entry points: `Interpreter(pkg, model, human, filters, log).run(flow)`,
`visible_tools(pkg, role, step, tools, held)`.
State: Ctx (outcomes, lists, stored, stopped, escalated) plus per-(step,
tool) call counters. Control is read ONLY from the flow file and Ctx —
never from tool results or model prose.
Watch: denials count against the limit (spec §6); `repeat` on_exhausted
'continue' lets the flow record the failure rather than dying silently.
Check: `python -m pytest tests_heddle -q -k "run or narrows or repeat or outcome"`
exits clean.
Verified 2026-08-05 (this commit): 5 passed.
