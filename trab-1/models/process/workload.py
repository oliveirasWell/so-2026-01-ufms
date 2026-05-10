"""Modelo do *workload* carregado de JSON (veja ``shared.parser.parse_input``).

Estrutura típica::

    {
      "quantum": 0,
      "context_switch_cost": 0,
      "processes": [
        {"pid": "P1", "arrival": 0, "priority": 1, "bursts": [5, 3, 3]}
      ]
    }

``quantum`` e ``context_switch_cost`` são opcionais (padrão ``0``).
``priority`` por processo é opcional (padrão ``1``).
``bursts``: comprimento ímpar (CPU, E/S, …, CPU), valores > 0.
"""

from dataclasses import dataclass

from models.process.process import Process


@dataclass(frozen=True)
class Workload:
    """Conjunto imutável de processos e parâmetros globais da simulação."""

    processes: tuple[Process, ...]
    quantum: int = 0
    context_switch_cost: int = 0
