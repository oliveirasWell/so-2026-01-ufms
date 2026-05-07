from typing import ClassVar

from schedulers.base import Scheduler
from shared.runtime_process import RuntimeProcess


class FCFS(Scheduler):
    name: ClassVar[str] = "FCFS"

    def pick_next(self, ready: list[RuntimeProcess], now: int) -> RuntimeProcess | None:
        return ready[0] if ready else None
