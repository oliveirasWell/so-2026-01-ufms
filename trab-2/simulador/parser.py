"""Leitura do arquivo de entrada em JSON.

Formato esperado:

    {
      "memoria_total": 1000,
      "eventos": [
        {"tipo": "ALOC",   "pid": "P1", "tamanho": 200},
        {"tipo": "ALOC",   "pid": "P2", "tamanho": 300},
        {"tipo": "LIBERA", "pid": "P1"}
      ]
    }

O usuário garante que o arquivo está bem-formado (mesma convenção do trab-1).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal


TipoEvento = Literal["ALOC", "LIBERA"]


@dataclass(frozen=True)
class Evento:
    tipo: TipoEvento
    pid: str
    tamanho: int | None = None  # obrigatório em ALOC, ausente em LIBERA


@dataclass(frozen=True)
class Workload:
    memoria_total: int
    eventos: list[Evento]


def parse_input(path: str | Path) -> Workload:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    memoria_total = int(raw["memoria_total"])
    eventos: list[Evento] = []
    for ev in raw["eventos"]:
        tipo = ev["tipo"]
        pid = str(ev["pid"])
        tamanho = int(ev["tamanho"]) if tipo == "ALOC" else None
        eventos.append(Evento(tipo=tipo, pid=pid, tamanho=tamanho))

    return Workload(memoria_total=memoria_total, eventos=eventos)
