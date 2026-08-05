# ERRATA — append-only. Every discovered falsehood in a committed document.
# One writer per ledger. Corrections stated plainly and once.
# Format: date | document | claim | what is actually true | evidence

2026-08-05 | map/RESULTS.md (entry "skills split to one purpose each") |
"`heddle check` on start.yaml, defect.yaml, change.yaml — all print 'no
problems.'", offered as evidence the flows were valid | the flows used
`name:`/`items:` keys that `load_flow` does not read, so validation saw
empty flows and passed vacuously; the flows also used `cond:`/`body:`
shapes the interpreter does not implement, assigned no roles (every tool
call would have been denied), and gated on yes/no options that YAML parses
as booleans | evidence: heddle/loader.py `load_flow`; re-running check
after the 2026-08-05 rewrite validates real content (19-test gate green,
smoke wheel added as the standing guard)
