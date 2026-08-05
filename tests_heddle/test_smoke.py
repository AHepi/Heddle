"""The smoke wheel (tool: run_wheel).

One fast spin that proves the harness itself turns before any ring or gate
is worth running: the root package loads, its flows parse to something
non-vacuous, and every flow validates clean. Seconds, not minutes.

The root package's tools legitimately target heddle/ — the runtime's own
source — which the validator rejects when heddle runs from this repo (see
TRAP-self-host-runtime-dir). The fixture copies the package to a neutral
directory first, the same effect as the documented installed-heddle
workaround, so validation exercises everything except that guard.
"""

import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from heddle.errors import HeddleError
from heddle.loader import load_flow, load_package, load_skills
from heddle.validate import validate_package

REPO = Path(__file__).resolve().parents[1]
FLOWS = ["start.yaml", "defect.yaml", "change.yaml", "skill-update.yaml"]

# One skill per step, grouped by workflow folder; skill name == step name.
SKILLS = {
    "shared": {"navigate", "record"},
    "defect": {"goal", "diagnose", "reproduce", "propose", "implement",
               "verify"},
    "change": {"specify", "plan", "execute_step", "validate",
               "deliver"},
    "skill-update": {"survey", "redraft", "confirm"},
}


@pytest.fixture()
def root_pkg(tmp_path):
    dst = tmp_path / "pkg"
    dst.mkdir()
    for d in ("skills", "flows", "map", "heddle", "tests_heddle"):
        shutil.copytree(REPO / d, dst / d,
                        ignore=shutil.ignore_patterns("__pycache__"))
    for f in ("tools.yaml", "grants.yaml", "HEDDLE_0_1.md"):
        shutil.copy(REPO / f, dst / f)
    return load_package(dst)


def test_root_flows_are_not_vacuous():
    # Guards TRAP-flow-vacuous-keys: a flow file with the wrong top-level
    # keys loads as (None, []) and then "validates clean" because there is
    # nothing to check.
    for fname in FLOWS:
        name, items = load_flow(REPO / "flows" / fname)
        assert name, f"{fname}: no 'flow:' key — loader sees an unnamed flow"
        assert items, f"{fname}: no 'steps:' items — validation would be vacuous"


def test_root_flows_validate_clean(root_pkg):
    for fname in FLOWS:
        probs = validate_package(root_pkg, root_pkg.root / "flows" / fname)
        assert probs == [], [str(p) for p in probs]


def test_every_root_step_assigns_a_declared_role(root_pkg):
    # A step without 'as:' runs as role "default", which holds no grants —
    # every tool call would be denied. The validator doesn't flag this, so
    # the wheel does.
    def walk(items, fname):
        for item in items:
            item = {k: v for k, v in (item or {}).items() if k != "__line__"}
            if "step" in item:
                role = item.get("as")
                assert role in root_pkg.grants, (
                    f"{fname}: step {item['step']} has role {role!r}, "
                    f"not a declared role {sorted(root_pkg.grants)}")
            elif "when" in item:
                walk(item.get("then") or [], fname)
                walk(item.get("else") or [], fname)
            elif "repeat" in item:
                walk((item["repeat"] or {}).get("steps") or [], fname)
            elif "for_each" in item:
                walk((item["for_each"] or {}).get("steps") or [], fname)

    for fname in FLOWS:
        _, items = load_flow(root_pkg.root / "flows" / fname)
        walk(items, fname)


def test_skills_load_from_workflow_folders(root_pkg):
    expected = set().union(*SKILLS.values())
    assert set(root_pkg.skills) == expected
    for folder, names in SKILLS.items():
        for name in names:
            s = root_pkg.skills[name]
            assert s.path.parent.name == folder, (
                f"skill '{name}' is in {s.path.parent.name}/, "
                f"expected {folder}/")
            # one file, one step, named after the skill
            assert set(s.steps) == {name}


def test_duplicate_skill_names_are_an_error(tmp_path):
    d = tmp_path / "skills" / "a"
    d.mkdir(parents=True)
    (tmp_path / "skills" / "b").mkdir()
    text = "---\nname: twin\nsteps:\n  s:\n    tools: []\n---\n\n## s\nx\n"
    (d / "one.md").write_text(text)
    (tmp_path / "skills" / "b" / "two.md").write_text(text)
    with pytest.raises(HeddleError, match="already declared"):
        load_skills(tmp_path)
