"""Registry: algorithm key -> ``choose`` function."""

from algorithms import best_fit, first_fit, worst_fit
from models.types import ChooseFunction

_ALGORITHM_ENTRIES: tuple[tuple[str, ChooseFunction], ...] = (
    ("first-fit", first_fit.choose),
    ("best-fit", best_fit.choose),
    ("worst-fit", worst_fit.choose),
)

ALGORITHM_FACTORIES = dict(_ALGORITHM_ENTRIES)
ALL_KEYS = tuple(key for key, _ in _ALGORITHM_ENTRIES)


def instantiate_algorithms(
    algo_key: str | None = None,
) -> tuple[tuple[str, ChooseFunction], ...]:
    """``algo_key=None`` returns all three; otherwise only the requested one."""
    keys = ALL_KEYS if algo_key is None else (algo_key,)
    return tuple((key, ALGORITHM_FACTORIES[key]) for key in keys)
