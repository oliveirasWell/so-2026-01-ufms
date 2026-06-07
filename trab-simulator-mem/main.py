import sys
from pathlib import Path

# run straight from the folder without touching PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))

from algorithms.instantiate_algorithms import ALL_KEYS
from parse_args import parse_args
from shared.parser import parse_input
from shared.report import print_comparison, print_report, snapshot_summary
from shared.runner import run_simulation


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv, ALL_KEYS)
    workload = parse_input(args.input)

    verbose = not args.quiet and args.algorithm is not None
    results = run_simulation(
        workload, args.algorithm, verbose=verbose, show_layout=args.layout
    )

    for result in results:
        print(f"=== {result.algorithm} ===")
        print_report(result.memory, result.stats)
        print()

    if len(results) > 1:
        print_comparison(
            [(r.algorithm, snapshot_summary(r.memory, r.stats)) for r in results]
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
