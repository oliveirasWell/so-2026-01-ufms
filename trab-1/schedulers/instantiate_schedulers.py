from models.process.workload import Workload
from schedulers.base import Scheduler
from schedulers.fcfs import FCFS
from schedulers.priority import Priority
from schedulers.round_robin import RoundRobin
from schedulers.sjf import SJF

_SCHEDULER_ENTRIES = (
    ("fcfs", lambda _w: FCFS()),
    ("sjf", lambda _w: SJF(preemptive=False)),
    ("sjf-preemptive", lambda _w: SJF(preemptive=True)),
    ("priority", lambda _w: Priority()),
    ("round-robin", lambda w: RoundRobin(w.quantum)),
)

SCHEDULER_FACTORIES = dict(_SCHEDULER_ENTRIES)
_ALL_KEYS = tuple(k for k, _ in _SCHEDULER_ENTRIES)


def instantiate_schedulers(workload: Workload, algo: str | None = None) -> tuple[Scheduler, ...]:
    keys = _ALL_KEYS if algo is None else (algo,)
    return tuple(SCHEDULER_FACTORIES[k](workload) for k in keys)
