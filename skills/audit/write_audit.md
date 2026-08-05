---
name: write_audit
version: 1
steps:
  write_audit:
    tools: [write_audit]
    outcomes: [written]
---

## write_audit

Turn inspect's findings into the report (write_audit, name
grant-audit.md). One section per finding class, one line per finding:
the quoted evidence, then the recommendation. Order classes as inspect
defines them; within a class, worst first (unlimited write before
over-broad always).

The header states the date and that every line is a proposal the human
may apply or dismiss — grants.yaml is the human's surface and this
report never speaks as if an edit already happened.

If inspect found nothing, write the report anyway: "no findings" with
the date and the flows walked is evidence the audit ran. An absent
report is indistinguishable from an audit that never happened.

Outcome: written.
