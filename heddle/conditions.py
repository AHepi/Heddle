"""heddle.conditions — the tiny 'when' language.

A condition reads only outcome(skill.step), count(list), stored(name), or a
comparison of those against a literal or each other. It never reads prose.
Grammar:  EXPR := TERM (OP TERM)?
          TERM := outcome(a.b) | count(x) | stored(x) | int | ident
"""

from __future__ import annotations

import re

from .errors import HeddleError

_TOKEN = re.compile(r"""
    \s*(?:(?P<call>outcome|count|stored)\((?P<arg>[A-Za-z0-9_.-]+)\)
       |(?P<int>-?\d+)
       |(?P<op>==|!=|<=|>=|<|>)
       |(?P<ident>[A-Za-z_][A-Za-z0-9_.-]*))
""", re.VERBOSE)


class _Ctx:
    def __init__(self, outcomes, lists, stored):
        self.outcomes, self.lists, self.stored = outcomes, lists, stored


def _term(tok, ctx: _Ctx):
    kind, val = tok
    if kind == "call":
        fn, arg = val
        if fn == "outcome":
            return ctx.outcomes.get(arg)
        if fn == "count":
            return len(ctx.lists.get(arg, []))
        return ctx.stored.get(arg)
    if kind == "int":
        return int(val)
    if kind == "ident":
        if val in ctx.stored:
            return ctx.stored[val]
        return val  # bare literal, e.g. an outcome name
    raise HeddleError(f"bad term in condition: {val!r}")


def tokenize(expr: str):
    out, pos = [], 0
    while pos < len(expr):
        m = _TOKEN.match(expr, pos)
        if not m:
            raise HeddleError(f"cannot parse condition near: {expr[pos:]!r}")
        pos = m.end()
        if m.group("call"):
            out.append(("call", (m.group("call"), m.group("arg"))))
        elif m.group("op"):
            out.append(("op", m.group("op")))
        elif m.group("int"):
            out.append(("int", m.group("int")))
        else:
            out.append(("ident", m.group("ident")))
    return out


def evaluate(expr: str, outcomes: dict, lists: dict, stored: dict) -> bool:
    toks = tokenize(str(expr).strip())
    ctx = _Ctx(outcomes, lists, stored)
    if not toks:
        raise HeddleError("empty condition")
    if len(toks) == 1:
        return bool(_term(toks[0], ctx))
    if len(toks) == 3 and toks[1][0] == "op":
        left, right = _term(toks[0], ctx), _term(toks[2], ctx)
        op = toks[1][1]
        if op == "==": return left == right
        if op == "!=": return left != right
        try:
            if op == "<":  return left < right
            if op == ">":  return left > right
            if op == "<=": return left <= right
            if op == ">=": return left >= right
        except TypeError:
            return False
    raise HeddleError(f"unsupported condition shape: {expr!r}")
