from dataclasses import dataclass

from models.simulation.result_kind import ResultKind
from models.workload.event import Event


@dataclass(frozen=True)
class EventResult:
    event: Event
    kind: ResultKind
    gap_index: int | None = None  # set for ALLOCATED
