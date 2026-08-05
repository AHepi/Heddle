---
name: mutation_probe
version: 1
steps:
  mutation_probe:
    tools: [read_map, read_code, write_code, run_check, restore_file, head_commit]
    outcomes: [proven, vacuous]
---

## mutation_probe

Prove one sampled check can still fail. A check that stays green while
the thing it guards is broken proves nothing — it only looks like a
guard, and the discipline's word for that is vacuous.

1. Sample one doc the sweep just stamped fresh — the one whose previous
   stamp was oldest, so probes rotate across the map over runs. Read
   the doc (read_map) and the code its check guards (read_code).
2. Break the guarded thing minimally and reversibly (write_code): one
   behavior-changing edit — invert a return, drop a condition, swap two
   branches. Nothing cosmetic; the break must be one a real regression
   would produce.
3. Run the doc's check (run_check). It MUST go red — quote the failure.
   Then restore (restore_file) and run the check once more: green
   again, quoted, with the commit (head_commit). Never report before
   the restore has landed and re-passed; a probe that leaves the repo
   broken is worse than no probe.
4. Red-then-restored → proven. Green while broken → vacuous: restore
   immediately, then name in your summary the doc and the property its
   check claims to guard. A vacuous check is a defect — park it as a
   ready-to-run defect entry; you do not write the replacement check
   today.

One probe per run. The sweep's breadth plus the probe's rotating depth
is what keeps the map honest over time.

Outcome: proven or vacuous.
