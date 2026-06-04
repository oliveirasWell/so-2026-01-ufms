"""First Fit (Primeiro-Apto).

Percorre a memória do início para o fim e devolve o índice da PRIMEIRA
brecha cujo tamanho é suficiente. Se nenhuma serve, devolve None.
"""

from __future__ import annotations

from simulador.memoria import Memoria


def escolher(memoria: Memoria, tamanho: int) -> int | None:
    for indice, bloco in memoria.brechas():
        if bloco.tamanho >= tamanho:
            return indice
    return None
