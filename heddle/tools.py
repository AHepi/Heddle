"""heddle.tools — §4: kinds, closed parameter domains, and §5 forms.

A target is never free text. Roots are declared in tools.yaml by a human,
never supplied by a model.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
import urllib.request
from pathlib import Path

from .errors import HeddleError


class Denied(HeddleError):
    """A call failed a check. Reported back, logged, counts against limit."""


# ------------------------------------------------------------- domains

def check_domain(domain: dict, value, pkg_root: Path) -> bool:
    kind, spec = next(iter(domain.items()))
    if kind == "one_of":
        return value in spec
    if kind == "int_range":
        try:
            v = int(value)
        except (TypeError, ValueError):
            return False
        lo, hi = spec
        return lo <= v <= hi
    if kind == "pattern":
        return isinstance(value, str) and re.fullmatch(spec, value) is not None
    if kind == "text":
        return isinstance(value, str)
    if kind == "one_of_files_in":
        d = (pkg_root / spec).resolve()
        try:
            candidate = (d / str(value)).resolve()
            candidate.relative_to(d)
        except (ValueError, OSError):
            return False
        return candidate.is_file()
    return False


def describe_domain(domain: dict) -> str:
    kind, spec = next(iter(domain.items()))
    return f"{kind}={spec}"


# ------------------------------------------------------------- kinds

def _under_root(pkg_root: Path, root: str, rel: str) -> Path:
    base = (pkg_root / root).resolve()
    p = (base / rel).resolve()
    try:
        p.relative_to(base)
    except ValueError:
        raise Denied(f"path escapes root '{root}'")
    return p


def run_tool(name: str, tdef: dict, args: dict, pkg_root: Path,
             scratch_dir: Path | None = None):
    """Execute a tool. scratch_dir replaces the root when form=scratch."""
    kind = tdef.get("kind")
    root = tdef.get("root")
    effective_root = pkg_root
    if scratch_dir is not None and root:
        effective_root = scratch_dir  # scratch mirrors pkg_root layout

    if kind == "read_file":
        param = next(iter(tdef.get("params") or {"path": None}))
        p = _under_root(effective_root, root, str(args[param]))
        if not p.is_file():
            raise Denied(f"no such file under '{root}': {args[param]}")
        return p.read_text(encoding="utf-8", errors="replace")

    if kind == "write_file":
        params = list(tdef.get("params") or {})
        name_param = params[0] if params else "name"
        p = _under_root(effective_root, root, str(args[name_param]))
        p.parent.mkdir(parents=True, exist_ok=True)
        body = args.get("body", "")
        p.write_text(str(body), encoding="utf-8")
        return f"wrote {p.relative_to(effective_root)}"

    if kind == "read_json":
        p = (effective_root / tdef["path"]).resolve()
        if not p.is_file():
            raise Denied(f"no such file: {tdef['path']}")
        return json.loads(p.read_text(encoding="utf-8"))

    if kind == "command":
        argv = [str(a).format(**{k: v for k, v in args.items()})
                for a in tdef["command"]]
        proc = subprocess.run(argv, cwd=str(effective_root), capture_output=True,
                              text=True, timeout=int(tdef.get("timeout", 120)))
        return {"exit": proc.returncode,
                "stdout": proc.stdout[-4000:], "stderr": proc.stderr[-4000:]}

    if kind == "http":
        url_t = tdef.get("url", "")
        url = str(url_t).format(**args) if args else url_t
        allowed = tdef.get("domains")
        if allowed and not any(urllib.request.urlparse(url).hostname == d
                               or urllib.request.urlparse(url).hostname.endswith("." + d)
                               for d in allowed):
            raise Denied(f"http target not in allowed domains {allowed}")
        with urllib.request.urlopen(url, timeout=30) as r:
            return r.read(65536).decode("utf-8", errors="replace")

    raise HeddleError(f"unknown tool kind: {kind}")


# ------------------------------------------------------------- forms

def make_scratch(pkg_root: Path, roots: list[str]) -> Path:
    """Copy the tool's declared roots into a temp dir; changes are discarded."""
    tmp = Path(tempfile.mkdtemp(prefix="heddle-scratch-"))
    for r in roots:
        src = (pkg_root / r)
        if src.is_dir():
            shutil.copytree(src, tmp / r)
    return tmp


def shape_result(form: str, result, filters: dict, filter_name: str | None):
    if form == "full":
        return result
    if form == "write_only":
        return {"receipt": str(result) if not isinstance(result, dict) else "done"}
    if form == "summary":
        fn = filters.get(filter_name or "")
        if fn is None:
            raise HeddleError(f"summary form needs a filter named '{filter_name}'")
        return fn(result)
    if form == "scratch":
        return result  # ran against a temp copy; result may be returned
    raise HeddleError(f"unknown form: {form}")
