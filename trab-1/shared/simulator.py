from models.process.runtime_process import RuntimeProcess
from models.process.workload import Workload
from models.simulation.constants import CS_PID, IDLE_PID
from models.simulation.event import Event
from models.simulation.gantt_slice import GanttSlice
from models.simulation.simulation_result import SimulationResult
from models.simulation.trace_entry import TraceEntry
from schedulers.base import Scheduler


class Simulator:
    def __init__(self, workload: Workload, scheduler: Scheduler):
        self.workload = workload
        self.scheduler = scheduler
        self.runtime = {
            p.pid: RuntimeProcess(process=p, cpu_remaining=p.bursts[0])
            for p in workload.processes
        }
        self.not_arrived = list(workload.processes)
        self.ready: list[RuntimeProcess] = []
        self.blocked: list[RuntimeProcess] = []
        self.running: RuntimeProcess | None = None
        self.t = 0
        self.gantt: list[GanttSlice] = []
        self.trace: list[TraceEntry] = []
        self.cs_cost = workload.context_switch_cost
        self.last_pid: str | None = None

    def run(self) -> SimulationResult:
        while True:
            self._handle_io_completions()
            self._handle_arrivals()
            self._handle_preemption_or_burst_end()

            if self.running is None and self.ready:
                self._dispatch()

            if self.running is None:
                if not self.blocked and not self.not_arrived:
                    break
                self._idle_tick()
                continue

            self._add_slice(self.running.pid, self.t, self.t + 1)
            self.running.cpu_remaining -= 1
            self._tick_blocked_io()
            self.t += 1

        return SimulationResult(
            algorithm=self.scheduler.name,
            workload=self.workload,
            gantt=tuple(self.gantt),
            trace=tuple(self.trace),
        )

    def _emit(self, event: Event, pid: str | None) -> None:
        self.trace.append(
            TraceEntry(
                time=self.t,
                event=event,
                pid=pid,
                ready_queue=tuple(rp.pid for rp in self.ready),
                blocked=tuple(rp.pid for rp in self.blocked),
                running=self.running.pid if self.running else None,
            )
        )

    def _add_slice(self, pid: str, start: int, end: int) -> None:
        if start >= end:
            return
        if self.gantt and self.gantt[-1].pid == pid and self.gantt[-1].end == start:
            self.gantt[-1] = GanttSlice(pid=pid, start=self.gantt[-1].start, end=end)
            return
        self.gantt.append(GanttSlice(pid=pid, start=start, end=end))

    def _handle_io_completions(self) -> None:
        completed = sorted(
            [rp for rp in self.blocked if rp.io_remaining == 0],
            key=lambda rp: rp.pid,
        )
        for rp in completed:
            self.blocked.remove(rp)
            self.ready.append(rp)
            self._emit(Event.IO_DONE, rp.pid)

    def _handle_arrivals(self) -> None:
        arriving = [p for p in self.not_arrived if p.arrival == self.t]
        for p in arriving:
            self.not_arrived.remove(p)
            self.ready.append(self.runtime[p.pid])
            self._emit(Event.ARRIVAL, p.pid)

    def _handle_preemption_or_burst_end(self) -> None:
        running = self.running
        if running is None:
            return

        if running.cpu_remaining == 0:
            next_idx = running.burst_index + 2
            if next_idx < len(running.process.bursts):
                running.io_remaining = running.process.bursts[running.burst_index + 1]
                running.burst_index = next_idx
                running.cpu_remaining = running.process.bursts[next_idx]
                self.blocked.append(running)
                self.running = None
                self._emit(Event.CPU_BURST_END, running.pid)
            else:
                running.finish = self.t
                self.running = None
                self._emit(Event.TERMINATE, running.pid)
            return

        if self.scheduler.should_preempt(running, self.ready, self.t):
            self.ready.append(running)
            self.running = None
            self._emit(Event.PREEMPT, running.pid)

    def _dispatch(self) -> None:
        next_rp = self.scheduler.pick_next(self.ready, self.t)
        if next_rp is None:
            raise RuntimeError("scheduler returned no candidate from non-empty ready queue")
        self.ready.remove(next_rp)
        self._apply_context_switch_cost(next_rp.pid)

        if next_rp.first_dispatch is None:
            next_rp.first_dispatch = self.t
        self.running = next_rp
        self.last_pid = next_rp.pid
        self.scheduler.on_dispatch(next_rp, self.t)
        self._emit(Event.DISPATCH, next_rp.pid)

    def _apply_context_switch_cost(self, next_pid: str) -> None:
        if self.cs_cost <= 0 or self.last_pid is None or self.last_pid == next_pid:
            return

        cs_start = self.t
        self._emit(Event.CONTEXT_SWITCH, next_pid)

        for _ in range(self.cs_cost):
            self._tick_blocked_io()
            self.t += 1
            self._handle_io_completions()
            self._handle_arrivals()

        self._add_slice(CS_PID, cs_start, self.t)

    def _tick_blocked_io(self) -> None:
        for rp in self.blocked:
            if rp.io_remaining > 0:
                rp.io_remaining -= 1

    def _idle_tick(self) -> None:
        self._add_slice(IDLE_PID, self.t, self.t + 1)
        self._tick_blocked_io()
        self.t += 1
