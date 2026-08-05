# REC-add-tool-kind — adding a sixth tool kind.

1. Decide the kind's closed parameter domains FIRST. If any target needs
   free text, the design is wrong — go back. (§4: a target is never free
   text.)
2. Handler: one branch in `run_tool` (heddle/tools.py), a few lines,
   raising `Denied` for out-of-domain requests rather than exceptions.
3. Validator: add the kind to TOOL_KINDS and any root/path rules in
   `validate_package`.
4. Tests: domain accepted/rejected, escape attempt if the kind has a root,
   form interaction (write_only receipt, scratch discard).
5. Same commit: SUB-tools stamp, RESULTS entry, TRAPS entry if the
   motivation was an incident.
