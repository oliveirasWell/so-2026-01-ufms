from dataclasses import dataclass

from models.simulation.trace_entry import TraceEntry
from models.process.workload import Workload


@dataclass(frozen=True)
class SimulationResult:
    algorithm: str
    workload: Workload
    trace: tuple[TraceEntry, ...]
