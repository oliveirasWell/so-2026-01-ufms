from dataclasses import dataclass

from models.workload.event import Event


@dataclass(frozen=True)
class Workload:
    total_memory: int
    events: list[Event]
