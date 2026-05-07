from dataclasses import dataclass
from statistics import mean

from shared.simulator import CS_PID, IDLE_PID, Event, SimulationResult


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


@dataclass(frozen=True)
class MetricsReport:
    algorithm: str
    per_process: tuple[ProcessMetrics, ...]
    avg_turnaround: float
    avg_waiting: float
    avg_response: float
    cpu_utilization: float


def compute_metrics(result: SimulationResult) -> MetricsReport:
    first_dispatch: dict[str, int] = {}
    finish: dict[str, int] = {}

    for entry in result.trace:
        if entry.pid is None:
            continue
        if entry.event == Event.DISPATCH and entry.pid not in first_dispatch:
            first_dispatch[entry.pid] = entry.time
        elif entry.event == Event.TERMINATE:
            finish[entry.pid] = entry.time

    per_process: list[ProcessMetrics] = []
    for p in result.workload.processes:
        f = finish[p.pid]
        turnaround = f - p.arrival
        per_process.append(
            ProcessMetrics(
                pid=p.pid,
                arrival=p.arrival,
                cpu_total=p.cpu_total,
                io_total=p.io_total,
                finish=f,
                turnaround=turnaround,
                waiting=turnaround - p.cpu_total - p.io_total,
                response=first_dispatch[p.pid] - p.arrival,
            )
        )

    busy = sum(s.end - s.start for s in result.gantt if s.pid not in (IDLE_PID, CS_PID))
    total = result.gantt[-1].end - result.gantt[0].start if result.gantt else 0
    utilization = busy / total if total > 0 else 0.0

    return MetricsReport(
        algorithm=result.algorithm,
        per_process=tuple(per_process),
        avg_turnaround=mean(pm.turnaround for pm in per_process),
        avg_waiting=mean(pm.waiting for pm in per_process),
        avg_response=mean(pm.response for pm in per_process),
        cpu_utilization=utilization,
    )
