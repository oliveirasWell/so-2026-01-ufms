from dataclasses import dataclass

from models.memory.memory import Memory
from models.simulation.statistics import Statistics


@dataclass(frozen=True)
class SimulationResult:
    algorithm: str
    memory: Memory
    stats: Statistics
