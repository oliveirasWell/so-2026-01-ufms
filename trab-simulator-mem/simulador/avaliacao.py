"""Escolha do "vencedor" por métrica entre os algoritmos.

Espelha `trab-1/shared/evaluation.pick_winners`, adaptado às métricas de
alocação de memória. Recebe os resumos (saída de
`relatorio.resumo_para_snapshot`) de cada algoritmo e devolve, por métrica,
qual algoritmo se saiu melhor.

Para falhas e rejeições, MENOR é melhor; para utilização final, MAIOR é
melhor. Empates: vence o primeiro algoritmo na ordem de inserção.
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
    """Mapeia métrica -> nome do algoritmo vencedor.

    `relatorios` é `{nome_algoritmo: resumo}` (resumo = resumo_para_snapshot).
    `rejeitados_total` é derivado da soma das duas categorias de falha.
    """
    if not relatorios:
        return {}
    itens = list(relatorios.items())
    vencedores: dict[str, str] = {}
    for metrica in MENOR_E_MELHOR:
        vencedores[metrica] = min(itens, key=lambda kv: _valor(kv[1], metrica))[0]
    for metrica in MAIOR_E_MELHOR:
        vencedores[metrica] = max(itens, key=lambda kv: _valor(kv[1], metrica))[0]
    return vencedores
