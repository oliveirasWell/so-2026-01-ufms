from dataclasses import dataclass

from models.simulation.gantt_slice import GanttSlice
from models.simulation.trace_entry import TraceEntry
from models.process.workload import Workload


@dataclass(frozen=True)
class SimulationResult:
    algorithm: str
    workload: Workload
    gantt: tuple[GanttSlice, ...]
    trace: tuple[TraceEntry, ...]
