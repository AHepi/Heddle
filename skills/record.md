---
name: record
description: Record the outcome in the ledgers, always.
steps:
  record:
    tools: [read_map, write_map, run_gate]
    outcomes: [recorded]
---
# Record

## record
Append to map/RESULTS.md: what was attempted, what the instruments showed,
what residue remains. If a failure mode was new and non-obvious, add it to
map/TRAPS.md (entries are never deleted). If the map itself was wrong, note it
in map/ERRATA.md. Outcome: recorded.
