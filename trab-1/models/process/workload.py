"""Immutable model of the *workload* loaded from JSON.

For the JSON format, defaults, and validation rules, see ``README.md``
and ``shared.parser.parse_input``.
"""

from dataclasses import dataclass

from models.process.process import Process


@dataclass(frozen=True)
class Workload:
    processes: tuple[Process, ...]
    quantum: int = 0
    context_switch_cost: int = 0
