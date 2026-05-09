from dataclasses import dataclass

from models.process.process import Process


@dataclass(frozen=True)
class Workload:
    processes: tuple[Process, ...]
    quantum: int = 0
    context_switch_cost: int = 0
