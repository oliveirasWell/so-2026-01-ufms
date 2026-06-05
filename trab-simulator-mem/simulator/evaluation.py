"""Per-metric winner: fewer failures/rejections and more utilization.

Tie: the first algorithm in insertion order wins.
"""

from __future__ import annotations

LOWER_IS_BETTER = (
    "external_fragmentation_failures",
    "no_space_failures",
    "total_rejected",
)
HIGHER_IS_BETTER = ("final_utilization_pct",)


def _value(summary: dict, metric: str) -> float:
    if metric == "total_rejected":
        return summary["external_fragmentation_failures"] + summary["no_space_failures"]
    return summary[metric]


def pick_winners(reports: dict[str, dict]) -> dict[str, str]:
    """`total_rejected` is derived from the sum of the two failure counts."""
    if not reports:
        return {}
    items = list(reports.items())
    winners: dict[str, str] = {}
    for metric in LOWER_IS_BETTER:
        winners[metric] = min(items, key=lambda kv: _value(kv[1], metric))[0]
    for metric in HIGHER_IS_BETTER:
        winners[metric] = max(items, key=lambda kv: _value(kv[1], metric))[0]
    return winners
