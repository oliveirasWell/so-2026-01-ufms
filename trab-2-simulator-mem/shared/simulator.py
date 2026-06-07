"""Event-by-event simulation engine.

Applies each workload event to the memory using a gap-choosing algorithm
(``choose(memory, size) -> int | None``) and classifies the result. Keeps the
aggregate statistics used by the final report.

Classification of an allocation the algorithm refused (choose -> None):
- sum of gaps >= requested size  => EXTERNAL FRAGMENTATION
  (total space exists, just not contiguous — the literal definition)
- sum of gaps <  requested size  => NO SPACE
"""

import copy
from collections.abc import Callable

from models.memory.memory import Memory
from models.simulation.event_result import EventResult
from models.simulation.result_kind import ResultKind
from models.simulation.statistics import Statistics
from models.types import ChooseFunction
from models.workload.event import Event
from models.workload.event_type import EventType
from models.workload.workload import Workload

OnEvent = Callable[[int, EventResult, Memory], None]

_COUNTERS = {
    ResultKind.ALLOCATED: "allocated",
    ResultKind.FREED: "freed",
    ResultKind.FREED_MISSING: "freed_missing",
    ResultKind.FAIL_EXTERNAL_FRAGMENTATION: "external_fragmentation_failures",
    ResultKind.FAIL_NO_SPACE: "no_space_failures",
}


def process(memory: Memory, event: Event, choose: ChooseFunction) -> EventResult:
    if event.type == EventType.ALLOC:
        assert event.size is not None
        index = choose(memory, event.size)
        if index is not None:
            memory.allocate(event.pid, event.size, index)
            return EventResult(event, ResultKind.ALLOCATED, gap_index=index)
        # Algorithm refused: tell external fragmentation from lack of space.
        if memory.free_space() >= event.size:
            return EventResult(event, ResultKind.FAIL_EXTERNAL_FRAGMENTATION)
        return EventResult(event, ResultKind.FAIL_NO_SPACE)

    found = memory.free(event.pid)
    return EventResult(event, ResultKind.FREED if found else ResultKind.FREED_MISSING)


def _accumulate(stats: Statistics, result: EventResult) -> None:
    stats.total_events += 1
    attr = _COUNTERS[result.kind]
    setattr(stats, attr, getattr(stats, attr) + 1)


def run(
    workload: Workload,
    choose: ChooseFunction,
    *,
    on_event: OnEvent | None = None,
) -> tuple[Memory, Statistics]:
    """Apply every workload event and return (final memory, stats).

    ``on_event``, if given, is called after each event — used by main to
    print the state in verbose mode.
    """
    memory = Memory(workload.total_memory)
    stats = Statistics()

    for number, event in enumerate(workload.events, start=1):
        result = process(memory, event, choose)
        _accumulate(stats, result)
        stats.usage_per_event.append(memory.used())
        if on_event is not None:
            on_event(number, result, memory)

    stats.merges = memory.merges
    return memory, stats


def timeline(workload: Workload, choose: ChooseFunction) -> list[list]:
    """Snapshot of ``memory.blocks`` after each event — drives the memory map."""
    snapshots: list[list] = []
    run(workload, choose, on_event=lambda _n, _r, memory: snapshots.append(copy.deepcopy(memory.blocks)))
    return snapshots
