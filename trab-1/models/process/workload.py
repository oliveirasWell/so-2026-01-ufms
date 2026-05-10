"""Modelo imutável do *workload* carregado de JSON.

Para o formato JSON, defaults e regras de validação, veja o ``README.md``
e ``shared.parser.parse_input``.
"""

from dataclasses import dataclass

from models.process.process import Process


@dataclass(frozen=True)
class Workload:
    processes: tuple[Process, ...]
    quantum: int = 0
    context_switch_cost: int = 0
