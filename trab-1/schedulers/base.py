from abc import ABC, abstractmethod
from typing import ClassVar

from models.process.runtime_process import RuntimeProcess


class Scheduler(ABC):
    name: ClassVar[str]

    @abstractmethod
    def pick_next(self, ready: list[RuntimeProcess], now: int) -> RuntimeProcess | None: ...

    def on_dispatch(self, running: RuntimeProcess, now: int) -> None:
        """Hook fired right after a process is dispatched. Override to track per-dispatch state."""

    def should_preempt(
        self,
        running: RuntimeProcess,
        ready: list[RuntimeProcess],
        now: int,
    ) -> bool:
        return False
