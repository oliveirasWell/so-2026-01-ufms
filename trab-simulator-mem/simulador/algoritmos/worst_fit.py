"""Worst Fit (Pior-Apto).

Examina TODAS as brechas e devolve o índice da MAIOR brecha (que serve).
Empate: vence a brecha mais à esquerda (primeira encontrada), conforme
convenção documentada no spec. A ideia é deixar a sobra a maior possível
para outros processos.
"""

from __future__ import annotations

from simulador.memoria import Memoria


def escolher(memoria: Memoria, tamanho: int) -> int | None:
    pior_indice: int | None = None
    maior_tamanho: int | None = None
    for indice, bloco in memoria.brechas():
        if bloco.tamanho < tamanho:
            continue
        if maior_tamanho is None or bloco.tamanho > maior_tamanho:
            maior_tamanho = bloco.tamanho
            pior_indice = indice
    return pior_indice
