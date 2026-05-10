import json
from pathlib import Path

from models.process.process import Process
from models.process.workload import Workload


def _hook(d):
    # O json chama este hook para *cada* objeto {...} do arquivo, de dentro para fora.
    # Objetos de processo trazem "pid"; o objeto raiz traz "quantum", "processes", etc., mas não "pid".
    if "pid" in d:
        return Process(
            d["pid"],
            d["arrival"],
            d.get("priority", 1),
            tuple(d["bursts"]),
        )
    return Workload(
        tuple(d.get("processes", ())),
        d.get("quantum", 0),
        d.get("context_switch_cost", 0),
    )

def parse_input(path):
    return json.loads(Path(path).read_text("utf-8"), object_hook=_hook)
