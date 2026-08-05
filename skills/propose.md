---
name: propose
description: Propose a minimal fix for human approval.
steps:
  propose:
    tools: [read_code, read_map]
    outcomes: [proposed]
---
# Propose

## propose
Describe the smallest change that fixes the reproduced defect. Name every file
it touches. Check map/PROTECTED.md: if the change touches a protected surface,
say so explicitly and quote the surface. Outcome: proposed.
