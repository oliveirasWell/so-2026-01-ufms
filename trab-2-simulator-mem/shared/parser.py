"""Reads the JSON input file.

Expected format:

    {
      "total_memory": 1000,
      "events": [
        {"type": "ALLOC", "pid": "P1", "size": 200},
        {"type": "ALLOC", "pid": "P2", "size": 300},
        {"type": "FREE",  "pid": "P1"}
      ]
    }

The user guarantees the file is well-formed.
"""

import json
from pathlib import Path

from models.workload.event import Event
from models.workload.event_type import EventType
from models.workload.workload import Workload


def _hook(d: dict):
    # json calls this hook for every {...} object, inside-out: events first
    # (they carry "type"), then the root object ("total_memory"/"events").
    if "type" in d:
        return Event(type=EventType(d["type"]), pid=str(d["pid"]), size=d.get("size"))
    return Workload(total_memory=int(d["total_memory"]), events=list(d.get("events", ())))


def parse_input(path: str | Path) -> Workload:
    return json.loads(Path(path).read_text("utf-8"), object_hook=_hook)
