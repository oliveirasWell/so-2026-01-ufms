from models.simulation.constants import CS_PID, IDLE_PID
from models.simulation.event import Event
from models.simulation.gantt_slice import GanttSlice
from models.simulation.simulation_result import SimulationResult


def build_gantt(result: SimulationResult) -> tuple[GanttSlice, ...]:
    slices: list[GanttSlice] = []
    cs_cost = result.workload.context_switch_cost

    proc_pid: str | None = None
    proc_start: int | None = None

    for entry in result.trace:
        if entry.event == Event.DISPATCH:
            proc_pid = entry.pid
            proc_start = entry.time
        elif entry.event in (Event.PREEMPT, Event.CPU_BURST_END, Event.TERMINATE):
            if proc_pid is not None and proc_start is not None:
                _push(slices, proc_pid, proc_start, entry.time)
            proc_pid = None
            proc_start = None
        elif entry.event == Event.IDLE:
            _push(slices, IDLE_PID, entry.time, entry.time + 1)
        elif entry.event == Event.CONTEXT_SWITCH:
            _push(slices, CS_PID, entry.time, entry.time + cs_cost)

    return tuple(slices)


def _push(slices: list[GanttSlice], pid: str, start: int, end: int) -> None:
    if start >= end:
        return
    if slices and slices[-1].pid == pid and slices[-1].end == start:
        slices[-1] = GanttSlice(pid=pid, start=slices[-1].start, end=end)
        return
    slices.append(GanttSlice(pid=pid, start=start, end=end))
