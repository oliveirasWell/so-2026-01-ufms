from typing import ClassVar

from schedulers.base import Scheduler
from models.process.runtime_process import RuntimeProcess


class Priority(Scheduler):
    name: ClassVar[str] = "Priority"

    def pick_next(self, ready: list[RuntimeProcess], now: int) -> RuntimeProcess | None:
        if not ready:
            return None
        return min(ready, key=lambda rp: rp.process.priority)
