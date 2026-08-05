"""heddle.validate — §8: report every problem, with file, line, and fix."""

from __future__ import annotations

import os
import re
from pathlib import Path

from .errors import Problem
from .loader import Package, load_flow, strip_marks

ROOT_OK = re.compile(r"^[A-Za-z0-9_./-]+$")
DOMAINS = {"one_of", "one_of_files_in", "pattern", "int_range", "text"}
TOOL_KINDS = {"read_file", "write_file", "read_json", "command", "http"}
FORMS = {"full", "summary", "write_only", "scratch"}


def _close(name: str, choices) -> str | None:
    import difflib
    m = difflib.get_close_matches(name, list(choices), n=1)
    return m[0] if m else None


def validate_package(pkg: Package, flow_path: Path) -> list[Problem]:
    """Validate one flow against the package. Returns all problems found."""
    probs: list[Problem] = []
    flow_file = str(flow_path)
    tools, grants, skills = pkg.tools, pkg.grants, pkg.skills

    # ---- tools.yaml --------------------------------------------------
    for tname, tdef in tools.items():
        tdef = tdef or {}
        kind = tdef.get("kind")
        tline = _find_line(Path(pkg.root) / "tools.yaml", tname)
        if kind not in TOOL_KINDS:
            probs.append(Problem("tools.yaml", tline,
                f"tool '{tname}' has kind '{kind}', not one of {sorted(TOOL_KINDS)}."))
        if kind in ("read_file", "write_file"):
            root = tdef.get("root")
            if not root:
                probs.append(Problem("tools.yaml", tline,
                    f"tool '{tname}' has no root.", "Declare a specific directory."))
            else:
                r = (pkg.root / root).resolve()
                if str(root).strip() in ("/", ".", "") or r == pkg.root.resolve() \
                        or r == Path(__file__).resolve().parent:
                    probs.append(Problem("tools.yaml", tline,
                        f"tool '{tname}' has root '{root}', which is not permitted.",
                        "Declare a specific directory."))
                elif not r.is_dir():
                    probs.append(Problem("tools.yaml", tline,
                        f"tool '{tname}' root '{root}' is not a real directory."))
        for pname, dom in (tdef.get("params") or {}).items():
            if not isinstance(dom, dict) or len(dom) != 1:
                probs.append(Problem("tools.yaml", tline,
                    f"tool '{tname}' param '{pname}' must be a single domain."))
                continue
            dkind = next(iter(dom))
            if dkind not in DOMAINS:
                probs.append(Problem("tools.yaml", tline,
                    f"tool '{tname}' param '{pname}' uses unknown domain '{dkind}'.",
                    f"Use one of {sorted(DOMAINS)}."))
            if dkind == "text" and kind in ("read_file", "read_json", "http"):
                probs.append(Problem("tools.yaml", tline,
                    f"tool '{tname}' param '{pname}' is free text on a read target. "
                    "A target is never free text."))

    # ---- grants.yaml -------------------------------------------------
    for role, entries in grants.items():
        for e in entries or []:
            line = e.get("__line__") if isinstance(e, dict) else None
            e = strip_marks(e) if isinstance(e, dict) else {}
            t = e.get("tool")
            if t not in tools:
                fix = None
                close = _close(str(t), tools)
                if close:
                    fix = f"Did you mean '{close}'? (tools.yaml)"
                probs.append(Problem("grants.yaml", line,
                    f"{role} is granted '{t}', which no tool declares.", fix))
            form = e.get("form", "full")
            if form not in FORMS:
                probs.append(Problem("grants.yaml", line,
                    f"{role}/{t}: unknown form '{form}'.",
                    f"Use one of {sorted(FORMS)}."))
            when = e.get("when", "always")
            if when != "always":
                for sname in when or []:
                    found = any(sname in s.steps for s in skills.values())
                    if not found:
                        probs.append(Problem("grants.yaml", line,
                            f"{role}/{t}: 'when' names step '{sname}', which no "
                            "loaded skill declares."))

    # ---- skills ------------------------------------------------------
    for s in skills.values():
        rel = os.path.relpath(s.path, pkg.root)
        for name, st in s.steps.items():
            if st.line is None:
                probs.append(Problem(rel, None,
                    f"front matter declares step '{name}' with no '## {name}' "
                    "heading in the file."))

    # ---- flow --------------------------------------------------------
    try:
        flow_name, items = load_flow(flow_path)
    except Exception as exc:
        probs.append(Problem(flow_file, None, f"flow does not parse: {exc}"))
        return probs

    _validate_items(pkg, probs, flow_file, items, skills, tools, grants,
                    seen_collects=[], call_stack=[flow_name])
    return probs


def _step_ref(pkg, probs, flow_file, item, skills, grants):
    line = item.get("__line__")
    ref = item.get("step")
    role = item.get("as")
    if role and role not in grants:
        probs.append(Problem(flow_file, line,
            f"step uses role '{role}', which grants.yaml doesn't declare."))
    if not ref or "." not in str(ref):
        probs.append(Problem(flow_file, line,
            f"step reference '{ref}' must be of the form skill.step."))
        return
    sname, stname = str(ref).split(".", 1)
    if sname not in skills:
        probs.append(Problem(flow_file, line, f"no skill named '{sname}'."))
        return
    skill = skills[sname]
    if stname not in skill.steps or skill.steps[stname].line is None:
        probs.append(Problem(flow_file, line,
            f"skill '{sname}' has no step heading '## {stname}'."))
        return
    st = skill.steps[stname]
    if not st.tools:
        return  # tools: [] declared; nothing to check grants against
    for t in st.tools:
        if t not in pkg.tools:
            probs.append(Problem(flow_file, line,
                f"step '{ref}' lists tool '{t}', which no tool declares."))
            continue
        if role and role in pkg.grants:
            usable = any(
                strip_marks(g).get("tool") == t and
                (strip_marks(g).get("when", "always") == "always"
                 or stname in (strip_marks(g).get("when") or []))
                for g in pkg.grants[role] or [])
            if not usable:
                probs.append(Problem(
                    os.path.relpath(skill.path, pkg.root), st.line,
                    f"step '{stname}' lists tool '{t}', but role '{role}' has "
                    f"no grant for it at that step.",
                    f"Add it to grants.yaml under {role} with: when: [{stname}]"))


def _check_condition(probs, flow_file, line, cond, skills):
    if not cond:
        return
    for ref, val in re.findall(r"outcome\(([A-Za-z0-9_.-]+)\)\s*[=!<>]+\s*([A-Za-z0-9_-]+)", str(cond)):
        if "." in ref:
            sname, stname = ref.split(".", 1)
            if sname in skills and stname in skills[sname].steps:
                outs = skills[sname].steps[stname].outcomes
                if outs and val not in outs:
                    probs.append(Problem(flow_file, line,
                        f"'when' compares outcome({ref}) to '{val}', which isn't "
                        f"in that step's outcomes {outs}."))


def _validate_items(pkg, probs, flow_file, items, skills, tools, grants,
                    seen_collects, call_stack):
    for item in items:
        if not isinstance(item, dict):
            probs.append(Problem(flow_file, None, f"flow item is not a mapping: {item!r}"))
            continue
        line = item.get("__line__")
        if "step" in item:
            _step_ref(pkg, probs, flow_file, item, skills, grants)
        elif "when" in item:
            _check_condition(probs, flow_file, line, item.get("when"), skills)
            for branch in ("then", "else"):
                if branch in item:
                    _validate_items(pkg, probs, flow_file, item[branch] or [],
                                    skills, tools, grants, seen_collects, call_stack)
        elif "repeat" in item:
            r = item["repeat"] or {}
            if "max" not in r:
                probs.append(Problem(flow_file, line,
                    "repeat has no 'max'. Every loop needs a bound."))
            if r.get("on_exhausted", "stop") not in ("stop", "continue", "escalate"):
                probs.append(Problem(flow_file, line,
                    "on_exhausted must be stop | continue | escalate."))
            _check_condition(probs, flow_file, line, r.get("until"), skills)
            _validate_items(pkg, probs, flow_file, r.get("steps") or [],
                            skills, tools, grants, seen_collects, call_stack)
        elif "for_each" in item:
            fe = item["for_each"] or {}
            lst = fe.get("list")
            if lst not in seen_collects:
                probs.append(Problem(flow_file, line,
                    f"for_each list '{lst}' is not produced by a 'collect' "
                    "earlier in the flow."))
            _validate_items(pkg, probs, flow_file, fe.get("steps") or [],
                            skills, tools, grants, seen_collects, call_stack)
        elif "collect" in item:
            seen_collects.append(item["collect"])
            src = item.get("from", "")
            m = re.match(r"tool\(([A-Za-z0-9_-]+)\)", str(src))
            if not m or m.group(1) not in tools:
                probs.append(Problem(flow_file, line,
                    f"collect source '{src}' doesn't name a declared tool."))
        elif "call" in item:
            target = item.get("call")
            flows_dir = pkg.root / "flows"
            tpath = flows_dir / f"{target}.yaml"
            if target in call_stack:
                cycle = " → ".join(str(c) for c in call_stack + [target])
                probs.append(Problem(flow_file, line,
                    f"call to flow {cycle} is a cycle."))
                continue
            if not tpath.is_file():
                probs.append(Problem(flow_file, line,
                    f"call to flow '{target}' doesn't resolve "
                    f"(flows/{target}.yaml missing)."))
                continue
            role = item.get("as")
            held = set()
            if role and role in grants:
                held = {strip_marks(g).get("tool") for g in grants[role] or []}
            for req in item.get("grants") or []:
                if req not in held:
                    probs.append(Problem(flow_file, line,
                        f"call to '{target}' requests grant '{req}', which the "
                        f"calling role '{role}' doesn't hold. Grants can only narrow."))
            try:
                tname, titems = load_flow(tpath)
            except Exception as exc:
                probs.append(Problem(flow_file, line,
                    f"called flow '{target}' does not parse: {exc}"))
                continue
            _validate_items(pkg, probs, str(tpath), titems, skills, tools, grants,
                            list(seen_collects), call_stack + [target])
        elif "ask" in item:
            if not item.get("options"):
                probs.append(Problem(flow_file, line,
                    "ask needs an 'options' list."))
        else:
            probs.append(Problem(flow_file, line,
                f"unknown flow item: {sorted(k for k in item if k != '__line__')}."))


def _find_line(path: Path, key: str) -> int | None:
    try:
        for i, line in enumerate(path.read_text().splitlines(), start=1):
            if re.match(rf"^{re.escape(str(key))}:\s*$", line):
                return i
    except OSError:
        pass
    return None
