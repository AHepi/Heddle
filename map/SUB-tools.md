# SUB-tools — heddle/tools.py

Owns: the five tool kinds, the five parameter domains, root containment,
scratch copies, result shaping (full/summary/write_only/scratch).
Entry points: `run_tool(name, tdef, args, pkg_root, scratch_dir)`,
`check_domain(domain, value, pkg_root)`, `shape_result(...)`,
`make_scratch(...)`.
State: none; scratch dirs are created and deleted by the caller
(interpreter).
Watch: a target is never free text — `text` domains on read/http tools are
rejected at validation; `one_of_files_in` resolves and re-roots candidates
to catch `..` escapes.
Check: `python -m pytest tests_heddle -q -k "domain or forms"` exits clean.
Verified 2026-08-05 @ 893044f: 2 passed.
