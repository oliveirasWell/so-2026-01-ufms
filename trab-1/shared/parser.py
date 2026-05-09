from pathlib import Path

from models.process.process import Process
from models.process.workload import Workload

_QUANTUM_KEY = "quantum"
_CS_COST_KEY = "cs_cost"
_VALID_HEADERS = frozenset({_QUANTUM_KEY, _CS_COST_KEY})


def parse_input(path: str | Path) -> Workload:
    quantum: int = 0
    cs_cost: int = 0
    processes: list[Process] = []
    seen_pids: set[str] = set()

    raw = Path(path).read_text(encoding="utf-8")
    for line_no, raw_line in enumerate(raw.splitlines(), start=1):
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue

        if "=" in line and " " not in line.split("=", 1)[0]:
            key, value = line.split("=", 1)
            key = key.strip().lower()
            value = value.strip()
            if key not in _VALID_HEADERS:
                raise ValueError(f"line {line_no}: unknown header '{key}'")
            parsed = _parse_int(value, line_no, key)
            if parsed < 0:
                raise ValueError(f"line {line_no}: '{key}' must be non-negative")
            if key == _QUANTUM_KEY:
                quantum = parsed
            else:
                cs_cost = parsed
            continue

        processes.append(_parse_process_line(line, line_no, seen_pids))

    return Workload(
        processes=tuple(processes),
        quantum=quantum,
        context_switch_cost=cs_cost,
    )


def _parse_process_line(line: str, line_no: int, seen_pids: set[str]) -> Process:
    tokens = line.split()
    if len(tokens) < 4:
        raise ValueError(
            f"line {line_no}: expected 'pid arrival priority cpu1 [io1 cpu2 ...]'"
        )

    pid = tokens[0]
    if pid in seen_pids:
        raise ValueError(f"line {line_no}: duplicate pid '{pid}'")
    seen_pids.add(pid)

    arrival = _parse_int(tokens[1], line_no, "arrival")
    priority = _parse_int(tokens[2], line_no, "priority")
    if arrival < 0:
        raise ValueError(f"line {line_no}: arrival must be non-negative")
    if priority < 0:
        raise ValueError(f"line {line_no}: priority must be non-negative")

    bursts = tuple(_parse_int(tok, line_no, "burst") for tok in tokens[3:])
    if not bursts:
        raise ValueError(f"line {line_no}: '{pid}' has no bursts")
    if len(bursts) % 2 == 0:
        raise ValueError(
            f"line {line_no}: '{pid}' bursts length must be odd (CPU IO CPU ... CPU)"
        )
    if any(b <= 0 for b in bursts):
        raise ValueError(f"line {line_no}: '{pid}' bursts must be positive")

    return Process(pid=pid, arrival=arrival, priority=priority, bursts=bursts)


def _parse_int(token: str, line_no: int, field: str) -> int:
    try:
        return int(token)
    except ValueError as exc:
        raise ValueError(f"line {line_no}: '{field}' must be integer, got '{token}'") from exc
