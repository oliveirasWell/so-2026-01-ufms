from dataclasses import dataclass

from models.simulation.event import Event


@dataclass(frozen=True)
class TraceEntry:
    time: int
    event: Event
    pid: str | None
    ready_queue: tuple[str, ...]
    blocked: tuple[str, ...]
    running: str | None
