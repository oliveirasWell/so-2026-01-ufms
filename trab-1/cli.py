import argparse
from collections.abc import Iterable
from pathlib import Path


def parse_args(argv: list[str] | None, algo_choices: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CPU scheduling simulator")
    parser.add_argument("--algo", choices=tuple(algo_choices), default=None)
    parser.add_argument("--trace", action="store_true")
    parser.add_argument("--input", type=Path, default=Path("inputs/workload.json"))
    return parser.parse_args(argv)
