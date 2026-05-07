from dataclasses import dataclass, field
from enum import StrEnum

from schedulers.base import Scheduler
from shared.process import Process, Workload

IDLE_PID = "IDLE"
CS_PID = "CS"


class Event(StrEnum):
    ARRIVAL = "ARRIVAL"
    DISPATCH = "DISPATCH"
    PREEMPT = "PREEMPT"
    CPU_BURST_END = "CPU_BURST_END"
    IO_DONE = "IO_DONE"
    CONTEXT_SWITCH = "CONTEXT_SWITCH"
    TERMINATE = "TERMINATE"


@dataclass(frozen=True)
class TraceEntry:
    time: int
    event: Event
    pid: str | None
    ready_queue: tuple[str, ...]
    blocked: tuple[str, ...]
    running: str | None


@dataclass(frozen=True)
class GanttSlice:
    pid: str
    start: int
    end: int


@dataclass(frozen=True)
class SimulationResult:
    algorithm: str
    workload: Workload
    gantt: tuple[GanttSlice, ...]
    trace: tuple[TraceEntry, ...]


@dataclass
class RuntimeProcess:
    process: Process
    burst_index: int = 0
    cpu_remaining: int = 0
    io_remaining: int = 0
    first_dispatch: int | None = None
    finish: int | None = None

    @property
    def pid(self) -> str:
        return self.process.pid


@dataclass
class _State:
    t: int
    gantt: list[GanttSlice]
    trace: list[TraceEntry] = field(default_factory=list)


def run(workload: Workload, scheduler: Scheduler) -> SimulationResult:
    runtime = {p.pid: RuntimeProcess(process=p, cpu_remaining=p.bursts[0]) for p in workload.processes}
    not_arrived = list(workload.processes)
    ready: list[RuntimeProcess] = []
    blocked: list[RuntimeProcess] = []
    running: RuntimeProcess | None = None
    quantum_used = 0
    cs_cost = workload.context_switch_cost
    last_pid: str | None = None
    quantum = scheduler.quantum()

    state = _State(t=0, gantt=[])

    while True:
        _handle_io_completions(state, blocked, ready, running)
        _handle_arrivals(state, not_arrived, ready, blocked, running, runtime)

        running, quantum_used = _handle_preemption_or_burst_end(
            state, running, ready, blocked, scheduler, quantum, quantum_used
        )

        if running is None and ready:
            running, quantum_used, last_pid = _dispatch(
                state, ready, blocked, not_arrived, runtime, scheduler, cs_cost, last_pid
            )

        if running is None:
            if not blocked and not not_arrived:
                break
            _idle_tick(state, blocked)
            continue

        _add_slice(state.gantt, running.pid, state.t, state.t + 1)
        running.cpu_remaining -= 1
        quantum_used += 1
        for rp in blocked:
            if rp.io_remaining > 0:
                rp.io_remaining -= 1
        state.t += 1

    return SimulationResult(
        algorithm=scheduler.name,
        workload=workload,
        gantt=tuple(state.gantt),
        trace=tuple(state.trace),
    )


def _emit(
    state: _State,
    event: Event,
    pid: str | None,
    ready: list[RuntimeProcess],
    blocked: list[RuntimeProcess],
    running: RuntimeProcess | None,
) -> None:
    state.trace.append(
        TraceEntry(
            time=state.t,
            event=event,
            pid=pid,
            ready_queue=tuple(rp.pid for rp in ready),
            blocked=tuple(rp.pid for rp in blocked),
            running=running.pid if running else None,
        )
    )


def _add_slice(gantt: list[GanttSlice], pid: str, start: int, end: int) -> None:
    if start >= end:
        return
    if gantt and gantt[-1].pid == pid and gantt[-1].end == start:
        gantt[-1] = GanttSlice(pid=pid, start=gantt[-1].start, end=end)
        return
    gantt.append(GanttSlice(pid=pid, start=start, end=end))


def _handle_io_completions(
    state: _State,
    blocked: list[RuntimeProcess],
    ready: list[RuntimeProcess],
    running: RuntimeProcess | None,
) -> None:
    completed = sorted([rp for rp in blocked if rp.io_remaining == 0], key=lambda rp: rp.pid)
    for rp in completed:
        blocked.remove(rp)
        ready.append(rp)
        _emit(state, Event.IO_DONE, rp.pid, ready, blocked, running)


def _handle_arrivals(
    state: _State,
    not_arrived: list[Process],
    ready: list[RuntimeProcess],
    blocked: list[RuntimeProcess],
    running: RuntimeProcess | None,
    runtime: dict[str, RuntimeProcess],
) -> None:
    arriving = [p for p in not_arrived if p.arrival == state.t]
    for p in arriving:
        not_arrived.remove(p)
        ready.append(runtime[p.pid])
        _emit(state, Event.ARRIVAL, p.pid, ready, blocked, running)


def _handle_preemption_or_burst_end(
    state: _State,
    running: RuntimeProcess | None,
    ready: list[RuntimeProcess],
    blocked: list[RuntimeProcess],
    scheduler: Scheduler,
    quantum: int | None,
    quantum_used: int,
) -> tuple[RuntimeProcess | None, int]:
    if running is None:
        return None, 0

    if running.cpu_remaining == 0:
        next_idx = running.burst_index + 2
        if next_idx < len(running.process.bursts):
            running.io_remaining = running.process.bursts[running.burst_index + 1]
            running.burst_index = next_idx
            running.cpu_remaining = running.process.bursts[next_idx]
            blocked.append(running)
            _emit(state, Event.CPU_BURST_END, running.pid, ready, blocked, None)
        else:
            running.finish = state.t
            _emit(state, Event.TERMINATE, running.pid, ready, blocked, None)
        return None, 0

    if quantum is not None and quantum_used >= quantum:
        ready.append(running)
        _emit(state, Event.PREEMPT, running.pid, ready, blocked, None)
        return None, 0

    if scheduler.is_preemptive() and scheduler.should_preempt(running, ready, state.t):
        ready.append(running)
        _emit(state, Event.PREEMPT, running.pid, ready, blocked, None)
        return None, 0

    return running, quantum_used


def _dispatch(
    state: _State,
    ready: list[RuntimeProcess],
    blocked: list[RuntimeProcess],
    not_arrived: list[Process],
    runtime: dict[str, RuntimeProcess],
    scheduler: Scheduler,
    cs_cost: int,
    last_pid: str | None,
) -> tuple[RuntimeProcess, int, str]:
    next_rp = scheduler.pick_next(ready, state.t)
    if next_rp is None:
        raise RuntimeError("scheduler returned no candidate from non-empty ready queue")
    ready.remove(next_rp)

    if cs_cost > 0 and last_pid is not None and last_pid != next_rp.pid:
        cs_start = state.t
        _emit(state, Event.CONTEXT_SWITCH, next_rp.pid, ready, blocked, None)
        for _ in range(cs_cost):
            for rp in blocked:
                if rp.io_remaining > 0:
                    rp.io_remaining -= 1
            state.t += 1
            _handle_io_completions(state, blocked, ready, None)
            _handle_arrivals(state, not_arrived, ready, blocked, None, runtime)
        _add_slice(state.gantt, CS_PID, cs_start, state.t)

    if next_rp.first_dispatch is None:
        next_rp.first_dispatch = state.t
    _emit(state, Event.DISPATCH, next_rp.pid, ready, blocked, next_rp)
    return next_rp, 0, next_rp.pid


def _idle_tick(state: _State, blocked: list[RuntimeProcess]) -> None:
    _add_slice(state.gantt, IDLE_PID, state.t, state.t + 1)
    for rp in blocked:
        if rp.io_remaining > 0:
            rp.io_remaining -= 1
    state.t += 1
