# SUB-loader — heddle/loader.py

Owns: parsing the four file types into Package/Skill/SkillStep; YAML line
marks (`__line__`) so validation can name locations; skill front matter and
`## heading` extraction.
Entry points: `load_package(root)`, `load_flow(path)`, `load_skill(path)`,
`strip_marks(obj)`.
State: none — pure functions of the filesystem.
Watch: marked mappings carry `__line__`; filter before iterating (see
TRAPS 'marked-yaml-line-key-leak').
Check: `python -m pytest tests_heddle -q -k loads` exits clean.
Verified 2026-08-05 @ 893044f: 1 passed.
