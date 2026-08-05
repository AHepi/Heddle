"""Regression probes for the 2026-08-05 review-package incident.

Each test pins a defect that shipped despite a recorded "end to end"
scripted run — a canned model's replies ignore the prompt, so that run
proved control flow only and could not observe what a step's model
actually receives. These are the probes for that observable
(DISCIPLINE.md §6: every new observable needs a probe that reads it).
"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from heddle.interpreter import Interpreter
from heddle.loader import load_package
from heddle.tools import run_tool

EX = Path(__file__).resolve().parents[1] / "examples" / "heddle"


@pytest.fixture()
def pkg(tmp_path):
    import shutil
    dst = tmp_path / "pkg"
    shutil.copytree(EX, dst)
    return load_package(dst)


def _run_with_probe(pkg, flow_text, model):
    (pkg.root / "flows" / "probe.yaml").write_text(flow_text)
    interp = Interpreter(pkg, model)
    interp.run(pkg.root / "flows" / "probe.yaml")


def test_with_binding_delivers_the_stored_value(pkg):
    # Incident: review.yaml's `with: {finding: f}` handed write_finding
    # the literal string 'f' instead of the finding object, because the
    # interpreter resolved the parameter NAME in stored values rather
    # than the variable. Spec §3: `with: {finding: f}` binds f's value.
    (pkg.root / "reports" / "findings.json").write_text(
        json.dumps([{"expected": "X", "observed": "Y"}]))
    prompts = []

    def model(prompt, tools, ref):
        if ref == "review.write_finding":
            prompts.append(prompt)
        return {"outcome": "done" if ref != "review.check" else "ok"}

    _run_with_probe(pkg, """flow: probe
steps:
  - collect: open_findings
    from: tool(list_findings)
  - for_each:
      list: open_findings
      as: f
      steps:
        - step: review.write_finding
          as: reviewer
          with: {finding: f}
""", model)
    assert len(prompts) == 1
    assert "'expected': 'X'" in prompts[0], prompts[0]
    assert "'f'" not in prompts[0]


def test_with_binding_leaks_no_line_marker(pkg):
    # Recurrence of TRAP-marked-yaml-line-key-leak: the __line__ marker
    # injected into every YAML mapping reached the model's prompt via
    # the unstripped `with:` mapping.
    prompts = []

    def model(prompt, tools, ref):
        prompts.append(prompt)
        return {"outcome": "done"}

    _run_with_probe(pkg, """flow: probe
steps:
  - step: implement.fix
    as: implementer
    with: {note: hello}
""", model)
    assert "__line__" not in prompts[0], prompts[0]
    assert "note='hello'" in prompts[0]


def test_write_receipt_survives_relative_pkg_root(tmp_path, monkeypatch):
    # Incident: any write_file receipt crashed with ValueError when the
    # package root was a relative path (heddle --root . run ...), because
    # the receipt compared a resolved path against the unresolved root.
    monkeypatch.chdir(tmp_path)
    (tmp_path / "out").mkdir()
    tdef = {"kind": "write_file", "root": "out/",
            "params": {"name": {"pattern": r"[a-z]+\.md"}, "body": {"text": True}}}
    receipt = run_tool("w", tdef, {"name": "a.md", "body": "hi"}, Path("."))
    assert "a.md" in str(receipt)
