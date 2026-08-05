"""heddle.interpreter — walks the flow. No compiler, no plan, no build.

The model is given the step's prose and exactly its visible tools (§6).
Every call is checked: visible? args in domain? limit? Then it runs and the
form shapes the result. Denials go back to the model and are logged.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from . import conditions
from .errors import HeddleError
from .loader import Package, load_flow, strip_marks
from .runlog import RunLog
from .tools import Denied, check_domain, make_scratch, run_tool, shape_result


@dataclass
class Ctx:
    outcomes: dict = field(default_factory=dict)
    lists: dict = field(default_factory=dict)
    stored: dict = field(default_factory=dict)
    stopped: bool = False
    escalated: bool = False


def grant_entries(pkg: Package, role: str) -> list[dict]:
    return [strip_marks(g) for g in (pkg.grants.get(role) or [])]


def visible_tools(pkg: Package, role: str, step_name: str,
                  skill_tools: list[str], held: list[str] | None = None) -> list[str]:
    """§6: step tools intersected with the role's live grants (and the
    narrowed grant list, for sub-flows)."""
    out = []
    for t in skill_tools:
        for g in grant_entries(pkg, role):
            if g.get("tool") != t:
                continue
            when = g.get("when", "always")
            if when != "always" and step_name not in (when or []):
                continue
            if held is not None and t not in held:
                continue
            out.append(t)
            break
    return out


class Interpreter:
    def __init__(self, pkg: Package, model, human=None, filters: dict | None = None,
                 log: RunLog | None = None):
        """model: callable(prompt, tools, step_ref) -> {"outcome": str,
        "tool_calls": [{"tool": name, "args": {...}}, ...]}
        human: callable(question, options) -> choice
        filters: named summary filters for form=summary."""
        self.pkg, self.model = pkg, model
        self.human = human or (lambda q, opts: opts[0])
        self.filters = filters or {}
        self.log = log or RunLog(pkg.root / "heddle-run.jsonl")
        self.limits: dict[tuple, int] = {}

    # ------------------------------------------------------------ run

    def run(self, flow_path: Path, held: list[str] | None = None,
            ctx: Ctx | None = None) -> Ctx:
        name, items = load_flow(Path(flow_path))
        ctx = ctx or Ctx()
        self.log.event("flow_started", flow=name)
        self._walk(items, ctx, held)
        self.log.event("flow_ended", flow=name,
                       stopped=ctx.stopped, escalated=ctx.escalated)
        return ctx

    def _walk(self, items, ctx: Ctx, held):
        for item in items:
            if ctx.stopped:
                return
            item = item if isinstance(item, dict) else {}
            clean = {k: v for k, v in item.items() if k != "__line__"}
            if "step" in clean:
                self._do_step(clean, ctx, held)
            elif "when" in clean:
                branch = "then" if conditions.evaluate(
                    clean["when"], ctx.outcomes, ctx.lists, ctx.stored) else "else"
                self._walk(clean.get(branch) or [], ctx, held)
            elif "repeat" in clean:
                self._do_repeat(clean["repeat"], ctx, held)
            elif "for_each" in clean:
                self._do_for_each(clean["for_each"], ctx, held)
            elif "collect" in clean:
                self._do_collect(clean, ctx, held)
            elif "call" in clean:
                self._do_call(clean, ctx, held)
            elif "ask" in clean:
                self._do_ask(clean, ctx)

    # ------------------------------------------------------------ items

    def _do_step(self, item, ctx: Ctx, held):
        ref = item["step"]
        sname, stname = ref.split(".", 1)
        role = item.get("as", "default")
        skill = self.pkg.skills[sname]
        step = skill.steps[stname]
        vis = visible_tools(self.pkg, role, stname, step.tools, held)
        self.log.event("step_started", step=ref, role=role, tools=vis)

        prompt = step.prose
        if item.get("with"):
            # §3: `with: {finding: f}` binds the VALUE of stored name f
            # (a for_each var or ask key); a name not in stored passes
            # through as a literal. Marked-YAML mappings carry __line__ —
            # strip before iterating (TRAPS marked-yaml-line-key-leak).
            bindings = {
                k: ctx.stored.get(v, v) if isinstance(v, str) else v
                for k, v in strip_marks(item["with"]).items()}
            prompt += "\n\nInputs: " + ", ".join(
                f"{k}={v!r}" for k, v in bindings.items())

        reply = self.model(prompt, vis, ref) or {}
        for call in reply.get("tool_calls") or []:
            self._tool_call(call, role, stname, ref, vis)
        outcome = reply.get("outcome")
        if outcome not in step.outcomes:
            self.log.event("outcome_rejected", step=ref, outcome=outcome,
                           allowed=step.outcomes)
            raise HeddleError(
                f"{ref}: model returned outcome {outcome!r}, "
                f"not in {step.outcomes}")
        ctx.outcomes[ref] = outcome
        self.log.event("outcome_recorded", step=ref, outcome=outcome)

    def _tool_call(self, call, role, stname, ref, vis):
        tname = call.get("tool")
        args = call.get("args") or {}
        key = (ref, tname)
        used = self.limits.get(key, 0)

        grant = next((g for g in grant_entries(self.pkg, role)
                      if g.get("tool") == tname and
                      (g.get("when", "always") == "always"
                       or stname in (g.get("when") or []))), None)

        def deny(reason):
            self.limits[key] = used + 1
            self.log.event("tool_denied", step=ref, tool=tname, reason=reason)
            return {"denied": reason}

        # 1. visible at this step?
        if tname not in vis or grant is None:
            return deny("tool not visible at this step")
        # 2. arguments in declared domains?
        tdef = self.pkg.tools[tname]
        for pname, dom in (tdef.get("params") or {}).items():
            if pname not in args:
                return deny(f"missing argument '{pname}'")
            if not check_domain(dom, args[pname], self.pkg.root):
                return deny(f"argument '{pname}' outside its domain")
        # 3. limit exhausted?
        limit = grant.get("limit")
        if limit is not None and used >= int(limit):
            return deny(f"call limit {limit} exhausted")

        self.limits[key] = used + 1
        form = grant.get("form", "full")
        scratch = None
        try:
            if form == "scratch":
                roots = [t.get("root") for t in self.pkg.tools.values() if t.get("root")]
                scratch = make_scratch(self.pkg.root, roots)
            result = run_tool(tname, tdef, args, self.pkg.root, scratch_dir=scratch)
            shaped = shape_result(form, result, self.filters, grant.get("filter"))
            self.log.event("tool_called", step=ref, tool=tname, args=args,
                           form=form)
            return shaped
        except Denied as d:
            return deny(str(d))
        finally:
            if scratch is not None:
                import shutil
                shutil.rmtree(scratch, ignore_errors=True)

    def _do_repeat(self, r, ctx: Ctx, held):
        maxn = int(r["max"])  # validator guarantees presence
        for _ in range(maxn):
            self._walk(r.get("steps") or [], ctx, held)
            if ctx.stopped:
                return
            until = r.get("until")
            if until and conditions.evaluate(until, ctx.outcomes, ctx.lists, ctx.stored):
                return
        if r.get("until"):
            mode = r.get("on_exhausted", "stop")
            self.log.event("repeat_exhausted", on_exhausted=mode)
            if mode == "stop":
                ctx.stopped = True
            elif mode == "escalate":
                ctx.escalated = True
                ctx.stopped = True

    def _do_for_each(self, fe, ctx: Ctx, held):
        lst = list(ctx.lists.get(fe.get("list"), []))
        var = fe.get("as", "item")
        for val in lst:
            ctx.stored[var] = val
            self._walk(fe.get("steps") or [], ctx, held)
            if ctx.stopped:
                return

    def _do_collect(self, item, ctx: Ctx, held):
        name = item["collect"]
        m = re.match(r"tool\(([A-Za-z0-9_-]+)\)", str(item.get("from", "")))
        tname = m.group(1)
        result = run_tool(tname, self.pkg.tools[tname], {}, self.pkg.root)
        ctx.lists[name] = result if isinstance(result, list) else [result]
        self.log.event("collected", list=name, count=len(ctx.lists[name]))

    def _do_call(self, item, ctx: Ctx, held):
        target = item["call"]
        role = item.get("as", "default")
        requested = item.get("grants")
        if requested is not None:
            parent_held = {g.get("tool") for g in grant_entries(self.pkg, role)}
            if held is not None:
                parent_held &= set(held)
            # the only operation is a filter on the parent's own list
            child_held = [t for t in parent_held if t in requested]
        else:
            child_held = held
        self.run(self.pkg.root / "flows" / f"{target}.yaml", child_held, ctx)

    def _do_ask(self, item, ctx: Ctx):
        options = item.get("options") or []
        choice = self.human(item["ask"], options)
        if choice not in options:
            raise HeddleError(f"human chose {choice!r}, not in {options}")
        ctx.stored[item.get("store_as", "human_decision")] = choice
        self.log.event("human_gate", question=item["ask"], choice=choice)
