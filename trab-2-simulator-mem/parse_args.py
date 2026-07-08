import argparse
from collections.abc import Iterable
from pathlib import Path


def parse_args(argv: list[str] | None, algo_choices: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Simulador de alocação dinâmica de memória "
        "(First Fit, Best Fit, Worst Fit)."
    )
    parser.add_argument(
        "--algorithm",
        default=None,
        choices=tuple(algo_choices),
        help="Algoritmo de alocação. Omita para rodar os três e comparar.",
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
    parser.add_argument(
        "--layout",
        action="store_true",
        help="Exibe a barra ASCII do layout da memória após cada evento.",
    )
    return parser.parse_args(argv)
