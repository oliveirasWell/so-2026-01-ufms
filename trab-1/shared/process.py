from dataclasses import dataclass


@dataclass(frozen=True)
class Process:
    pid: str
    arrival: int
    priority: int
    bursts: tuple[int, ...]

    @property
    def cpu_total(self) -> int:
        return sum(self.bursts[i] for i in range(0, len(self.bursts), 2))

    @property
    def io_total(self) -> int:
        return sum(self.bursts[i] for i in range(1, len(self.bursts), 2))


@dataclass(frozen=True)
class Workload:
    processes: tuple[Process, ...]
    quantum: int | None
    context_switch_cost: int = 0
