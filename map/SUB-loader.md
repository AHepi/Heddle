# SUB-loader — heddle/loader.py

Owns: parsing the four file types into Package/Skill/SkillStep; YAML line
marks (`__line__`) so validation can name locations; skill front matter and
`## heading` extraction. Skills are discovered recursively under skills/
(one folder per workflow is the package convention); skill names are global
across folders and a duplicate name is a load error, not an overwrite.
Entry points: `load_package(root)`, `load_flow(path)`, `load_skill(path)`,
`strip_marks(obj)`.
State: none — pure functions of the filesystem.
Watch: marked mappings carry `__line__`; filter before iterating (see
TRAPS 'marked-yaml-line-key-leak').
Check: `python -m pytest tests_heddle -q -k "loads or folders or duplicate"`
exits clean. Verified 2026-08-05 (skills-per-folder commit): 3 passed.
