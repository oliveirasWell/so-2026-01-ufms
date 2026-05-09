import sys
from typing import TextIO

from shared.comparison import COMPARISON_METRICS
from models.metrics.metrics_report import MetricsReport
from models.simulation.simulation_result import SimulationResult


def print_metrics(report: MetricsReport, file: TextIO | None = None) -> None:
    out = file or sys.stdout
    headers = ("pid", "arrival", "cpu_total", "io_total", "finish", "turnaround", "waiting", "response")
    rows = [
        (pm.pid, str(pm.arrival), str(pm.cpu_total), str(pm.io_total),
         str(pm.finish), str(pm.turnaround), str(pm.waiting), str(pm.response))
        for pm in report.per_process
    ]
    _print_table(out, report.algorithm, headers, rows)
    out.write(
        f"avg_turnaround={report.avg_turnaround:.4f}  "
        f"avg_waiting={report.avg_waiting:.4f}  "
        f"avg_response={report.avg_response:.4f}  "
        f"cpu_utilization={report.cpu_utilization:.4f}\n"
    )


def print_trace(result: SimulationResult, file: TextIO | None = None) -> None:
    out = file or sys.stdout
    headers = ("time", "event", "pid", "running", "ready", "blocked")
    rows = [
        (str(e.time), e.event.value, e.pid or "-", e.running or "-",
         ",".join(e.ready_queue) or "-", ",".join(e.blocked) or "-")
        for e in result.trace
    ]
    _print_table(out, f"{result.algorithm} trace", headers, rows)


def print_comparison(
    reports: list[MetricsReport],
    winners: dict[str, str],
    file: TextIO | None = None,
) -> None:
    out = file or sys.stdout
    headers = ("algorithm",) + COMPARISON_METRICS
    rows = [
        (r.algorithm, f"{r.avg_turnaround:.4f}", f"{r.avg_waiting:.4f}",
         f"{r.avg_response:.4f}", f"{r.cpu_utilization:.4f}")
        for r in reports
    ]
    _print_table(out, "Comparison", headers, rows)
    out.write("\nWinner per metric\n")
    for metric in COMPARISON_METRICS:
        out.write(f"  {metric}: {winners.get(metric, '-')}\n")


def _print_table(
    out: TextIO,
    title: str,
    headers: tuple[str, ...],
    rows: list[tuple[str, ...]],
) -> None:
    widths = _column_widths(headers, rows)
    out.write(f"{title}\n")
    out.write(_format_row(headers, widths) + "\n")
    out.write(_format_row(tuple("-" * w for w in widths), widths) + "\n")
    for row in rows:
        out.write(_format_row(row, widths) + "\n")


def _column_widths(headers: tuple[str, ...], rows: list[tuple[str, ...]]) -> list[int]:
    if not rows:
        return [len(h) for h in headers]
    return [max(len(h), *(len(row[i]) for row in rows)) for i, h in enumerate(headers)]


def _format_row(row: tuple[str, ...], widths: list[int]) -> str:
    return "  ".join(cell.ljust(w) for cell, w in zip(row, widths))
