"""Teste de regressao: roda os 3 algoritmos sobre os workloads de exemplo
e confere que as contagens do relatorio batem com o esperado.

Sem dependencias externas — basta `python3 test_simulator.py` a partir
de `trab-2/`. Encerra com codigo != 0 se algo divergir.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from simulador.parser import parse_input
from simulador.runner import executar
from simulador.algoritmos import first_fit, best_fit, worst_fit


_ROOT = Path(__file__).resolve().parent
ALGORITMOS = {
    "first-fit": first_fit.escolher,
    "best-fit": best_fit.escolher,
    "worst-fit": worst_fit.escolher,
}


def _resumo(stats) -> dict:
    return {
        "alocados": stats.alocados,
        "liberados": stats.liberados,
        "liberados_inexistentes": stats.liberados_inexistentes,
        "falhas_fragmentacao_externa": stats.falhas_fragmentacao_externa,
        "falhas_sem_espaco": stats.falhas_sem_espaco,
    }


def _assert_eq(esperado: dict, obtido: dict, contexto: str) -> None:
    if esperado != obtido:
        raise AssertionError(
            f"\n[{contexto}] divergiu:\n  esperado = {esperado}\n  obtido   = {obtido}"
        )


def _testa_workload_simples() -> None:
    # 7 eventos, 5 ALOC, 2 LIBERA — todos cabem em qualquer estratégia.
    workload = parse_input(_ROOT / "inputs" / "workload_simples.json")
    esperado = {
        "alocados": 5,
        "liberados": 2,
        "liberados_inexistentes": 0,
        "falhas_fragmentacao_externa": 0,
        "falhas_sem_espaco": 0,
    }
    for nome, escolher in ALGORITMOS.items():
        _, stats = executar(workload, escolher)
        _assert_eq(esperado, _resumo(stats), f"workload_simples / {nome}")


def _testa_workload_fragmentacao() -> None:
    # 10 eventos. Independente do algoritmo, a configuração final é:
    # 5 alocados, 2 liberados, 1 LIBERA pid inexistente, 1 falha
    # por fragmentação externa, 1 falha por falta de memória.
    workload = parse_input(_ROOT / "inputs" / "workload_fragmentacao.json")
    esperado = {
        "alocados": 5,
        "liberados": 2,
        "liberados_inexistentes": 1,
        "falhas_fragmentacao_externa": 1,
        "falhas_sem_espaco": 1,
    }
    for nome, escolher in ALGORITMOS.items():
        _, stats = executar(workload, escolher)
        _assert_eq(esperado, _resumo(stats), f"workload_fragmentacao / {nome}")


def _testa_coalescing() -> None:
    # Verifica que liberar todos os processos faz a memoria voltar a um
    # unico bloco livre do tamanho original (invariante de coalescing).
    from simulador.memoria import Memoria

    m = Memoria(1000)
    m.alocar("P1", 300, 0)
    m.alocar("P2", 200, 1)
    m.alocar("P3", 100, 2)
    m.liberar("P2")
    m.liberar("P1")
    m.liberar("P3")
    if len(m.blocos) != 1 or m.blocos[0].tamanho != 1000 or not m.blocos[0].livre:
        raise AssertionError(
            f"coalescing falhou: esperado [livre:1000], obtido {m.blocos}"
        )


def main() -> int:
    _testa_workload_simples()
    _testa_workload_fragmentacao()
    _testa_coalescing()
    print("OK — 3 algoritmos x 2 workloads + coalescing")
    return 0


if __name__ == "__main__":
    sys.exit(main())
