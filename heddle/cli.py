"""heddle cli — check / show / run (§7)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

from .errors import HeddleError
from .interpreter import Interpreter, visible_tools
from .loader import load_flow, load_package
from .runlog import RunLog
from .validate import validate_package


class CannedModel:
    """Deterministic model for CLI runs: outcomes and tool calls come from a
    YAML script keyed by step ref. Real runs wire in a real model callable."""

    def __init__(self, script: dict):
        self.script = script or {}

    def __call__(self, prompt, tools, ref):
        entry = dict(self.script.get(ref) or {})
        calls = entry.get("tool_calls") or []
        # drop calls to tools that aren't visible — the interpreter would deny
        # them, but a scripted model should behave like one that can't see them
        calls = [c for c in calls if c.get("tool") in tools]
        return {"outcome": entry.get("outcome"),
                "tool_calls": calls}


def _stdin_human(question, options):
    print(f"\nHUMAN GATE: {question}")
    for i, o in enumerate(options, 1):
        print(f"  {i}. {o}")
    while True:
        try:
            pick = input("choose: ").strip()
        except EOFError:
            return options[0]
        if pick in options:
            return pick
        if pick.isdigit() and 1 <= int(pick) <= len(options):
            return options[int(pick) - 1]
        print(f"one of: {options}")


def _flow_path(args) -> Path:
    f = Path(args.flow)
    return f if f.is_absolute() or f.is_file() else Path(args.root) / f


def cmd_check(args) -> int:
    pkg = load_package(Path(args.root))
    probs = validate_package(pkg, _flow_path(args))
    if not probs:
        print("no problems.")
        return 0
    for p in probs:
        print(p)
        print()
    print(f"{len(probs)} problem(s).")
    return 1


def cmd_show(args) -> int:
    pkg = load_package(Path(args.root))
    name, items = load_flow(_flow_path(args))

    def walk(items, indent=0, held=None):
        for item in items:
            item = {k: v for k, v in (item or {}).items() if k != "__line__"}
            pad = "  " * indent
            if "step" in item:
                ref = item["step"]
                sname, stname = ref.split(".", 1)
                role = item.get("as", "default")
                skill = pkg.skills.get(sname)
                if skill is None or stname not in skill.steps:
                    print(f"{pad}{ref}  (role: {role})  [unresolved]")
                    continue
                vis = visible_tools(pkg, role, stname, skill.steps[stname].tools, held)
                print(f"{pad}{ref}  (role: {role})")
                for t in vis:
                    print(f"{pad}    - {t}")
                if not vis:
                    print(f"{pad}    (no tools visible)")
            elif "when" in item:
                print(f"{pad}when {item['when']}")
                walk(item.get("then") or [], indent + 1, held)
                if item.get("else"):
                    print(f"{pad}else")
                    walk(item["else"], indent + 1, held)
            elif "repeat" in item:
                r = item["repeat"]
                print(f"{pad}repeat max={r.get('max')} until={r.get('until')}")
                walk(r.get("steps") or [], indent + 1, held)
            elif "for_each" in item:
                fe = item["for_each"]
                print(f"{pad}for_each {fe.get('list')} as {fe.get('as', 'item')}")
                walk(fe.get("steps") or [], indent + 1, held)
            elif "collect" in item:
                print(f"{pad}collect {item['collect']} from {item.get('from')}")
            elif "call" in item:
                print(f"{pad}call {item['call']} (role: {item.get('as')}, "
                      f"grants: {item.get('grants')})")
            elif "ask" in item:
                print(f"{pad}ask: {item['ask']}  {item.get('options')}")

    print(f"flow: {name}")
    walk(items)
    return 0


def cmd_run(args) -> int:
    pkg = load_package(Path(args.root))
    probs = validate_package(pkg, _flow_path(args))
    if probs:
        print("package won't run; fix these first:\n", file=sys.stderr)
        for p in probs:
            print(p, file=sys.stderr)
        return 1
    script = {}
    if args.script:
        script = yaml.safe_load((Path(args.root) / args.script).read_text()) or {}
    model = CannedModel(script)
    log = RunLog(Path(args.log) if args.log else Path(args.root) / "heddle-run.jsonl")
    interp = Interpreter(pkg, model, human=_stdin_human, log=log)
    ctx = interp.run(_flow_path(args))
    log.close()
    print(json.dumps({"stopped": ctx.stopped, "escalated": ctx.escalated,
                      "outcomes": ctx.outcomes, "log": str(log.path)}, indent=2))
    return 2 if ctx.stopped else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="heddle")
    ap.add_argument("--root", default=".", help="package root (skills/, flows/, tools.yaml, grants.yaml)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for c in ("check", "show", "run"):
        p = sub.add_parser(c)
        p.add_argument("flow")
        if c == "run":
            p.add_argument("--script", help="YAML file of canned model replies")
            p.add_argument("--log", help="JSONL log path")
    args = ap.parse_args(argv)
    try:
        return {"check": cmd_check, "show": cmd_show, "run": cmd_run}[args.cmd](args)
    except HeddleError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
