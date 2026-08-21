from __future__ import annotations
import json, time
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

class TraceWriter:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, event: str, payload: Any) -> None:
        if is_dataclass(payload):
            payload = asdict(payload)
        rec = {"ts": time.time(), "event": event, "payload": payload}
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")
