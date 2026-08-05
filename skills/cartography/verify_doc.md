---
name: verify_doc
version: 1
steps:
  verify_doc:
    tools: [read_map, run_check, head_commit, write_map]
    outcomes: [fresh, stale, unchecked]
---

## verify_doc

You are given one map doc (Inputs: doc=...). Re-run its recorded check
and make its stamp honest. A stamp that advances without a re-run is the
exact decay this flow exists to catch; a stamp left claiming a pass the
check no longer produces is worse than no stamp.

1. Read the doc (read_map) and find its `Check:` command. Translate it
   into run_check arguments exactly — an "improved" variant audits a
   different check than the one recorded.
2. Run it (run_check) and quote the result. Get the current commit
   (head_commit): a stamp names the commit it was measured at.
3. Rewrite the doc (write_map), changing ONLY the stamp line:
   - Check passes → `Verified <today> @ <commit>: <n> passed.` and
     report fresh.
   - Check red → replace the stamp with `STALE <today>: check red —
     <one-line failure>` and report stale. Fix nothing. A stale doc is
     a defect, and cross-routing is strict: park it in your summary as
     a ready-to-run defect entry (one-goal statement, the quoted
     failure, end state), not as something you repair here.
   - No `Check:` line, or a check run_check's domain cannot express →
     mark `STALE <today>: no runnable check recorded` and report
     unchecked, naming the shape the check would need.

Every other line of the doc stays byte-identical — you are refreshing a
stamp, not editing content.

Outcome: fresh, stale, or unchecked.
