"""Best Fit (Melhor-Apto).

Examina TODAS as brechas e devolve o índice daquela que produz a menor
sobra (`brecha.tamanho - tamanho`). Empate: vence a brecha mais à esquerda
(primeira encontrada), conforme convenção documentada no spec.
"""

from __future__ import annotations

from simulador.memoria import Memoria


def escolher(memoria: Memoria, tamanho: int) -> int | None:
    melhor_indice: int | None = None
    menor_sobra: int | None = None
    for indice, bloco in memoria.brechas():
        if bloco.tamanho < tamanho:
            continue
        sobra = bloco.tamanho - tamanho
        if menor_sobra is None or sobra < menor_sobra:
            menor_sobra = sobra
            melhor_indice = indice
    return melhor_indice
