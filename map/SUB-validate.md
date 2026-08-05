# SUB-validate — heddle/validate.py

Owns: the §8 check list. Reports EVERY problem with file, line, and fix;
never executes anything.
Entry point: `validate_package(pkg, flow_path) -> list[Problem]`.
State: none. Recurses into called flows with a visited-set (cycle check).
Watch: `when` outcome comparisons are validated by regex over the condition
text — a condition the regex can't see is a condition not checked.
Check: `python -m pytest tests_heddle -q -k "validator or cycle or widening or root"`
exits clean.
Verified 2026-08-05 (this commit): 8 passed.
