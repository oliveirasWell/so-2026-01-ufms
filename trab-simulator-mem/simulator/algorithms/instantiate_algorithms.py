"""Registry: algorithm name -> `choose` function."""

from __future__ import annotations

from typing import TYPE_CHECKING

from simulator.algorithms import best_fit, first_fit, worst_fit

if TYPE_CHECKING:
    from simulator.runner import ChooseFunction


_ALGORITHM_ENTRIES = (
    ("first-fit", first_fit.choose),
    ("best-fit", best_fit.choose),
    ("worst-fit", worst_fit.choose),
)

ALGORITHM_FACTORIES = dict(_ALGORITHM_ENTRIES)
ALL_KEYS = tuple(k for k, _ in _ALGORITHM_ENTRIES)


def instantiate_algorithms(
    algo: str | None = None,
) -> tuple[tuple[str, "ChooseFunction"], ...]:
    """`algo=None` returns all three; otherwise only the requested one."""
    keys = ALL_KEYS if algo is None else (algo,)
    return tuple((k, ALGORITHM_FACTORIES[k]) for k in keys)
