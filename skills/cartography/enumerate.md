---
name: enumerate
version: 1
steps:
  enumerate:
    tools: [list_map, read_map, write_index]
    outcomes: [indexed]
---

## enumerate

List the map docs that carry verification stamps, so the sweep can walk
them. Run list_map for the directory listing, then read each candidate
(read_map) and keep the docs with a `Check:` line — today that is the
SUB-, CON-, INV-, and REC- docs. RESULTS, TRAPS, ERRATA, and PROTECTED
have no stamps and are not swept; a REQ- doc is stamped at delivery and
is likewise out of scope for the standing sweep.

Write the survivors as a JSON array of bare filenames (write_index,
name map-index.json), e.g. ["SUB-tools.md", "SUB-loader.md"]. The next
step's collect reads exactly this file — valid JSON, no commentary.

Note in your summary how many docs qualified and the oldest stamp date
among them; that pair is the sweep's baseline.

Outcome: indexed.
