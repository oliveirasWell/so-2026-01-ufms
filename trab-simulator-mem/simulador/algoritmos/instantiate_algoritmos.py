"""Registry dos algoritmos de alocação.

Espelha `trab-1/schedulers/instantiate_schedulers.py`: mapeia o nome do
algoritmo (`first-fit`, `best-fit`, `worst-fit`) para a sua função
`escolher(memoria, tamanho) -> int | None` e permite instanciar um
algoritmo específico ou todos de uma vez.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from simulador.algoritmos import best_fit, first_fit, worst_fit

if TYPE_CHECKING:
    from simulador.runner import AlgoritmoEscolher


_ALGORITMO_ENTRIES = (
    ("first-fit", first_fit.escolher),
    ("best-fit", best_fit.escolher),
    ("worst-fit", worst_fit.escolher),
)

ALGORITMO_FACTORIES = dict(_ALGORITMO_ENTRIES)
ALL_KEYS = tuple(k for k, _ in _ALGORITMO_ENTRIES)


def instantiate_algoritmos(
    algo: str | None = None,
) -> tuple[tuple[str, "AlgoritmoEscolher"], ...]:
    """Devolve `((nome, escolher), ...)` para um algoritmo ou para todos.

    Com `algo=None` retorna os três na ordem do registry; caso contrário,
    apenas o solicitado.
    """
    keys = ALL_KEYS if algo is None else (algo,)
    return tuple((k, ALGORITMO_FACTORIES[k]) for k in keys)
