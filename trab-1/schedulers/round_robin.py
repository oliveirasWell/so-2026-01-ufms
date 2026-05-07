from typing import ClassVar

from schedulers.base import Scheduler
from shared.runtime_process import RuntimeProcess


class RoundRobin(Scheduler):
    name: ClassVar[str] = "Round Robin"

    def __init__(self, quantum: int) -> None:
        if quantum <= 0:
            raise ValueError("Round Robin requires positive quantum")
        self._quantum = quantum

    def pick_next(self, ready: list[RuntimeProcess], now: int) -> RuntimeProcess | None:
        return ready[0] if ready else None

    def quantum(self) -> int | None:
        return self._quantum
