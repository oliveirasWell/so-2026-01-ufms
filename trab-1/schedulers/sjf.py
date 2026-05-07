from schedulers.base import Scheduler
from shared.runtime_process import RuntimeProcess


class SJF(Scheduler):
    def __init__(self, preemptive: bool) -> None:
        self._preemptive = preemptive
        self.name = "SJF (preemptive)" if preemptive else "SJF"

    def pick_next(self, ready: list[RuntimeProcess], now: int) -> RuntimeProcess | None:
        if not ready:
            return None
        return min(ready, key=self._sort_key)

    def is_preemptive(self) -> bool:
        return self._preemptive

    def should_preempt(
        self,
        running: RuntimeProcess,
        ready: list[RuntimeProcess],
        now: int,
    ) -> bool:
        if not self._preemptive or not ready:
            return False
        candidate = min(ready, key=self._sort_key)
        return candidate.cpu_remaining < running.cpu_remaining

    @staticmethod
    def _sort_key(rp: RuntimeProcess) -> tuple[int, int, str]:
        return (rp.cpu_remaining, rp.process.arrival, rp.process.pid)
