"""Orquestração da simulação evento-a-evento.

Aplica cada evento do workload sobre a memória usando um algoritmo de
escolha de brecha (`escolher(memoria, tamanho) -> int | None`) e classifica
o resultado. Mantém estatísticas agregadas usadas pelo relatório final.

Classificação de uma alocação que o algoritmo recusou (escolher → None):
- soma das brechas ≥ tamanho pedido ⇒ FRAGMENTAÇÃO EXTERNA
  (há espaço total, só não contíguo — definição literal do enunciado)
- soma das brechas < tamanho pedido ⇒ FALTA DE ESPAÇO
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Literal

from simulador.memoria import Memoria
from simulador.parser import Evento, Workload


TipoResultado = Literal[
    "ALOCADO",
    "LIBERADO",
    "LIBERADO_INEXISTENTE",
    "FALHA_FRAGMENTACAO_EXTERNA",
    "FALHA_SEM_ESPACO",
]


@dataclass(frozen=True)
class ResultadoEvento:
    evento: Evento
    tipo: TipoResultado
    indice_brecha: int | None = None  # preenchido em ALOCADO


@dataclass
class Estatisticas:
    total_eventos: int = 0
    alocados: int = 0
    liberados: int = 0
    liberados_inexistentes: int = 0
    falhas_fragmentacao_externa: int = 0
    falhas_sem_espaco: int = 0
    ocupacao_por_evento: list[int] = field(default_factory=list)
    fusoes: int = 0


AlgoritmoEscolher = Callable[[Memoria, int], int | None]


def processar(
    memoria: Memoria,
    evento: Evento,
    escolher: AlgoritmoEscolher,
) -> ResultadoEvento:
    if evento.tipo == "ALOC":
        assert evento.tamanho is not None
        indice = escolher(memoria, evento.tamanho)
        if indice is not None:
            memoria.alocar(evento.pid, evento.tamanho, indice)
            return ResultadoEvento(evento, "ALOCADO", indice_brecha=indice)
        # Algoritmo recusou: distinguir fragmentação externa de falta de espaço.
        if memoria.soma_brechas() >= evento.tamanho:
            return ResultadoEvento(evento, "FALHA_FRAGMENTACAO_EXTERNA")
        return ResultadoEvento(evento, "FALHA_SEM_ESPACO")

    # tipo == "LIBERA"
    achou = memoria.liberar(evento.pid)
    return ResultadoEvento(evento, "LIBERADO" if achou else "LIBERADO_INEXISTENTE")


def executar(
    workload: Workload,
    escolher: AlgoritmoEscolher,
    *,
    on_evento: Callable[[ResultadoEvento, Memoria], None] | None = None,
) -> tuple[Memoria, Estatisticas]:
    """Aplica todos os eventos do workload e devolve (memória final, stats).

    `on_evento`, se fornecido, é chamado após cada evento — usado pelo main
    para imprimir o estado em modo verbose.
    """
    memoria = Memoria(workload.memoria_total)
    stats = Estatisticas()

    for evento in workload.eventos:
        resultado = processar(memoria, evento, escolher)
        stats.total_eventos += 1
        if resultado.tipo == "ALOCADO":
            stats.alocados += 1
        elif resultado.tipo == "LIBERADO":
            stats.liberados += 1
        elif resultado.tipo == "LIBERADO_INEXISTENTE":
            stats.liberados_inexistentes += 1
        elif resultado.tipo == "FALHA_FRAGMENTACAO_EXTERNA":
            stats.falhas_fragmentacao_externa += 1
        elif resultado.tipo == "FALHA_SEM_ESPACO":
            stats.falhas_sem_espaco += 1
        stats.ocupacao_por_evento.append(memoria.ocupacao())

        if on_evento is not None:
            on_evento(resultado, memoria)

    stats.fusoes = memoria.fusoes
    return memoria, stats


@dataclass(frozen=True)
class ResultadoSimulacao:
    algoritmo: str
    memoria: Memoria
    stats: Estatisticas


def run_simulation(
    workload: Workload,
    algo: str | None = None,
    *,
    on_evento: Callable[[ResultadoEvento, Memoria], None] | None = None,
) -> list[ResultadoSimulacao]:
    """`algo=None` roda os três; senão, só o solicitado."""
    # import local evita ciclo (o registry referencia este módulo)
    from simulador.algoritmos.instantiate_algoritmos import instantiate_algoritmos

    resultados: list[ResultadoSimulacao] = []
    for nome, escolher in instantiate_algoritmos(algo):
        memoria, stats = executar(workload, escolher, on_evento=on_evento)
        resultados.append(ResultadoSimulacao(algoritmo=nome, memoria=memoria, stats=stats))
    return resultados
