from models.process.runtime_process import RuntimeProcess
from models.process.workload import Workload
from models.simulation.simulation_result import SimulationResult
from models.simulation.trace.constants import IDLE_PID
from models.simulation.trace.event import Event
from models.simulation.trace.trace_entry import TraceEntry
from schedulers.base import Scheduler


class Simulator:
    def __init__(self, workload: Workload, scheduler: Scheduler):
        self.workload = workload
        self.scheduler = scheduler
        self.runtime = {
            p.pid: RuntimeProcess(process=p, cpu_remaining=p.bursts[0]) for p in workload.processes
        }
        self.not_arrived = list(workload.processes)
        self.ready: list[RuntimeProcess] = []
        self.blocked: list[RuntimeProcess] = []
        self.running: RuntimeProcess | None = None
        self.current_time = 0
        self.trace: list[TraceEntry] = []
        self.cs_cost = workload.context_switch_cost
        self.last_pid: str | None = None

    def run(self) -> SimulationResult:
        while True:
            self._handle_io_completions()
            self._handle_arrivals()
            self._handle_preemption_or_burst_end()
            self._dispatch_if_ready()

            if self.running is None:
                # finish the simulation if there are no blocked or arriving processes
                if not self.blocked and not self.not_arrived:
                    break

                # if there are no blocked or arriving processes, idle the CPU
                self._idle_tick()
                continue

            self._advance_running_tick()

        return SimulationResult(
            algorithm=self.scheduler.name,
            workload=self.workload,
            trace=tuple(self.trace),
        )

    def _dispatch_if_ready(self) -> None:
        if self.running is None and self.ready:
            self._dispatch()

    def _advance_running_tick(self) -> None:
        assert self.running is not None

        # advance the running process by 1 tick
        # decrement the CPU remaining time
        # useful for the scheduler to know when to preempt the process
        self.running.cpu_remaining -= 1
        self._tick_blocked_io()
        self.current_time += 1

    def _emit(self, event: Event, pid: str) -> None:
        self.trace.append(
            TraceEntry(
                time=self.current_time,
                event=event,
                pid=pid,
                ready_queue=tuple(ready_proc.pid for ready_proc in self.ready),
                blocked=tuple(blocked_proc.pid for blocked_proc in self.blocked),
                running=self.running.pid if self.running else None,
            )
        )

    def _handle_io_completions(self) -> None:
        io_finished = sorted(
            [blocked_proc for blocked_proc in self.blocked if blocked_proc.io_remaining == 0],
            key=lambda blocked_proc: blocked_proc.pid,
        )
        for blocked_proc in io_finished:
            self.blocked.remove(blocked_proc)
            self.ready.append(blocked_proc)
            self._emit(Event.IO_DONE, blocked_proc.pid)

    def _handle_arrivals(self) -> None:
        arriving = [p for p in self.not_arrived if p.arrival == self.current_time]
        for p in arriving:
            self.not_arrived.remove(p)
            self.ready.append(self.runtime[p.pid])
            self._emit(Event.ARRIVAL, p.pid)

    def _handle_preemption_or_burst_end(self) -> None:
        running = self.running
        if running is None:
            return

        # handle burst end
        if running.cpu_remaining == 0:
            # burst_index + 2 because the bursts are in the format [CPU, IO, CPU, ...]
            next_idx = running.burst_index + 2
            # if there are more bursts, add the next burst to the blocked queue
            if next_idx < len(running.process.bursts):
                running.io_remaining = running.process.bursts[running.burst_index + 1]
                running.burst_index = next_idx
                running.cpu_remaining = running.process.bursts[next_idx]
                self.blocked.append(running)
                self.running = None
                self._emit(Event.CPU_BURST_END, running.pid)
            else:
                # if there are no more bursts, terminate the process
                running.finish = self.current_time
                self.running = None
                self._emit(Event.TERMINATE, running.pid)

            return

        if self.scheduler.should_preempt(running, self.ready, self.current_time):
            self.ready.append(running)
            self.running = None
            self._emit(Event.PREEMPT, running.pid)

    def _dispatch(self) -> None:
        next_proc = self.scheduler.pick_next(self.ready, self.current_time)
        if next_proc is None:
            raise RuntimeError("scheduler returned no candidate from non-empty ready queue")
        self.ready.remove(next_proc)
        self._apply_context_switch_cost(next_proc.pid)
        self.running = next_proc
        self.last_pid = next_proc.pid
        self.scheduler.on_dispatch(next_proc, self.current_time)
        self._emit(Event.DISPATCH, next_proc.pid)

    def _apply_context_switch_cost(self, next_pid: str) -> None:
        # if the context switch cost is 0 or the last process is the same as the next process, do not apply the context switch cost
        if self.cs_cost <= 0 or self.last_pid is None or self.last_pid == next_pid:
            return

        self._emit(Event.CONTEXT_SWITCH, next_pid)

        for _ in range(self.cs_cost):
            self._tick_blocked_io()
            self.current_time += 1
            self._handle_io_completions()
            self._handle_arrivals()

    def _tick_blocked_io(self) -> None:
        for blocked_proc in self.blocked:
            if blocked_proc.io_remaining > 0:
                blocked_proc.io_remaining -= 1

    def _idle_tick(self) -> None:
        self._emit(Event.IDLE, IDLE_PID)
        self._tick_blocked_io()
        self.current_time += 1
