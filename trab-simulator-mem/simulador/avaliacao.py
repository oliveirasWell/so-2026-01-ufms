"""Vencedor por métrica: menos falhas/rejeições e mais utilização.

Empate: vence o primeiro algoritmo na ordem de inserção.
"""

from __future__ import annotations

MENOR_E_MELHOR = (
    "falhas_fragmentacao_externa",
    "falhas_sem_espaco",
    "rejeitados_total",
)
MAIOR_E_MELHOR = ("utilizacao_final_pct",)


def _valor(resumo: dict, metrica: str) -> float:
    if metrica == "rejeitados_total":
        return resumo["falhas_fragmentacao_externa"] + resumo["falhas_sem_espaco"]
    return resumo[metrica]


def pick_winners(relatorios: dict[str, dict]) -> dict[str, str]:
    """`rejeitados_total` é derivado da soma das duas categorias de falha."""
    if not relatorios:
        return {}
    itens = list(relatorios.items())
    vencedores: dict[str, str] = {}
    for metrica in MENOR_E_MELHOR:
        vencedores[metrica] = min(itens, key=lambda kv: _valor(kv[1], metrica))[0]
    for metrica in MAIOR_E_MELHOR:
        vencedores[metrica] = max(itens, key=lambda kv: _valor(kv[1], metrica))[0]
    return vencedores
