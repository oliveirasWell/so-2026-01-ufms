import sys
from pathlib import Path

# run straight from the folder without touching PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))

from cli import parse_args
from simulator.algorithms.instantiate_algorithms import ALL_KEYS
from simulator.memory import Memory
from simulator.parser import parse_input
from simulator.report import print_comparison, print_report, snapshot_summary
from simulator.runner import EventResult, run_simulation
from simulator.visualization import describe_result, print_state


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv, ALL_KEYS)
    workload = parse_input(args.input)

    n = 0

    def callback(result: EventResult, memory: Memory) -> None:
        nonlocal n
        n += 1
        print(f"Evento #{n}: {describe_result(result)}")
        print_state(memory)
        print()

    verbose = not args.quiet and args.algorithm is not None
    results = run_simulation(workload, args.algorithm, on_event=callback if verbose else None)

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
