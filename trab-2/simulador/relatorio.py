"""Relatório final da simulação.

O enunciado exige reportar "utilização da memória" e "número de processos
que não puderam ser alocados por falta de espaço contíguo". Reportamos
esses dois e algumas estatísticas extras úteis para conferir o
comportamento dos algoritmos: utilização final, contagem por categoria
de falha, maior brecha residual e número de fusões realizadas.
"""

from __future__ import annotations

from simulador.memoria import Memoria
from simulador.runner import Estatisticas


def imprimir_relatorio(memoria: Memoria, stats: Estatisticas) -> None:
    total = memoria.tamanho_total
    media_ocupacao = (
        sum(stats.ocupacao_por_evento) / len(stats.ocupacao_por_evento)
        if stats.ocupacao_por_evento
        else 0
    )
    ocupacao_final = memoria.ocupacao()
    rejeitados_total = stats.falhas_fragmentacao_externa + stats.falhas_sem_espaco

    print("==================== RELATÓRIO FINAL ====================")
    print(f"  Memória total ............... {total}")
    print(f"  Eventos processados ......... {stats.total_eventos}")
    print()
    print(f"  Utilização média ............ {media_ocupacao / total * 100:6.2f}% "
          f"({media_ocupacao:.1f} / {total})")
    print(f"  Utilização final ............ {ocupacao_final / total * 100:6.2f}% "
          f"({ocupacao_final} / {total})")
    print(f"  Maior brecha final .......... {memoria.maior_brecha()}")
    print(f"  Soma das brechas finais ..... {memoria.soma_brechas()}")
    print(f"  Fusões realizadas (LIBERA) .. {stats.fusoes}")
    print()
    print(f"  Processos alocados .......... {stats.alocados}")
    print(f"  Processos liberados ......... {stats.liberados}")
    print(f"  LIBERAs de pid inexistente .. {stats.liberados_inexistentes}")
    print()
    print(f"  Rejeitados por fragmentação . {stats.falhas_fragmentacao_externa}")
    print(f"  Rejeitados por falta de mem . {stats.falhas_sem_espaco}")
    print(f"  Rejeitados (total) .......... {rejeitados_total}")
    print("=========================================================")
