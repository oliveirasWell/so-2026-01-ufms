from dataclasses import dataclass

from models.metrics.process_metrics import ProcessMetrics


@dataclass(frozen=True)
class MetricsReport:
    algorithm: str
    per_process: tuple[ProcessMetrics, ...]
    avg_turnaround: float
    avg_waiting: float
    avg_response: float
    cpu_utilization: float
    throughput: float
