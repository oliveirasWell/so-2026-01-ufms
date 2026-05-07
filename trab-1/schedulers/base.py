from abc import ABC, abstractmethod
from typing import ClassVar

from shared.runtime_process import RuntimeProcess


class Scheduler(ABC):
    name: ClassVar[str]

    @abstractmethod
    def pick_next(self, ready: list[RuntimeProcess], now: int) -> RuntimeProcess | None: ...

    def is_preemptive(self) -> bool:
        return False

    def quantum(self) -> int | None:
        return None

    def should_preempt(
        self,
        running: RuntimeProcess,
        ready: list[RuntimeProcess],
        now: int,
    ) -> bool:
        return False
