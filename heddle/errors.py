"""heddle.errors — one error type. Validation collects; execution raises."""

from __future__ import annotations


class HeddleError(Exception):
    pass


class Problem:
    """One validation problem: file, optional line, message, suggested fix."""

    def __init__(self, file: str, line: int | None, message: str, fix: str | None = None):
        self.file = file
        self.line = line
        self.message = message
        self.fix = fix

    def __str__(self) -> str:
        loc = self.file if self.line is None else f"{self.file}:{self.line}"
        out = f"{loc}  {self.message}"
        if self.fix:
            out += f"\n{' ' * (len(loc) + 2)}{self.fix}"
        return out
