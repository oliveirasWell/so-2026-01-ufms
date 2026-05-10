import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from cli import parse_args
from schedulers.instantiate_schedulers import SCHEDULER_FACTORIES
from shared.runner import run_simulation
from shared.parser import parse_input
from shared.reporter import print_reports, print_trace


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv, SCHEDULER_FACTORIES)

    workload = parse_input(args.input)

    results, _, reports = run_simulation(workload, args.algo)

    print_reports(reports)

    if args.trace:
        for result in results:
            print()
            print_trace(result)

    return 0


if __name__ == "__main__":
    sys.exit(main())
