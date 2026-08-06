# packages/ — out-of-the-box Heddle packages

Each folder here is a complete, self-contained Heddle package: its own
skills/, flows/, tools.yaml, and grants.yaml. They are distributables —
the root repo's skills/ and flows/ are THIS repo's working discipline
and are not for export; these are.

## Why here and not in the root package

The root of this repository is itself a Heddle package (it governs work
on Heddle). Mixing exportable skills into it would muddy its inventory
pin and its folder-per-workflow convention. A separate packages/ tree
keeps each distributable independently loadable, checkable, and
versioned, with no effect on the root package: nothing in packages/ is
reachable by the root flows or grants.

## Trying one standalone

    python -m heddle --root packages/triage check flows/triage.yaml
    python -m heddle --root packages/triage show  flows/triage.yaml

(From an installed heddle if you are inside this repo — see
TRAP-self-host-runtime-dir. From any other repo, plain `heddle` works.)

## Adopting one into your repo

1. Copy `skills/*` into your package's `skills/<name>/` folder, and the
   flow into your `flows/`. Skill names are global in a package —
   a duplicate name is a load error, so rename in front matter if you
   collide.
2. Merge the package's `tools.yaml` entries into yours. Tool roots are
   directories in YOUR repo — create them or repoint them.
3. Merge the package's `grants.yaml` role into yours. **This step is
   the authorization** — per the spec (§9), installed skills do nothing
   until a flow names them and your grants cover their tools. Read
   every grant before merging; narrow anything you don't want.
4. Optionally splice your own orientation and record steps around the
   flow (in this repo that would be `navigate.navigate` and
   `record.record`) — packages ship self-contained and don't assume
   them.

## Inventory

- **triage/** — turn a raw request into a routed, ready-to-run work
  item: clarify → classify (defect / change / question) → route.
- **publish/** — bounded release: preflight (gate + clean tree) →
  changelog → human gate → push, where the push grant has `limit: 1`.
  The smallest complete demonstration of grant narrowing.
- **postmortem/** — incident to infrastructure: timeline from the
  record only → cause named with evidence or declared inconclusive →
  one prevention per contributing miss.
- **style/** — Pinker's Sense of Style as a workflow: critique a draft
  against the book's checklist with quoted evidence → rewrite into
  classic style as a new note; a sound draft skips the rewrite.
- **bounded/** — bounded implementation: scope + baseline → read-only
  audit → bounded plan → human gate → one bounded task at a time
  (implement → focused verify → strictly read-only review) → core-only
  qualification → delivery gate. The separations are grants: only
  implement writes code, the reviewer holds no write at all, and
  commit/push authority stays with the human.

The package list is pinned in tests_heddle/test_packages.py; adding or
removing a package moves that pin in the same commit (AGENTS.md §3).
