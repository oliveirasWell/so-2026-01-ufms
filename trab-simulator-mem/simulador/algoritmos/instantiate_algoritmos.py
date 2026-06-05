"""Registry: nome do algoritmo -> função `escolher`."""

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
    """`algo=None` devolve os três; senão, só o solicitado."""
    keys = ALL_KEYS if algo is None else (algo,)
    return tuple((k, ALGORITMO_FACTORIES[k]) for k in keys)
