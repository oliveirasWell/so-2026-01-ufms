import sys
from statistics import mean
from typing import TextIO

from shared.constants import COMPARISON_METRICS
from shared.evaluation import pick_winners
from models.metrics.metrics_report import MetricsReport
from models.simulation.simulation_result import SimulationResult


def aggregate_reports(runs: list[list[MetricsReport]]) -> list[MetricsReport]:
    """Average aggregated metrics per algorithm across multiple runs (same algorithm order)."""
    if not runs:
        return []
    n_algo = len(runs[0])
    out: list[MetricsReport] = []
    for i in range(n_algo):
        algo = runs[0][i].algorithm
        out.append(
            MetricsReport(
                algorithm=algo,
                per_process=tuple(),
                avg_turnaround=mean(r[i].avg_turnaround for r in runs),
                avg_waiting=mean(r[i].avg_waiting for r in runs),
                avg_response=mean(r[i].avg_response for r in runs),
                cpu_utilization=mean(r[i].cpu_utilization for r in runs),
            )
        )
    return out


def print_reports(reports: list[MetricsReport], file: TextIO | None = None) -> None:
    out = file or sys.stdout
    if len(reports) > 1:
        print_comparison(reports, pick_winners(reports), file=out)
    else:
        print_metrics(reports[0], file=out)


def print_metrics(report: MetricsReport, file: TextIO | None = None) -> None:
    out = file or sys.stdout
    cols = ("pid", "arrival", "cpu_total", "io_total", "finish", "turnaround", "waiting", "response")
    out.write(f"{report.algorithm}\n")
    out.write("\t".join(cols) + "\n")
    for pm in report.per_process:
        out.write("\t".join((
            pm.pid,
            str(pm.arrival),
            str(pm.cpu_total),
            str(pm.io_total),
            str(pm.finish),
            str(pm.turnaround),
            str(pm.waiting),
            str(pm.response),
        )) + "\n")
    out.write(
        f"avg_turnaround={report.avg_turnaround:.4f}  "
        f"avg_waiting={report.avg_waiting:.4f}  "
        f"avg_response={report.avg_response:.4f}  "
        f"cpu_utilization={report.cpu_utilization:.4f}\n"
    )


def print_trace(result: SimulationResult, file: TextIO | None = None) -> None:
    out = file or sys.stdout
    cols = ("time", "event", "pid", "running", "ready", "blocked")
    out.write(f"{result.algorithm} trace\n")
    out.write("\t".join(cols) + "\n")
    for e in result.trace:
        out.write("\t".join((
            str(e.time),
            e.event.value,
            e.pid,
            e.running or "-",
            ",".join(e.ready_queue) or "-",
            ",".join(e.blocked) or "-",
        )) + "\n")


def print_comparison(
    reports: list[MetricsReport],
    winners: dict[str, str],
    file: TextIO | None = None,
    *,
    title: str = "Comparison",
) -> None:
    out = file or sys.stdout
    headers = ("algorithm",) + COMPARISON_METRICS
    out.write(f"{title}\n")
    out.write("\t".join(headers) + "\n")
    for r in reports:
        out.write("\t".join((
            r.algorithm,
            f"{r.avg_turnaround:.4f}",
            f"{r.avg_waiting:.4f}",
            f"{r.avg_response:.4f}",
            f"{r.cpu_utilization:.4f}",
        )) + "\n")
    out.write("\nWinner per metric\n")
    for metric in COMPARISON_METRICS:
        out.write(f"  {metric}: {winners.get(metric, '-')}\n")
