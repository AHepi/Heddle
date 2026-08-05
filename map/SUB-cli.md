# SUB-cli — heddle/cli.py

Owns: `check`, `show`, `run`; CannedModel (scripted YAML replies for
deterministic runs); the stdin human gate; `--root` path resolution.
Entry point: `main(argv)`.
State: none.
Watch: `run` re-validates before executing and refuses on any problem;
CannedModel drops scripted calls to invisible tools, mirroring a model
that can't see them.
Check: `python -m pytest tests_heddle -q -k cli` exits clean.
Verified 2026-08-05 @ 893044f: 2 passed.
