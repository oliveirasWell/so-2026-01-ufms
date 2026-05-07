from typing import ClassVar

from schedulers.base import Scheduler
from shared.runtime_process import RuntimeProcess


class Priority(Scheduler):
    name: ClassVar[str] = "Priority"

    def pick_next(self, ready: list[RuntimeProcess], now: int) -> RuntimeProcess | None:
        if not ready:
            return None
        best = ready[0]
        for rp in ready[1:]:
            if rp.process.priority < best.process.priority:
                best = rp
        return best
