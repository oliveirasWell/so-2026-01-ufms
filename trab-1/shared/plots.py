import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.lines import Line2D

from shared.constants import COMPARISON_METRICS
from shared.gantt import build_gantt
from models.metrics.metrics_report import MetricsReport
from models.simulation.simulation_result import SimulationResult
from models.simulation.trace.constants import CS_PID, IDLE_PID
from models.visualization.gantt_slice import GanttSlice

_NEUTRAL_COLOR = "#bdbdbd"
_CS_COLOR = "#9e9e9e"


def plot_gantt(
    result: SimulationResult,
    ax: Axes | None = None,
    gantt: tuple[GanttSlice, ...] | None = None,
) -> Axes:
    if ax is None:
        _, ax = plt.subplots(figsize=(10, 3))
    if gantt is None:
        gantt = build_gantt(result)

    pids = [p.pid for p in result.workload.processes]
    palette = plt.get_cmap("tab10")
    color_map = {pid: palette(i % 10) for i, pid in enumerate(pids)}
    color_map[IDLE_PID] = _NEUTRAL_COLOR
    color_map[CS_PID] = _CS_COLOR

    lanes = pids + [IDLE_PID, CS_PID]
    lane_index = {name: i for i, name in enumerate(lanes)}

    for slc in gantt:
        y = lane_index[slc.pid]
        ax.broken_barh(
            [(slc.start, slc.end - slc.start)],
            (y - 0.4, 0.8),
            facecolors=color_map[slc.pid],
            edgecolor="black",
            linewidth=0.5,
            zorder=1,
        )

    ax.set_yticks(range(len(lanes)))
    ax.set_yticklabels(lanes)
    ax.set_xlabel("time")
    ax.set_title(result.algorithm)
    ax.invert_yaxis()
    ax.grid(axis="x", linestyle=":", alpha=0.5)
    ax.margins(x=0.02)

    for p in result.workload.processes:
        y = lane_index[p.pid]
        c = color_map[p.pid]
        ax.plot(
            [p.arrival, p.arrival],
            [y - 0.42, y + 0.42],
            color=c,
            linewidth=3,
            solid_capstyle="butt",
            zorder=4,
            clip_on=False,
        )
        ax.plot(
            p.arrival,
            y,
            marker="v",
            markersize=9,
            markerfacecolor=c,
            markeredgecolor="black",
            markeredgewidth=0.8,
            linestyle="None",
            zorder=5,
            clip_on=False,
        )
    ax.legend(
        handles=[
            Line2D(
                [0],
                [0],
                marker="v",
                color="w",
                markerfacecolor="gray",
                markeredgecolor="black",
                markersize=9,
                linestyle="None",
                label="chegada",
            ),
        ],
        loc="upper right",
        fontsize=8,
    )

    return ax


def plot_metric_bars(
    reports: list[MetricsReport],
    metric: str,
    ax: Axes | None = None,
) -> Axes:
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
