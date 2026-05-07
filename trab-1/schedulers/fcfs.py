from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from schedulers.base import Scheduler

if TYPE_CHECKING:
    from shared.simulator import RuntimeProcess


class FCFS(Scheduler):
    name: ClassVar[str] = "FCFS"

    def pick_next(
        self, ready: list["RuntimeProcess"], now: int
    ) -> "RuntimeProcess | None":
        return ready[0] if ready else None
