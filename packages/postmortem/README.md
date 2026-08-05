# postmortem — incident to infrastructure

DISCIPLINE.md §8 in a box: a workflow failure becomes a permanent part
of the workflow instead of a repeated cost. Timeline from the record
only (no theorizing), cause named with evidence or declared
inconclusive, then one prevention per contributing miss — each either
mechanical or owed at a named boundary, never "be more careful".

    heddle --root . check flows/postmortem.yaml
    heddle --root . run   flows/postmortem.yaml

Incident notes and the resulting prevention/trap entries land in
notes/. See ../README.md for adoption; wire the trap entry into your
own TRAPS ledger if you keep one.
