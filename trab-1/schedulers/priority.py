from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from schedulers.base import Scheduler

if TYPE_CHECKING:
    from shared.simulator import RuntimeProcess


class Priority(Scheduler):
    name: ClassVar[str] = "Priority"

    def pick_next(
        self, ready: list["RuntimeProcess"], now: int
    ) -> "RuntimeProcess | None":
        if not ready:
            return None
        best = ready[0]
        for rp in ready[1:]:
            if rp.process.priority < best.process.priority:
                best = rp
        return best
