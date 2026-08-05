"""heddle.runlog — JSONL, one line per event. A record, not evidence."""

from __future__ import annotations

import json
import time
from pathlib import Path


class RunLog:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._fh = self.path.open("a", encoding="utf-8")

    def event(self, kind: str, **fields):
        rec = {"t": round(time.time(), 3), "event": kind, **fields}
        self._fh.write(json.dumps(rec, default=str) + "\n")
        self._fh.flush()

    def close(self):
        self._fh.close()
