from models.metrics.metrics_report import MetricsReport
from models.process.workload import Workload
from models.simulation.gantt_slice import GanttSlice
from models.simulation.simulation_result import SimulationResult
from schedulers.instantiate_schedulers import instantiate_schedulers
from shared.gantt import build_gantt
from shared.metrics import compute_metrics
from shared.simulator import Simulator


def run_simulation(
    workload: Workload,
    algo: str | None = None,
) -> tuple[
    list[SimulationResult],
    list[tuple[GanttSlice, ...]],
    list[MetricsReport],
]:
    results: list[SimulationResult] = []
    gantts: list[tuple[GanttSlice, ...]] = []
    reports: list[MetricsReport] = []

    for scheduler in instantiate_schedulers(workload, algo):
        result = Simulator(workload, scheduler).run()
        gantt = build_gantt(result)
        report = compute_metrics(result, gantt=gantt)
        
        results.append(result)
        gantts.append(gantt)
        reports.append(report)

    return results, gantts, reports
