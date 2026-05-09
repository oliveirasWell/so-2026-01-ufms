from typing import ClassVar

from schedulers.base import Scheduler
from models.process.runtime_process import RuntimeProcess


class RoundRobin(Scheduler):
    name: ClassVar[str] = "Round Robin"

    def __init__(self, quantum: int) -> None:
        if quantum <= 0:
            raise ValueError("Round Robin requires positive quantum")
        self._quantum = quantum
        self._dispatched_at = 0

    def pick_next(self, ready: list[RuntimeProcess], now: int) -> RuntimeProcess | None:
        return ready[0] if ready else None

    def on_dispatch(self, running: RuntimeProcess, now: int) -> None:
        self._dispatched_at = now

    def should_preempt(
        self,
        running: RuntimeProcess,
        ready: list[RuntimeProcess],
        now: int,
    ) -> bool:
        return now - self._dispatched_at >= self._quantum
