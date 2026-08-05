# Heddle 0.1 — A Small Harness for Skills

Replaces the previous draft entirely. That one imported acceptance-grade
spec discipline into a general-purpose tool and cost a year. This one is four
file types and an interpreter, and it does two things:

1. **A model can only do what it has been granted, and sees nothing else.**
2. **If a package won't run, the reason is printed before anything starts.**

Everything else here exists to serve those two. Nothing proves anything.
There are no hashes, no identities, no canonical encodings, and no
reproducibility claims beyond "the same flow takes the same path".

Estimated implementation: around 1,500 lines and a couple of weeks.

---

## 1. The four files

| File | Written by | Contains |
|---|---|---|
| **Skill** (`skills/*.md`) | you or a model | prose instructions, plus a list of steps and the tools each step wants |
| **Flow** (`flows/*.yaml`) | you or a model | the control structure: order, conditions, loops, sub-flows |
| **Tools** (`tools.yaml`) | you | every action that exists, and its parameter domains |
| **Grants** (`grants.yaml`) | you | which role may use which tool, in what form, where, when |

The runtime loads all four, validates, then walks the flow. There is no
compiler, no intermediate plan, no build step. A flow is interpreted directly.

YAML is used because every language already parses it. A nicer surface syntax
can be added later and desugared into these same structures; don't start there.

---

## 2. Skills

A skill is one Markdown file. Level-2 headings are steps. The front matter says
which tools each step wants and what outcomes it may report.

```markdown
---
name: review
version: 1
steps:
  derive:
    tools: [read_authority]
    outcomes: [done]
  check:
    tools: [read_authority, read_code, run_tests]
    outcomes: [ok, problems_found]
  write_finding:
    tools: [write_report]
    outcomes: [done]
---

## derive
Before reading any implementation, write down what the authority requires.
Cite the clause for each expectation. Name the strongest alternative reading.

## check
Compare the implementation against your derivation. Do not harmonise a
disagreement toward the implementation.

## write_finding
One finding. Include expected, observed, and the narrowest repair boundary.
```

The prose under a heading is what the model is given at that step. That's the
whole binding: a step name in front matter, a heading with the same name, and
prose beneath it.

**Outcomes** are the only thing a step returns to the flow. The model picks one
from the declared list. Free text is written through tools, not returned as
control. This is what keeps `when:` conditions honest, and it costs one
string-membership check.

**The prose is advice; the tool list is enforced.** A skill can say "remain
read-only" all it likes — what makes it read-only is that no write tool appears
in its step's list, or no grant covers one. Nothing checks that the prose and
the grants agree. If you want that check, write a linter later; it isn't part
of the runtime.

---

## 3. Flows

A flow is a list of items executed in order. Seven item types, and that's the
entire language.

```yaml
flow: lifecycle
steps:
  # 1. a step
  - step: review.derive
    as: reviewer

  # 2. a conditional
  - when: outcome(review.check) == problems_found
    then:
      - step: implement.fix
        as: implementer
    else:
      - step: review.write_finding
        as: reviewer

  # 3. a bounded loop
  - repeat:
      max: 3                                  # required
      until: outcome(review.check) == ok
      on_exhausted: stop                      # stop | continue | escalate
      steps:
        - step: review.check
          as: reviewer
        - step: implement.fix
          as: implementer

  # 4. iteration over a list
  - for_each:
      list: open_findings                     # produced by a `collect`
      as: f
      steps:
        - step: review.write_finding
          as: reviewer
          with: {finding: f}

  # 5. a sub-flow, with narrowed authority
  - call: publish
    as: publisher
    grants: [push_once]                       # intersected with what the caller holds

  # 6. a list, built by the machine
  - collect: open_findings
      from: tool(list_findings)

  # 7. a human gate
  - ask: "Accept this review and publish?"
    options: [accept, revise, reject]
    store_as: human_decision
```

Rules, all cheap to implement:

- `repeat` requires `max`. There is no unbounded loop.
- `when` conditions read only: `outcome(step)`, `count(list)`, a stored value
  from `ask`, or a comparison of those. They never read model prose.
- `call` cannot form a cycle. Check with a visited-set at load; error if it
  does.
- `for_each` iterates a list built by `collect`, in the order the tool returned
  it. If you need a different order, sort in the tool.
- A step name is `skill.step` and must resolve to a real heading.

That gives chains, conditionals, loops, iteration, enumeration, sub-flows, and
a human gate. Adding a construct later is adding a case to one dispatch
function.

---

## 4. Tools

A tool is an action that exists. The model never names a path, a command, or a
URL — only a tool and arguments from a closed domain.

```yaml
read_authority:
  kind: read_file
  root: docs/authority/
  params:
    doc: {one_of_files_in: docs/authority/}

read_code:
  kind: read_file
  root: src/
  params:
    path: {one_of_files_in: src/}

run_tests:
  kind: command
  command: ["pytest", "-q", "{suite}"]
  params:
    suite: {one_of: [unit, integration, smoke]}

write_report:
  kind: write_file
  root: reports/
  params:
    name: {pattern: "[a-z0-9-]{1,40}\\.md"}
    body: {text: true}

list_findings:
  kind: read_json
  path: reports/findings.json
```

Parameter domains are `one_of`, `one_of_files_in`, `pattern`, `int_range`, or
`text`. `text` is only ever a body, never a target. **A target is never free
text** — that single rule is most of the security property, and it's a dozen
lines of validation.

Five tool kinds cover almost everything: `read_file`, `write_file`,
`read_json`, `command`, `http`. Add more as you need them; each is a small
handler.

**Base code.** Tools reach only what their `root` says. Roots are declared here
by you, never supplied by a model. The runtime's own directory is not a valid
root and is rejected at load. There is no tool for "read any file", so there is
no way to ask for one.

---

## 5. Grants

Who gets what, in what form, where, when.

```yaml
roles:

  reviewer:
    - tool: read_authority
      form: full
      when: always
    - tool: read_code
      form: full
      when: [check]                    # only during these steps
    - tool: run_tests
      form: scratch                    # runs against a temp copy
      when: [check]
      limit: 20                        # calls per step attempt
    - tool: write_report
      form: write_only                 # does it, returns a receipt not the content
      when: always

  implementer:
    - tool: read_code
      form: full
      when: always
    - tool: write_code
      form: full
      when: [fix]
      limit: 50

  publisher:
    - tool: git_push
      form: full
      when: [push]
      limit: 1
```

**Forms** — four, each a few lines of handler:

| Form | Effect |
|---|---|
| `full` | the result comes back as-is |
| `summary` | a named filter runs on the result first (you write the filter) |
| `write_only` | the action happens; the model gets a receipt, not the content |
| `scratch` | the tool runs against a temp copy; changes are discarded |

`when` is a list of step names, or `always`. That's the whole temporal axis: a
grant is live during named steps and dead everywhere else. `where` is already
handled by the tool's root, so grants don't repeat it — narrow the root or
declare a second tool if you need two scopes.

**Hierarchy.** A `call` passes a `grants:` list. The child's grants are the
intersection of what it asked for and what the caller holds:

```python
child_grants = [g for g in parent_grants if g.name in requested]
```

Widening isn't forbidden — it's not expressible. A child can never end up with
something the parent didn't have, because the only operation is a filter on the
parent's own list. One line, and the hierarchy property falls out of it.

---

## 6. What the model sees

At each step:

```python
visible = [t for t in step.tools
           if role_has_grant(role, t, current_step)]
```

The model is given the step's prose and exactly those tools. Tools it isn't
granted are not mentioned, not described, and not listed as unavailable. They
are simply not in the prompt.

Every call is checked in this order, and the first failure is what gets
reported back:

1. Is the tool visible at this step?
2. Are the arguments in their declared domains?
3. Is the call limit exhausted?

Then it runs, and the form handler shapes the result. A denial goes back to the
model as a short message, counts against the limit, and is logged. It doesn't
end the run unless the step exhausts its attempts.

Results are data. Nothing in a tool result can change the flow, a grant, a
limit, or a condition — not because a scanner catches it, but because the
interpreter never reads control from anywhere except the flow file it loaded at
start.

**Absence, not refusal.** A refused tool invites negotiation. An absent one
isn't a fact the model has to be talked out of.

---

## 7. Running

```
heddle check flows/lifecycle.yaml     # validate only, print problems
heddle show  flows/lifecycle.yaml     # print each step and the tools visible there
heddle run   flows/lifecycle.yaml
```

`show` is worth building early. Being able to read, before a run, the exact
list of things each model will be able to do at each step is the most useful
output the system has.

The log is a JSONL file, one line per event: step started (with the visible
tool list), tool called, tool denied, outcome recorded, flow ended. It's a
record of what happened, not evidence — nobody signs it and nothing chains.

Determinism: the same flow with the same outcomes takes the same path. Model
text isn't reproducible and the runtime doesn't pretend otherwise.

---

## 8. Why a package won't run

Validation runs before anything executes and reports **every** problem it
finds, not the first. Each one names the file, the line, what's wrong, and what
to do about it.

```
grants.yaml:14  reviewer is granted 'write_code', which no tool declares.
                Did you mean 'write_report'? (tools.yaml:31)

skills/review.md:6  step 'check' lists tool 'run_tests', but role 'reviewer'
                has no grant for it at that step.
                Add it to grants.yaml under reviewer with: when: [check]

skills/review.md  front matter declares step 'summarise' with no '## summarise'
                heading in the file.

flows/lifecycle.yaml:22  repeat has no 'max'. Every loop needs a bound.

flows/lifecycle.yaml:31  'when' compares outcome(review.check) to 'passed',
                which isn't in that step's outcomes [ok, problems_found].

flows/lifecycle.yaml:40  call to flow 'publish' → 'review' → 'publish' is a cycle.

flows/lifecycle.yaml:44  call to 'publish' requests grant 'push_once', which
                the calling flow doesn't hold. Grants can only narrow.

tools.yaml:52   tool 'read_anything' has root '/', which is not permitted.
                Declare a specific directory.
```

The full check list, all of which are simple lookups:

- every step reference resolves to a skill and a heading
- every heading has a front-matter entry, and vice versa
- every tool named by a skill exists in `tools.yaml`
- every tool named in `grants.yaml` exists in `tools.yaml`
- every role named in a flow exists in `grants.yaml`
- every `when` step name is a real step
- every `repeat` has a `max`
- every `when` condition compares against a declared outcome
- every `for_each` list is produced by a `collect` earlier in the flow
- every `call` resolves, and the call graph is acyclic
- every requested sub-grant is held by the caller
- every tool root is a real directory and not the runtime's own
- every parameter domain is closed (no free-text target)
- **every step has at least one usable tool, or is declared `tools: []`**

That last one catches the most common real failure: a step that's been given
work it has no way to do. Silence about it would look like a model being lazy.

---

## 9. Adding skills later

Dropping an MD file into `skills/` does nothing. It reaches a run only when a
flow names one of its steps *and* grants cover its tools. Installation is not
authorisation, so there's no risk in having a large skills directory.

Skills are versioned by a number in front matter, for your own reference. The
runtime doesn't pin anything — if you edit a skill, the next run uses the
edited one. That's the right trade for a general-purpose tool; pinning is what
you add if you ever need a run to be defensible, and you probably won't.

Two skills can define the same step name; references are always `skill.step`,
so there's no collision to resolve.

---

## 10. What this doesn't do

- **No identity.** Roles are names in a file. Anyone who can edit the file can
  occupy any role. There's no authentication and none is wanted.
- **No sandbox.** Grants are checked in-process at the call boundary. A
  compromised runtime, a malicious dependency, or a tool that itself escalates
  are all outside this. `scratch` copies files; it doesn't contain anything.
- **No protection from authorised misuse.** A model with a write tool can write
  something bad.
- **No injection immunity.** Tool results can't become control, which is real
  but narrow. A model can still be talked into misusing a tool it holds.
- **No claim your skill is correct**, or that the prose is followed.
- **No evidence.** The log records; it doesn't prove.

If you ever need a run to survive a hostile reader, that's a different system
and it costs what the previous draft cost. Don't build it into this one.

---

## 11. Build order

| Stage | What | Roughly |
|---|---|---|
| 1 | Loaders for the four file types + the validator in §8. No execution. | 2 days |
| 2 | `show`: print each step with its visible tools. | half a day |
| 3 | Interpreter: sequence, `when`, `step` dispatch, outcome capture. | 2 days |
| 4 | Tool handlers (`read_file`, `write_file`, `read_json`, `command`) + domain checks + limits. | 2 days |
| 5 | `repeat`, `for_each`, `collect`, `call` with grant intersection. | 2 days |
| 6 | Forms: `full`, `write_only`, `summary`, `scratch`. | 1 day |
| 7 | `ask` (human gate), JSONL log. | 1 day |

Stage 1 alone is useful: point it at your existing skills and it will tell you
which steps ask for tools nobody grants.

---

## 12. Against the original requirements

| Requirement | Mechanism |
|---|---|
| embeds skills as MD files | §2: headings are steps, prose is the prompt |
| turn a skill into a bounded harness | §3: every loop bounded, every step's tools enumerated |
| modular, hierarchies of control | §5: `call` with grant intersection |
| add skills later | §9: installation is not authorisation |
| who / what / form / where / when | §5: role / tool / form / tool root / `when` |
| limited tool exposure | §6: visible set computed per step, absent otherwise |
| no access to base code | §4: roots declared by you, never free text, runtime dir rejected |
| harness built by the machine | §7: the runtime walks the flow; a model never assembles it |
| authorised endpoints | §4: tools with closed parameter domains |
| user decides authority, machine implements | §5: you write `grants.yaml`; the runtime enforces it |
| deterministic execution | §7: same flow, same outcomes, same path |
| loops, chains, if/then, iteration, enumeration | §3: seven item types |
| can't act outside authorisation | §6: three checks before dispatch, denial by default |
| clear reason when it won't run | §8: all problems, with file, line, and fix |
