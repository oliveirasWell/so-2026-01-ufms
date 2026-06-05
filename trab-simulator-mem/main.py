import sys
from pathlib import Path

# roda direto da pasta sem mexer no PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))

from cli import parse_args
from simulador.algoritmos.instantiate_algoritmos import ALL_KEYS
from simulador.memoria import Memoria
from simulador.parser import parse_input
from simulador.relatorio import imprimir_comparacao, imprimir_relatorio, resumo_para_snapshot
from simulador.runner import ResultadoEvento, run_simulation
from simulador.visualizacao import descrever_resultado, imprimir_estado


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv, ALL_KEYS)
    workload = parse_input(args.input)

    n = 0

    def callback(resultado: ResultadoEvento, memoria: Memoria) -> None:
        nonlocal n
        n += 1
        print(f"Evento #{n}: {descrever_resultado(resultado)}")
        imprimir_estado(memoria)
        print()

    verbose = not args.quiet and args.algoritmo is not None
    resultados = run_simulation(workload, args.algoritmo, on_evento=callback if verbose else None)

    for resultado in resultados:
        print(f"=== {resultado.algoritmo} ===")
        imprimir_relatorio(resultado.memoria, resultado.stats)
        print()

    if len(resultados) > 1:
        imprimir_comparacao(
            [(r.algoritmo, resumo_para_snapshot(r.memoria, r.stats)) for r in resultados]
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
