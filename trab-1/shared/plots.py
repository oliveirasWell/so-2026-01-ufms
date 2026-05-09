import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from shared.comparison import COMPARISON_METRICS
from models.metrics.metrics_report import MetricsReport
from models.simulation.constants import CS_PID, IDLE_PID
from models.simulation.simulation_result import SimulationResult

_NEUTRAL_COLOR = "#bdbdbd"
_CS_COLOR = "#9e9e9e"


def plot_gantt(result: SimulationResult, ax: Axes | None = None) -> Axes:
    if ax is None:
        _, ax = plt.subplots(figsize=(10, 3))

    pids = [p.pid for p in result.workload.processes]
    palette = plt.get_cmap("tab10")
    color_map = {pid: palette(i % 10) for i, pid in enumerate(pids)}
    color_map[IDLE_PID] = _NEUTRAL_COLOR
    color_map[CS_PID] = _CS_COLOR

    lanes = pids + [IDLE_PID, CS_PID]
    lane_index = {name: i for i, name in enumerate(lanes)}

    for slc in result.gantt:
        y = lane_index[slc.pid]
        ax.broken_barh(
            [(slc.start, slc.end - slc.start)],
            (y - 0.4, 0.8),
            facecolors=color_map[slc.pid],
            edgecolor="black",
            linewidth=0.5,
        )

    ax.set_yticks(range(len(lanes)))
    ax.set_yticklabels(lanes)
    ax.set_xlabel("time")
    ax.set_title(result.algorithm)
    ax.invert_yaxis()
    ax.grid(axis="x", linestyle=":", alpha=0.5)
    return ax


def plot_metric_bars(
    reports: list[MetricsReport],
    metric: str,
    ax: Axes | None = None,
) -> Axes:
    if metric not in COMPARISON_METRICS:
        raise ValueError(f"unknown metric '{metric}'")
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 4))

    names = [r.algorithm for r in reports]
    values = [getattr(r, metric) for r in reports]
    palette = plt.get_cmap("tab10")
    colors = [palette(i % 10) for i in range(len(reports))]
    ax.bar(names, values, color=colors)
    ax.set_ylabel(metric)
    ax.set_title(metric)
    ax.tick_params(axis="x", rotation=20)
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    return ax
