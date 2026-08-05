# Heddle 0.1

A small harness for skills, per `HEDDLE_0_1.md`. Four file types and an
interpreter: a model can only do what it has been granted, and if a package
won't run, the reason is printed before anything starts.

```
python -m heddle --root examples/heddle check flows/lifecycle.yaml
python -m heddle --root examples/heddle show  flows/lifecycle.yaml
python -m heddle --root examples/heddle run   flows/lifecycle.yaml --script script.yaml
```

A package root holds `skills/` (`.md` files, directly or grouped in
subfolders — skill names are global and duplicates are a load error),
`flows/*.yaml`, `tools.yaml`, and `grants.yaml`. `run` takes a script of
canned model replies; for real runs, wire a model callable into
`heddle.Interpreter(pkg, model, human, filters)`, where
`model(prompt, tools, step_ref)` returns
`{"outcome": ..., "tool_calls": [...]}`.

Depends on PyYAML. Tests: `pytest tests_heddle`.
