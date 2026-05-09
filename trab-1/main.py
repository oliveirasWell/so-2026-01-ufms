import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from cli import parse_args
from models.process.workload import Workload
from schedulers.registry import SCHEDULER_FACTORIES
from shared.comparison import pick_winners, run_all
from shared.metrics import compute_metrics
from shared.parser import parse_input
from shared.reporter import print_comparison, print_metrics, print_trace
from shared.simulator import Simulator


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv, SCHEDULER_FACTORIES)

    workload_path = args.input or (Path(__file__).parent / "inputs" / "workload.txt")
    workload = parse_input(workload_path)

    if args.algo is None:
        _run_comparison(workload, show_trace=args.trace)
        return 0

    scheduler = SCHEDULER_FACTORIES[args.algo](workload)
    result = Simulator(workload, scheduler).run()
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
