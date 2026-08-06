# bounded — bounded implementation as a Heddle package

A distributable Heddle package for substantial repository work that
must not become an open-ended overhaul: features, remediation, and
release preparation in large or dirty repositories where scope drift,
unauthorized cleanup, role collapse, or premature delivery must be
prevented.

The governing sequence, one step per skill file:

```
scope -> audit -> plan -> [human plan gate] ->
  implement one bounded task -> verify (focused) -> review (read-only)
  -> repair or continue ->
qualify (core-only) -> deliver -> [human delivery gate]
```

## What the runtime enforces (grants.yaml, not prose)

- Only `implement` may write code; the lead plans and reports but
  holds no `write_code` at all.
- `review` is strictly read-only: the reviewer can read the code and
  the notes and write its report — no `write_code`, no `run_checks`.
- Focused checks run at `verify`; the broad suite runs only at
  `qualify`, after every blocker has passed review.
- Commit and push authority never leaves the human: the flow asks at
  the plan gate and again at the delivery gate.

## What the prose carries

The bounded-task format (objective, allowed files, required behavior,
forbidden work, verification, stop conditions, required report), the
audit classification (core blocker / compatibility obligation /
optional / unrelated — when uncertain, exclude), failure classification
(evidence, not authority to roam), the two review tiers, the
qualification attempt-family ledger (two terminal failures stop the
family; only a new grant reopens it), and the completion standard
(green tests are not acceptance and not release-readiness).

## Layout

- `skills/` — scope, audit, plan, implement, verify, review, qualify,
  deliver (one step per file; name = step = filename).
- `flows/bounded.yaml` — the orchestrator above.
- `tools.yaml` — `repo/` for code, `notes/` for the working record,
  fixed commands for checks and Git identity. Repoint `run_checks` and
  the roots at your own tree when adopting.
- `grants.yaml` — roles `lead`, `worker`, `reviewer`.
- `repo/` — a tiny seed module and test so a first run has real bytes.
- `notes/example-task.md` — a bounded task in the required format, as
  a template.

## Adoption

Copy the package into your repo and merge its grants into your
`grants.yaml` — the merge is the authorization (HEDDLE_0_1 §9). Skill
names here (`scope`, `plan`, `review`, ...) are generic; on a
collision the loader's duplicate-name error fires — rename the skill
(and its step and flow refs) to your namespace.
