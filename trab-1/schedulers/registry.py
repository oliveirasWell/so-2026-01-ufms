from collections.abc import Callable

from models.process.workload import Workload
from schedulers.base import Scheduler
from schedulers.fcfs import FCFS
from schedulers.priority import Priority
from schedulers.round_robin import RoundRobin
from schedulers.sjf import SJF

# Single source of truth: (CLI flag, factory). Order is the comparison order in run_all.
_SCHEDULER_ENTRIES: tuple[tuple[str, Callable[[Workload], Scheduler]], ...] = (
    ("fcfs", lambda _w: FCFS()),
    ("sjf", lambda _w: SJF(preemptive=False)),
    ("sjf-preemptive", lambda _w: SJF(preemptive=True)),
    ("priority", lambda _w: Priority()),
    ("round-robin", lambda w: RoundRobin(w.quantum)),
)

SCHEDULER_FACTORIES: dict[str, Callable[[Workload], Scheduler]] = dict(_SCHEDULER_ENTRIES)


def build_algorithms(workload: Workload) -> tuple[Scheduler, ...]:
    return tuple(factory(workload) for _, factory in _SCHEDULER_ENTRIES)
