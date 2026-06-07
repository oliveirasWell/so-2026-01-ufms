from dataclasses import dataclass

from models.workload.event_type import EventType


@dataclass(frozen=True)
class Event:
    type: EventType
    pid: str
    size: int | None = None
