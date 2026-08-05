"""heddle.loader — load the four file types.

Skills are Markdown with YAML front matter and level-2 headings as steps.
Flows, tools, and grants are YAML. YAML node marks are used to attach line
numbers to flow items and grant entries so the validator can name them.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .errors import HeddleError


# ---------------------------------------------------------------- skills

@dataclass
class SkillStep:
    name: str
    tools: list[str]
    outcomes: list[str]
    prose: str
    line: int  # line of the '## heading'


@dataclass
class Skill:
    name: str
    version: int
    steps: dict[str, SkillStep]
    path: Path


_FRONT_RE = re.compile(r"^---\s*$")
_HEADING_RE = re.compile(r"^##\s+([A-Za-z0-9_-]+)\s*$")


def load_skill(path: Path) -> Skill:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or not _FRONT_RE.match(lines[0]):
        raise HeddleError(f"{path}: skill must start with a '---' front-matter block")
    try:
        end = next(i for i in range(1, len(lines)) if _FRONT_RE.match(lines[i]))
    except StopIteration:
        raise HeddleError(f"{path}: front matter is not closed with a second '---'")
    meta = yaml.safe_load("\n".join(lines[1:end])) or {}
    if not isinstance(meta, dict) or "name" not in meta or "steps" not in meta:
        raise HeddleError(f"{path}: front matter needs 'name' and 'steps'")

    headings: dict[str, tuple[int, str]] = {}
    cur, cur_line, buf = None, None, []
    for i, line in enumerate(lines[end + 1 :], start=end + 2):
        m = _HEADING_RE.match(line)
        if m:
            if cur is not None:
                headings[cur] = (cur_line, "\n".join(buf).strip())
            cur, cur_line, buf = m.group(1), i, []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        headings[cur] = (cur_line, "\n".join(buf).strip())

    steps: dict[str, SkillStep] = {}
    declared = meta.get("steps") or {}
    for name, spec in declared.items():
        spec = spec or {}
        hline, prose = headings.get(name, (None, ""))
        steps[name] = SkillStep(
            name=name,
            tools=list(spec.get("tools") or []),
            outcomes=list(spec.get("outcomes") or []),
            prose=prose,
            line=hline,
        )
    # headings with no front-matter entry still get recorded for the validator
    for name, (hline, prose) in headings.items():
        if name not in steps:
            steps[name] = SkillStep(name, [], [], prose, hline)
    return Skill(name=str(meta["name"]), version=int(meta.get("version", 1)),
                 steps=steps, path=path)


def load_skills(root: Path) -> dict[str, Skill]:
    skills = {}
    d = root / "skills"
    if d.is_dir():
        for p in sorted(d.glob("*.md")):
            s = load_skill(p)
            skills[s.name] = s
    return skills


# ---------------------------------------------------------------- yaml with line numbers

class _MarkLoader(yaml.SafeLoader):
    pass


def _construct_mapping(loader, node, deep=False):
    mapping = yaml.SafeLoader.construct_mapping(loader, node, deep=deep)
    mapping["__line__"] = node.start_mark.line + 1
    return mapping


_MarkLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)


def load_yaml_marked(path: Path):
    """Load YAML; every mapping gains a __line__ key (1-based)."""
    data = yaml.load(path.read_text(encoding="utf-8"), Loader=_MarkLoader)
    return data


def strip_marks(obj):
    """Remove __line__ keys recursively. Callers needing lines read them first."""
    if isinstance(obj, dict):
        return {k: strip_marks(v) for k, v in obj.items() if k != "__line__"}
    if isinstance(obj, list):
        return [strip_marks(v) for v in obj]
    return obj


# ---------------------------------------------------------------- package

@dataclass
class Package:
    root: Path
    skills: dict[str, Skill]
    tools: dict                 # raw tools.yaml mapping
    grants: dict                # raw grants.yaml mapping (roles -> entries with __line__)
    flow_dirs: Path = field(default=None)


def load_package(root: Path) -> Package:
    root = Path(root)
    tools_path, grants_path = root / "tools.yaml", root / "grants.yaml"
    if not tools_path.is_file():
        raise HeddleError(f"{tools_path}: missing")
    if not grants_path.is_file():
        raise HeddleError(f"{grants_path}: missing")
    tools = strip_marks(load_yaml_marked(tools_path)) or {}
    grants_raw = load_yaml_marked(grants_path) or {}
    skills = load_skills(root)
    return Package(root=root, skills=skills, tools=tools,
                   grants={k: v for k, v in (grants_raw.get("roles", {}) or {}).items()
                           if isinstance(v, list)},
                   flow_dirs=root / "flows")


def load_flow(path: Path):
    """Return (flow_name, items_with_lines). Each item keeps its __line__."""
    data = load_yaml_marked(Path(path)) or {}
    name = data.get("flow")
    items = data.get("steps") or []
    return name, items
