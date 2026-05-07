from schedulers.base import Scheduler
from schedulers.fcfs import FCFS
from schedulers.priority import Priority
from schedulers.round_robin import RoundRobin
from schedulers.sjf import SJF
from shared.metrics import MetricsReport, compute_metrics
from shared.process import Workload
from shared.simulator import SimulationResult, run

METRIC_AVG_TURNAROUND = "avg_turnaround"
METRIC_AVG_WAITING = "avg_waiting"
METRIC_AVG_RESPONSE = "avg_response"
METRIC_CPU_UTILIZATION = "cpu_utilization"

LOWER_IS_BETTER = (METRIC_AVG_TURNAROUND, METRIC_AVG_WAITING, METRIC_AVG_RESPONSE)
HIGHER_IS_BETTER = (METRIC_CPU_UTILIZATION,)
COMPARISON_METRICS = LOWER_IS_BETTER + HIGHER_IS_BETTER


def build_algorithms(workload: Workload) -> tuple[Scheduler, ...]:
    schedulers: list[Scheduler] = [
        FCFS(),
        SJF(preemptive=False),
        SJF(preemptive=True),
        Priority(),
    ]
    if workload.quantum is not None:
        schedulers.append(RoundRobin(workload.quantum))
    return tuple(schedulers)


def run_all(workload: Workload) -> list[tuple[SimulationResult, MetricsReport]]:
    pairs: list[tuple[SimulationResult, MetricsReport]] = []
    for scheduler in build_algorithms(workload):
        result = run(workload, scheduler)
        pairs.append((result, compute_metrics(result)))
    return pairs


def build_comparison_table(reports: list[MetricsReport]) -> list[dict]:
    rows: list[dict] = []
    for r in reports:
        rows.append(
            {
                "algorithm": r.algorithm,
                METRIC_AVG_TURNAROUND: r.avg_turnaround,
                METRIC_AVG_WAITING: r.avg_waiting,
                METRIC_AVG_RESPONSE: r.avg_response,
                METRIC_CPU_UTILIZATION: r.cpu_utilization,
            }
        )
    return rows


def pick_winners(reports: list[MetricsReport]) -> dict[str, str]:
    if not reports:
        return {}
    winners: dict[str, str] = {}
    for metric in LOWER_IS_BETTER:
        winners[metric] = min(reports, key=lambda r: getattr(r, metric)).algorithm
    for metric in HIGHER_IS_BETTER:
        winners[metric] = max(reports, key=lambda r: getattr(r, metric)).algorithm
    return winners
