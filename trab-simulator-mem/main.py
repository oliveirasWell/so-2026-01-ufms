import sys
from pathlib import Path

# Permite rodar `python3 main.py` direto da pasta trab-2/ sem PYTHONPATH.
sys.path.insert(0, str(Path(__file__).parent))

from cli import parse_args
from simulador.parser import parse_input
from simulador.runner import ResultadoEvento, executar
from simulador.memoria import Memoria
from simulador.visualizacao import imprimir_estado
from simulador.relatorio import imprimir_relatorio
from simulador.algoritmos import first_fit, best_fit, worst_fit


ALGORITMOS = {
    "first-fit": first_fit.escolher,
    "best-fit": best_fit.escolher,
    "worst-fit": worst_fit.escolher,
}


def _descrever(resultado: ResultadoEvento) -> str:
    ev = resultado.evento
    if resultado.tipo == "ALOCADO":
        return (
            f"ALOC  {ev.pid}={ev.tamanho}  → alocado na brecha #{resultado.indice_brecha}"
        )
    if resultado.tipo == "LIBERADO":
        return f"LIBERA {ev.pid}  → liberado"
    if resultado.tipo == "LIBERADO_INEXISTENTE":
        return f"LIBERA {ev.pid}  → AVISO: pid inexistente (ignorado)"
    if resultado.tipo == "FALHA_FRAGMENTACAO_EXTERNA":
        return (
            f"ALOC  {ev.pid}={ev.tamanho}  → FALHA: FRAGMENTAÇÃO EXTERNA "
            f"(soma das brechas comporta, mas nenhuma individualmente)"
        )
    if resultado.tipo == "FALHA_SEM_ESPACO":
        return f"ALOC  {ev.pid}={ev.tamanho}  → FALHA: sem memória suficiente"
    return f"{ev}"


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    workload = parse_input(args.input)
    escolher = ALGORITMOS[args.algoritmo]

    print(f"# Algoritmo: {args.algoritmo}")
    print(f"# Input: {args.input}")
    print(f"# Memória total: {workload.memoria_total}")
    print(f"# Eventos: {len(workload.eventos)}")
    print()

    n = 0

    def callback(resultado: ResultadoEvento, memoria: Memoria) -> None:
        nonlocal n
        n += 1
        if args.quiet:
            return
        print(f"Evento #{n}: {_descrever(resultado)}")
        imprimir_estado(memoria)
        print()

    memoria, stats = executar(workload, escolher, on_evento=callback)
    imprimir_relatorio(memoria, stats)
    return 0


if __name__ == "__main__":
    sys.exit(main())
