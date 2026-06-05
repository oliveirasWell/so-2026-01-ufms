"""Regressão por snapshot: compara `run_simulation` com `snapshots/*.json`.

Regenerar com `gerar_snapshots()` ao mudar a semântica de propósito.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from simulador.parser import parse_input
from simulador.relatorio import resumo_para_snapshot
from simulador.runner import run_simulation


_ROOT = Path(__file__).resolve().parent

_CASOS = (
    ("workload_simples", "inputs/workload_simples.json", "snapshots/workload_simples_stats.json"),
    ("workload_fragmentacao", "inputs/workload_fragmentacao.json", "snapshots/workload_fragmentacao_stats.json"),
)


def _resumos(input_rel: str) -> dict[str, dict]:
    workload = parse_input(_ROOT / input_rel)
    return {
        r.algoritmo: resumo_para_snapshot(r.memoria, r.stats)
        for r in run_simulation(workload)
    }


def _testa_snapshots() -> None:
    for nome, input_rel, snap_rel in _CASOS:
        esperado = json.loads((_ROOT / snap_rel).read_text(encoding="utf-8"))
        obtido = _resumos(input_rel)
        for algo, esperado_algo in esperado.items():
            if obtido.get(algo) != esperado_algo:
                raise AssertionError(
                    f"\n[{nome} / {algo}] divergiu:\n"
                    f"  esperado = {esperado_algo}\n"
                    f"  obtido   = {obtido.get(algo)}"
                )


def _testa_coalescing() -> None:
    # liberar tudo deve voltar a um único bloco livre do tamanho original
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


def gerar_snapshots() -> None:
    """Dev: `python3 -c "import test_simulator as t; t.gerar_snapshots()"`."""
    for _, input_rel, snap_rel in _CASOS:
        resumos = _resumos(input_rel)
        (_ROOT / snap_rel).write_text(
            json.dumps(resumos, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"escrito {snap_rel}")


def main() -> int:
    _testa_snapshots()
    _testa_coalescing()
    print("OK — snapshots (3 algoritmos × 2 workloads) + coalescing")
    return 0


if __name__ == "__main__":
    sys.exit(main())
