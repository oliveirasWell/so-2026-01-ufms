"""Reads the JSON input file.

Expected format:

    {
      "memoria_total": 1000,
      "eventos": [
        {"tipo": "ALOC",   "pid": "P1", "tamanho": 200},
        {"tipo": "ALOC",   "pid": "P2", "tamanho": 300},
        {"tipo": "LIBERA", "pid": "P1"}
      ]
    }

The user guarantees the file is well-formed.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal


EventKind = Literal["ALOC", "LIBERA"]


@dataclass(frozen=True)
class Event:
    kind: EventKind
    pid: str
    size: int | None = None  # required for ALOC, absent for LIBERA


@dataclass(frozen=True)
class Workload:
    total_memory: int
    events: list[Event]


def parse_input(path: str | Path) -> Workload:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    total_memory = int(raw["memoria_total"])
    events: list[Event] = []
    for ev in raw["eventos"]:
        kind = ev["tipo"]
        pid = str(ev["pid"])
        size = int(ev["tamanho"]) if kind == "ALOC" else None
        events.append(Event(kind=kind, pid=pid, size=size))

    return Workload(total_memory=total_memory, events=events)
