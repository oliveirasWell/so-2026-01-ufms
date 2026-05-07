from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from cli import parse_args
from schedulers.base import Scheduler
from schedulers.fcfs import FCFS
from schedulers.priority import Priority
from schedulers.round_robin import RoundRobin
from schedulers.sjf import SJF
from shared.comparison import pick_winners, run_all
from shared.metrics import compute_metrics
from shared.parser import parse_input
from shared.process import Workload
from shared.reporter import print_comparison, print_metrics, print_trace
from shared.simulator import run


def _build_round_robin(workload: Workload) -> Scheduler:
    if workload.quantum is None:
        raise SystemExit("round-robin requires 'quantum=' header in workload")
    return RoundRobin(workload.quantum)


_SCHEDULER_FACTORIES: dict[str, Callable[[Workload], Scheduler]] = {
    "fcfs": lambda _w: FCFS(),
    "sjf": lambda _w: SJF(preemptive=False),
    "sjf-preemptive": lambda _w: SJF(preemptive=True),
    "priority": lambda _w: Priority(),
    "round-robin": _build_round_robin,
}


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv, _SCHEDULER_FACTORIES)

    workload_path = args.input or (Path(__file__).parent / "inputs" / "workload.txt")
    workload = parse_input(workload_path)

    if args.algo is None:
        _run_comparison(workload, show_trace=args.trace)
        return 0

    scheduler = _SCHEDULER_FACTORIES[args.algo](workload)
    result = run(workload, scheduler)
    report = compute_metrics(result)
    print_metrics(report)
    if args.trace:
        print_trace(result)
    return 0


def _run_comparison(workload: Workload, show_trace: bool) -> None:
    pairs = run_all(workload)
    reports = [m for _, m in pairs]
    print_comparison(reports, pick_winners(reports))
    if show_trace:
        for result, _ in pairs:
            print()
            print_trace(result)


if __name__ == "__main__":
    sys.exit(main())
