"""Event-by-event simulation orchestration.

Applies each workload event to the memory using a gap-choosing algorithm
(`choose(memory, size) -> int | None`) and classifies the result. Keeps
aggregate statistics used by the final report.

Classification of an allocation the algorithm refused (choose -> None):
- sum of gaps >= requested size  => EXTERNAL FRAGMENTATION
  (total space exists, just not contiguous — the literal definition)
- sum of gaps <  requested size  => NO SPACE
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Literal

from simulator.memory import Memory
from simulator.parser import Event, Workload


ResultKind = Literal[
    "ALLOCATED",
    "FREED",
    "FREED_MISSING",
    "FAIL_EXTERNAL_FRAGMENTATION",
    "FAIL_NO_SPACE",
]


@dataclass(frozen=True)
class EventResult:
    event: Event
    kind: ResultKind
    gap_index: int | None = None  # set for ALLOCATED


@dataclass
class Statistics:
    total_events: int = 0
    allocated: int = 0
    freed: int = 0
    freed_missing: int = 0
    external_fragmentation_failures: int = 0
    no_space_failures: int = 0
    usage_per_event: list[int] = field(default_factory=list)
    merges: int = 0


ChooseFunction = Callable[[Memory, int], int | None]


def process(
    memory: Memory,
    event: Event,
    choose: ChooseFunction,
) -> EventResult:
    if event.kind == "ALOC":
        assert event.size is not None
        index = choose(memory, event.size)
        if index is not None:
            memory.allocate(event.pid, event.size, index)
            return EventResult(event, "ALLOCATED", gap_index=index)
        # Algorithm refused: tell external fragmentation from lack of space.
        if memory.free_space() >= event.size:
            return EventResult(event, "FAIL_EXTERNAL_FRAGMENTATION")
        return EventResult(event, "FAIL_NO_SPACE")

    # kind == "LIBERA"
    found = memory.free(event.pid)
    return EventResult(event, "FREED" if found else "FREED_MISSING")


def run(
    workload: Workload,
    choose: ChooseFunction,
    *,
    on_event: Callable[[EventResult, Memory], None] | None = None,
) -> tuple[Memory, Statistics]:
    """Apply every workload event and return (final memory, stats).

    `on_event`, if given, is called after each event — used by main to
    print the state in verbose mode.
    """
    memory = Memory(workload.total_memory)
    stats = Statistics()

    for event in workload.events:
        result = process(memory, event, choose)
        stats.total_events += 1
        if result.kind == "ALLOCATED":
            stats.allocated += 1
        elif result.kind == "FREED":
            stats.freed += 1
        elif result.kind == "FREED_MISSING":
            stats.freed_missing += 1
        elif result.kind == "FAIL_EXTERNAL_FRAGMENTATION":
            stats.external_fragmentation_failures += 1
        elif result.kind == "FAIL_NO_SPACE":
            stats.no_space_failures += 1
        stats.usage_per_event.append(memory.used())

        if on_event is not None:
            on_event(result, memory)

    stats.merges = memory.merges
    return memory, stats


@dataclass(frozen=True)
class SimulationResult:
    algorithm: str
    memory: Memory
    stats: Statistics


def run_simulation(
    workload: Workload,
    algo: str | None = None,
    *,
    on_event: Callable[[EventResult, Memory], None] | None = None,
) -> list[SimulationResult]:
    """`algo=None` runs all three; otherwise only the requested one."""
    # local import avoids a cycle (the registry references this module)
    from simulator.algorithms.instantiate_algorithms import instantiate_algorithms

    results: list[SimulationResult] = []
    for name, choose in instantiate_algorithms(algo):
        memory, stats = run(workload, choose, on_event=on_event)
        results.append(SimulationResult(algorithm=name, memory=memory, stats=stats))
    return results
