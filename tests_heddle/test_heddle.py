import json
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from heddle.loader import load_package
from heddle.validate import validate_package
from heddle.interpreter import Interpreter, visible_tools
from heddle.runlog import RunLog
from heddle.conditions import evaluate
from heddle.errors import HeddleError

EX = Path(__file__).resolve().parents[1] / "examples" / "heddle"


@pytest.fixture()
def pkg(tmp_path):
    dst = tmp_path / "pkg"
    shutil.copytree(EX, dst)
    return load_package(dst)


# ---- loader ---------------------------------------------------------

def test_skill_loads_steps_and_prose(pkg):
    s = pkg.skills["review"]
    assert set(s.steps) == {"derive", "check", "write_finding"}
    assert "authority requires" in s.steps["derive"].prose
    assert s.steps["check"].outcomes == ["ok", "problems_found"]


# ---- conditions ------------------------------------------------------

def test_conditions():
    outs, lists, stored = {"review.check": "ok"}, {"f": [1, 2]}, {"d": "accept"}
    assert evaluate("outcome(review.check) == ok", outs, lists, stored)
    assert evaluate("count(f) == 2", outs, lists, stored)
    assert evaluate("count(f) > 5", outs, lists, stored) is False
    assert evaluate("stored(d) == accept", outs, lists, stored)
    assert evaluate("d != reject", outs, lists, stored)


# ---- validation -------------------------------------------------------

def test_example_package_is_clean(pkg):
    probs = validate_package(pkg, pkg.root / "flows" / "lifecycle.yaml")
    assert probs == [], [str(p) for p in probs]


def test_validator_reports_all_problems(pkg):
    (pkg.root / "flows" / "bad.yaml").write_text("""flow: bad
steps:
  - step: review.check
    as: ghost
  - step: review.nonexistent
    as: reviewer
  - step: noskill.x
    as: reviewer
  - repeat:
      steps:
        - step: review.derive
          as: reviewer
  - for_each:
      list: missing
      steps: []
  - when: outcome(review.check) == passed
    then: []
""")
    probs = validate_package(pkg, pkg.root / "flows" / "bad.yaml")
    text = "\n".join(str(p) for p in probs)
    assert "ghost" in text                       # unknown role
    assert "nonexistent" in text                 # missing heading
    assert "noskill" in text                     # missing skill
    assert "no 'max'" in text                    # unbounded loop
    assert "missing" in text                     # for_each without collect
    assert "passed" in text                      # undeclared outcome
    assert len(probs) >= 6                       # all problems, not the first


def test_cycle_detection(pkg):
    (pkg.root / "flows" / "a.yaml").write_text(
        "flow: a\nsteps:\n  - call: b\n    as: reviewer\n")
    (pkg.root / "flows" / "b.yaml").write_text(
        "flow: b\nsteps:\n  - call: a\n    as: reviewer\n")
    probs = validate_package(pkg, pkg.root / "flows" / "a.yaml")
    assert any("cycle" in str(p) for p in probs)


def test_grant_widening_rejected(pkg):
    (pkg.root / "flows" / "pub.yaml").write_text("flow: pub\nsteps: []\n")
    (pkg.root / "flows" / "widen.yaml").write_text(
        "flow: widen\nsteps:\n  - call: pub\n    as: reviewer\n"
        "    grants: [write_code]\n")
    probs = validate_package(pkg, pkg.root / "flows" / "widen.yaml")
    assert any("only narrow" in str(p) for p in probs)


def test_bad_root_rejected(pkg):
    (pkg.root / "tools.yaml").write_text(
        (pkg.root / "tools.yaml").read_text() +
        "read_anything:\n  kind: read_file\n  root: /\n  params:\n"
        "    p: {one_of_files_in: /}\n")
    pkg2 = load_package(pkg.root)
    probs = validate_package(pkg2, pkg.root / "flows" / "lifecycle.yaml")
    assert any("not permitted" in str(p) for p in probs)


def test_undeclared_tool_in_grants_named(pkg):
    (pkg.root / "grants.yaml").write_text(
        (pkg.root / "grants.yaml").read_text() +
        "    - tool: writ_code\n      form: full\n      when: always\n")
    pkg2 = load_package(pkg.root)
    probs = validate_package(pkg2, pkg.root / "flows" / "lifecycle.yaml")
    assert any("writ_code" in str(p) and "no tool declares" in str(p)
               for p in probs)


# ---- visibility -------------------------------------------------------

def test_visibility_is_step_scoped(pkg):
    assert visible_tools(pkg, "reviewer", "derive",
                         pkg.skills["review"].steps["derive"].tools) == ["read_authority"]
    assert visible_tools(pkg, "reviewer", "check",
                         pkg.skills["review"].steps["check"].tools) == \
        ["read_authority", "read_code", "run_tests"]
    # implementer never sees read_authority; write_code only during fix
    assert visible_tools(pkg, "implementer", "check",
                         pkg.skills["review"].steps["check"].tools) == ["read_code"]


# ---- interpreter ------------------------------------------------------

def make_model(replies):
    def model(prompt, tools, ref):
        return replies.get(ref, {"outcome": "done"})
    return model


def test_run_walks_flow_and_enforces_forms(pkg):
    log = RunLog(pkg.root / "run.jsonl")
    replies = {
        "review.derive": {"outcome": "done",
                          "tool_calls": [{"tool": "read_authority",
                                          "args": {"doc": "standard.md"}}]},
        "review.check": {"outcome": "ok",
                         "tool_calls": [
                             {"tool": "read_code", "args": {"path": "widget.py"}},
                             {"tool": "write_report",   # not visible here: denied
                              "args": {"name": "x.md", "body": "b"}}]},
        "review.write_finding": {"outcome": "done",
                                 "tool_calls": [{"tool": "write_report",
                                                 "args": {"name": "f.md", "body": "hi"}}]},
    }
    interp = Interpreter(pkg, make_model(replies), human=lambda q, o: "accept", log=log)
    ctx = interp.run(pkg.root / "flows" / "lifecycle.yaml")
    log.close()
    assert ctx.outcomes["review.check"] == "ok"
    assert ctx.lists["open_findings"] == ["finding-1", "finding-2"]
    assert ctx.stored["human_decision"] == "accept"
    # write_only wrote the file but the model saw a receipt
    assert (pkg.root / "reports" / "f.md").read_text() == "hi"
    events = [json.loads(l) for l in (pkg.root / "run.jsonl").read_text().splitlines()]
    kinds = [e["event"] for e in events]
    assert "step_started" in kinds and "tool_called" in kinds
    assert "outcome_recorded" in kinds and "flow_ended" in kinds
    # write_report is not visible during check -> denial logged
    assert any(e["event"] == "tool_denied" and e.get("tool") == "write_report"
               and e["step"] == "review.check" for e in events)


def test_domain_violation_denied(pkg):
    log = RunLog(pkg.root / "run.jsonl")
    replies = {
        "review.derive": {"outcome": "done",
                          "tool_calls": [{"tool": "read_authority",
                                          "args": {"doc": "../grants.yaml"}}]},
        "review.check": {"outcome": "ok"},
        "review.write_finding": {"outcome": "done"},
    }
    interp = Interpreter(pkg, make_model(replies), human=lambda q, o: "accept", log=log)
    interp.run(pkg.root / "flows" / "lifecycle.yaml")
    log.close()
    events = [json.loads(l) for l in (pkg.root / "run.jsonl").read_text().splitlines()]
    assert any(e["event"] == "tool_denied" and "domain" in e["reason"]
               for e in events)


def test_bad_outcome_rejected(pkg):
    log = RunLog(pkg.root / "run.jsonl")
    interp = Interpreter(pkg, make_model({"review.derive": {"outcome": "maybe"}}), log=log)
    with pytest.raises(HeddleError):
        interp.run(pkg.root / "flows" / "lifecycle.yaml")
    log.close()


def test_repeat_until_and_exhaustion(pkg):
    log = RunLog(pkg.root / "run.jsonl")
    replies = {"review.derive": {"outcome": "done"},
               "review.check": {"outcome": "problems_found"},
               "implement.fix": {"outcome": "done"},
               "review.write_finding": {"outcome": "done"}}
    interp = Interpreter(pkg, make_model(replies), human=lambda q, o: "reject", log=log)
    ctx = interp.run(pkg.root / "flows" / "lifecycle.yaml")
    log.close()
    assert ctx.escalated and ctx.stopped  # 3 tries, never ok -> escalate


def test_call_narrows_grants(pkg):
    (pkg.root / "flows" / "child.yaml").write_text(
        "flow: child\nsteps:\n  - step: review.write_finding\n    as: reviewer\n")
    (pkg.root / "flows" / "parent.yaml").write_text(
        "flow: parent\nsteps:\n  - call: child\n    as: reviewer\n"
        "    grants: [read_authority]\n")   # write_report filtered out
    log = RunLog(pkg.root / "run.jsonl")
    replies = {"review.write_finding": {"outcome": "done",
               "tool_calls": [{"tool": "write_report",
                               "args": {"name": "f.md", "body": "x"}}]}}
    interp = Interpreter(pkg, make_model(replies), log=log)
    interp.run(pkg.root / "flows" / "parent.yaml")
    log.close()
    assert not (pkg.root / "reports" / "f.md").exists()
    events = [json.loads(l) for l in (pkg.root / "run.jsonl").read_text().splitlines()]
    assert any(e["event"] == "tool_denied" for e in events)


# ---- CLI --------------------------------------------------------------

def test_cli_check_and_show(pkg):
    from heddle.cli import main
    assert main(["--root", str(pkg.root), "check", "flows/lifecycle.yaml"]) == 0
    assert main(["--root", str(pkg.root), "show", "flows/lifecycle.yaml"]) == 0


def test_cli_run_with_script(pkg, monkeypatch):
    from heddle.cli import main
    (pkg.root / "script.yaml").write_text("""review.derive: {outcome: done}
review.check: {outcome: ok}
review.write_finding: {outcome: done}
""")
    monkeypatch.setattr("builtins.input", lambda *a: "accept")
    rc = main(["--root", str(pkg.root), "run", "flows/lifecycle.yaml",
               "--script", "script.yaml", "--log", str(pkg.root / "cli.jsonl")])
    assert rc == 0


# ---- forms ------------------------------------------------------------

def test_scratch_tolerates_shared_roots(tmp_path):
    # TRAP-scratch-shared-roots: read_map, write_map, and capture all root
    # at map/; collecting every tool root naively copies map/ twice and
    # crashes before the tool ever runs.
    from heddle.tools import make_scratch
    (tmp_path / "map").mkdir()
    (tmp_path / "map" / "x.md").write_text("x")
    scratch = make_scratch(tmp_path, ["map/", "map/", "reports/"])
    assert (scratch / "map" / "x.md").read_text() == "x"
