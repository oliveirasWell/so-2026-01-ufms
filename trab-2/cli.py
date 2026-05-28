import argparse
from pathlib import Path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Simulador de alocação dinâmica de memória "
        "(First Fit, Best Fit, Worst Fit) — UFMS SO 2026."
    )
    parser.add_argument(
        "--algoritmo",
        required=True,
        choices=("first-fit", "best-fit", "worst-fit"),
        help="Algoritmo de alocação a usar.",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("inputs/workload.json"),
        help="Arquivo JSON de entrada (default: inputs/workload.json).",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suprime impressão do estado após cada evento; mostra só o relatório final.",
    )
    return parser.parse_args(argv)
