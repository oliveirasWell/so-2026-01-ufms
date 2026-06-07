"""Matplotlib helpers for the analysis notebook.

The memory map (``plot_memory_timeline``) is the counterpart of trab-1's Gantt
chart: address on the y-axis, event on the x-axis, each occupied partition drawn
as a colored band so external fragmentation is visible as the memory breaks into
scattered holes over time.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from models.types import ChooseFunction
from models.workload.workload import Workload
from shared.simulator import timeline


def pid_color_map(snapshots: list[list]) -> dict[str, tuple]:
    """Stable pid -> color across every snapshot of one run."""
    pids: list[str] = []
    for blocks in snapshots:
        for b in blocks:
            if not b.is_free and b.pid not in pids:
                pids.append(b.pid)
    palette = plt.get_cmap("tab20")
    return {pid: palette(i % 20) for i, pid in enumerate(pids)}


def plot_memory_timeline(
    snapshots: list[list],
    total_size: int,
    *,
    ax=None,
    title: str = "",
    legend: bool = True,
):
    if ax is None:
        _, ax = plt.subplots(figsize=(11, 4))

    colors = pid_color_map(snapshots)
    for event, blocks in enumerate(snapshots):
        for b in blocks:
            if b.is_free:
                continue
            ax.broken_barh(
                [(event, 1)], (b.start, b.size),
                facecolors=colors[b.pid], edgecolors="white", linewidth=0.4,
            )

    ax.set_xlim(0, len(snapshots))
    ax.set_ylim(0, total_size)
    ax.invert_yaxis()  # low addresses on top, classic memory-map orientation
    ax.set_xlabel("evento")
    ax.set_ylabel("endereço")
    ax.set_title(title)
    if legend and colors:
        ax.legend(
            handles=[Patch(color=c, label=pid) for pid, c in colors.items()],
            loc="center left", bbox_to_anchor=(1.0, 0.5), fontsize=8,
            ncol=max(1, (len(colors) + 14) // 15),
        )
    return ax


def plot_metric_bars(reports: list[tuple[str, dict]], metric: str, *, ax=None, label=None):
    if ax is None:
        _, ax = plt.subplots(figsize=(6, 3))
    names = [name for name, _ in reports]
    values = [summary[metric] for _, summary in reports]
    palette = plt.get_cmap("tab10")
    ax.bar(names, values, color=[palette(i) for i in range(len(names))])
    ax.set_title(label or metric)
    ax.tick_params(axis="x", rotation=15)
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    return ax


def plot_largest_gap_evolution(
    workload: Workload,
    algorithms: tuple[tuple[str, ChooseFunction], ...],
    *,
    ax=None,
):
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 4))
    for name, choose in algorithms:
        series = [
            max((b.size for b in blocks if b.is_free), default=0)
            for blocks in timeline(workload, choose)
        ]
        ax.plot(range(1, len(series) + 1), series, marker="o", label=name)
    ax.set_xlabel("evento")
    ax.set_ylabel("maior brecha livre")
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    ax.legend()
    return ax
