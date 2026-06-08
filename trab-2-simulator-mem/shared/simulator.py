"""Event-by-event simulation engine.

Applies each workload event to the memory using a gap-choosing algorithm
(``choose(memory, size) -> int | None``) and classifies the result. Keeps the
aggregate statistics used by the final report.

Classification of an allocation the algorithm refused (choose -> None):
- sum of gaps >= requested size  => EXTERNAL FRAGMENTATION
  (total space exists, just not contiguous — the literal definition)
- sum of gaps <  requested size  => NO SPACE
"""

from models.memory.memory import Memory
from models.simulation.event_result import EventResult
from models.simulation.result_kind import ResultKind
from models.simulation.statistics import Statistics
from models.types import ChooseFunction, OnEvent
from models.workload.event import Event
from models.workload.event_type import EventType
from models.workload.workload import Workload
from shared.constants import RESULT_KIND_COUNTERS


class Simulator:
    def __init__(
        self,
        workload: Workload,
        choose: ChooseFunction,
        *,
        on_event: OnEvent | None = None,
    ):
        self.workload = workload
        self.choose = choose
        self.on_event = on_event
        self.memory = Memory(workload.total_memory)
        self.stats = Statistics()

    def run(self) -> tuple[Memory, Statistics]:
        for number, event in enumerate(self.workload.events, start=1):
            result = self._apply(event)
            self._accumulate(result)
            self.stats.usage_per_event.append(self.memory.used())
            if self.on_event is not None:
                self.on_event(number, result, self.memory)

        self.stats.merges = self.memory.merges
        return self.memory, self.stats

    def _apply(self, event: Event) -> EventResult:
        if event.type == EventType.ALLOC:
            return self._alloc(event)
        return self._free(event)

    def _alloc(self, event: Event) -> EventResult:
        assert event.size is not None
        index = self.choose(self.memory, event.size)
        if index is not None:
            self.memory.allocate(event.pid, event.size, index)
            return EventResult(event, ResultKind.ALLOCATED, gap_index=index)
        
        # Algorithm refused: total free space exists but not contiguously =>
        # external fragmentation; otherwise it is plain lack of space.
        if self.memory.free_space() >= event.size:
            return EventResult(event, ResultKind.FAIL_EXTERNAL_FRAGMENTATION)
        return EventResult(event, ResultKind.FAIL_NO_SPACE)

    def _free(self, event: Event) -> EventResult:
        found = self.memory.free(event.pid)
        return EventResult(event, ResultKind.FREED if found else ResultKind.FREED_MISSING)

    def _accumulate(self, result: EventResult) -> None:
        self.stats.total_events += 1
        attr = RESULT_KIND_COUNTERS[result.kind]
        setattr(self.stats, attr, getattr(self.stats, attr) + 1)
