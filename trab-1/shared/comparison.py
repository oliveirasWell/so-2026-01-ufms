from models.metrics.metrics_report import MetricsReport
from models.simulation.simulation_result import SimulationResult
from models.process.workload import Workload
from schedulers.registry import build_algorithms
from shared.metrics import compute_metrics
from shared.simulator import Simulator

METRIC_AVG_TURNAROUND = "avg_turnaround"
METRIC_AVG_WAITING = "avg_waiting"
METRIC_AVG_RESPONSE = "avg_response"
METRIC_CPU_UTILIZATION = "cpu_utilization"

LOWER_IS_BETTER = (METRIC_AVG_TURNAROUND, METRIC_AVG_WAITING, METRIC_AVG_RESPONSE)
HIGHER_IS_BETTER = (METRIC_CPU_UTILIZATION,)
COMPARISON_METRICS = LOWER_IS_BETTER + HIGHER_IS_BETTER


def run_all(workload: Workload) -> list[tuple[SimulationResult, MetricsReport]]:
    pairs: list[tuple[SimulationResult, MetricsReport]] = []
    for scheduler in build_algorithms(workload):
        result = Simulator(workload, scheduler).run()
        pairs.append((result, compute_metrics(result)))
    return pairs


def pick_winners(reports: list[MetricsReport]) -> dict[str, str]:
    if not reports:
        return {}
    winners: dict[str, str] = {}
    for metric in LOWER_IS_BETTER:
        winners[metric] = min(reports, key=lambda r: getattr(r, metric)).algorithm
    for metric in HIGHER_IS_BETTER:
        winners[metric] = max(reports, key=lambda r: getattr(r, metric)).algorithm
    return winners
