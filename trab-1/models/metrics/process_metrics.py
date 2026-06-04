from dataclasses import dataclass


@dataclass(frozen=True)
class ProcessMetrics:
    pid: str
    arrival: int
    cpu_total: int
    io_total: int
    finish: int
    turnaround: int
    waiting: int
    response: int
