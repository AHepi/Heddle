# style — Pinker's Sense of Style as a workflow

Built from *The Sense of Style* (Steven Pinker, 2014). Two steps:
critique holds a draft against the book's checklist — classic style,
the curse of knowledge, zombie nouns and hedges, the tree (working
memory), arcs of coherence, and the usage rulings (break the folklore
rules; hold the line on *disinterested*, *enormity*, *fortuitous*,
*refute* and their kin) — every finding quoting the draft's own words.
rewrite then re-sees the draft and writes a NEW note, so the
before/after pair is the evidence the pass happened. A sound draft
skips the rewrite.

    heddle --root . check flows/style.yaml
    heddle --root . run   flows/style.yaml

Drafts live in drafts/ (both tools root there); a seed draft waits
there so a first run has something to chew. See ../README.md for how
to adopt this into your own package — the grants merge is the
authorization.
