from dataclasses import dataclass


@dataclass(frozen=True)
class GanttSlice:
    pid: str
    start: int
    end: int
