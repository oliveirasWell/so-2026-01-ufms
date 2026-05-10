from models.metrics.metrics_report import MetricsReport
from shared.constants import HIGHER_IS_BETTER, LOWER_IS_BETTER


def pick_winners(reports: list[MetricsReport]) -> dict[str, str]:
    if not reports:
        return {}
    winners: dict[str, str] = {}
    for metric in LOWER_IS_BETTER:
        winners[metric] = min(reports, key=lambda r, m=metric: getattr(r, m)).algorithm
    for metric in HIGHER_IS_BETTER:
        winners[metric] = max(reports, key=lambda r, m=metric: getattr(r, m)).algorithm
    return winners
