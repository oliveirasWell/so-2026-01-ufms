from dataclasses import dataclass

from models.simulation.trace.event import Event


@dataclass(frozen=True)
class TraceEntry:
    time: int
    event: Event
    pid: str
    ready_queue: tuple[str, ...]
    blocked: tuple[str, ...]
    running: str | None
