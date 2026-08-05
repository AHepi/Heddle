"""The packages/ wheel: every distributable package stays loadable,
validates clean, and is non-vacuous.

packages/<name>/ are self-contained Heddle packages for other repos to
adopt (see packages/README.md). Nothing in the root package reaches
them, so without these probes they would rot silently — an instrument
nothing mentions rots (DISCIPLINE.md §6). The PACKAGES pin moves in the
same commit as any package add/remove/rename (AGENTS.md §3).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from heddle.loader import load_flow, load_package
from heddle.validate import validate_package

PKG_ROOT = Path(__file__).resolve().parents[1] / "packages"

# The pin: one entry per distributable package, mapping to its flows.
PACKAGES = {
    "triage": ["triage.yaml"],
    "publish": ["publish.yaml"],
    "postmortem": ["postmortem.yaml"],
    "style": ["style.yaml"],
}


def test_packages_inventory_is_pinned():
    on_disk = {p.name for p in PKG_ROOT.iterdir() if p.is_dir()}
    assert on_disk == set(PACKAGES), (
        "packages/ and the PACKAGES pin disagree — move the pin in the "
        "same commit as the package (AGENTS.md §3)")


@pytest.mark.parametrize("name", sorted(PACKAGES))
def test_package_validates_clean(name):
    pkg = load_package(PKG_ROOT / name)
    for fname in PACKAGES[name]:
        probs = validate_package(pkg, pkg.root / "flows" / fname)
        assert probs == [], [str(p) for p in probs]


@pytest.mark.parametrize("name", sorted(PACKAGES))
def test_package_flows_are_not_vacuous(name):
    # Guards TRAP-flow-vacuous-keys for the distributables too.
    for fname in PACKAGES[name]:
        flow_name, items = load_flow(PKG_ROOT / name / "flows" / fname)
        assert flow_name, f"{name}/{fname}: no 'flow:' key"
        assert items, f"{name}/{fname}: no 'steps:' items"


@pytest.mark.parametrize("name", sorted(PACKAGES))
def test_package_steps_have_declared_roles(name):
    pkg = load_package(PKG_ROOT / name)

    def walk(items, fname):
        for item in items:
            item = {k: v for k, v in (item or {}).items() if k != "__line__"}
            if "step" in item:
                assert item.get("as") in pkg.grants, (
                    f"{name}/{fname}: step {item['step']} has role "
                    f"{item.get('as')!r}, not in {sorted(pkg.grants)}")
            elif "when" in item:
                walk(item.get("then") or [], fname)
                walk(item.get("else") or [], fname)
            elif "repeat" in item:
                walk((item["repeat"] or {}).get("steps") or [], fname)
            elif "for_each" in item:
                walk((item["for_each"] or {}).get("steps") or [], fname)

    for fname in PACKAGES[name]:
        _, items = load_flow(pkg.root / "flows" / fname)
        walk(items, fname)
