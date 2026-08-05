# publish — bounded release

The smallest complete demonstration of what Heddle's grants buy you: a
flow that can push to a remote **exactly once**, and cannot be talked
into more. preflight proves the tree is clean and the gate is green;
changelog writes the release note from the record; a human gate decides;
push holds `git_push` with `limit: 1`.

    heddle --root . check flows/publish.yaml
    heddle --root . show  flows/publish.yaml   # watch the tools appear per step

The gate command is `python -m pytest -q` — repoint it at your own
suite when adopting. Release notes land in notes/. See ../README.md for
adoption steps; the grants merge is where your repo authorizes the
push, and the limit is enforced by the runtime, not by prose.
