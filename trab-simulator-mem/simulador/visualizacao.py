"""Impressão textual do estado da memória.

Cada chamada a `imprimir_estado` mostra três visões do mesmo instante:

1. Partições ocupadas — uma linha por bloco com pid e intervalo.
2. Brechas — uma linha por espaço livre.
3. Barra ASCII compacta — layout proporcional da memória inteira numa
   única linha, útil para enxergar fragmentação de relance.
"""

from __future__ import annotations

from simulador.memoria import Memoria


def imprimir_estado(memoria: Memoria, largura_barra: int = 60) -> None:
    print("  Partições ocupadas:")
    ocupadas = [b for b in memoria.blocos if not b.livre]
    if not ocupadas:
        print("    (nenhuma)")
    else:
        for b in ocupadas:
            print(f"    [{b.inicio:>5}–{b.fim - 1:>5}] {b.pid:<6} tam={b.tamanho}")

    print("  Brechas:")
    livres = [b for b in memoria.blocos if b.livre]
    if not livres:
        print("    (nenhuma)")
    else:
        for b in livres:
            print(f"    [{b.inicio:>5}–{b.fim - 1:>5}] LIVRE  tam={b.tamanho}")

    print(f"  Layout: {_barra_ascii(memoria, largura_barra)}")


def _barra_ascii(memoria: Memoria, largura: int) -> str:
    """Renderiza a memória inteira numa barra de `largura` caracteres."""
    total = memoria.tamanho_total
    partes: list[str] = []
    for b in memoria.blocos:
        # Garante pelo menos 1 caractere por bloco para não sumir blocos pequenos.
        n = max(1, round(b.tamanho / total * largura))
        # Para brechas usa '.', para ocupados usa o último caractere do pid
        # (com "P1"/"P2"/etc. vira "1"/"2"/etc., legível em workloads didáticos).
        rotulo = "." if b.livre else b.pid[-1]
        partes.append(rotulo * n)
    return "|" + "|".join(partes) + "|"
