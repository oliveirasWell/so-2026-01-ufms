"""Snapshot regression: compares `run_simulation` against `snapshots/*.json`.

Regenerate with `generate_snapshots()` when the semantics change on purpose.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from simulator.memory import Memory
from simulator.parser import parse_input
from simulator.report import snapshot_summary
from simulator.runner import run_simulation


_ROOT = Path(__file__).resolve().parent

_CASES = (
    ("workload_simples", "inputs/workload_simples.json", "snapshots/workload_simples_stats.json"),
    ("workload_fragmentacao", "inputs/workload_fragmentacao.json", "snapshots/workload_fragmentacao_stats.json"),
)


def _summaries(input_rel: str) -> dict[str, dict]:
    workload = parse_input(_ROOT / input_rel)
    return {
        r.algorithm: snapshot_summary(r.memory, r.stats)
        for r in run_simulation(workload)
    }


def _test_snapshots() -> None:
    for name, input_rel, snap_rel in _CASES:
        expected = json.loads((_ROOT / snap_rel).read_text(encoding="utf-8"))
        actual = _summaries(input_rel)
        for algo, expected_algo in expected.items():
            if actual.get(algo) != expected_algo:
                raise AssertionError(
                    f"\n[{name} / {algo}] divergiu:\n"
                    f"  esperado = {expected_algo}\n"
                    f"  obtido   = {actual.get(algo)}"
                )


def _test_coalescing() -> None:
    # freeing everything must return a single free block of the original size
    m = Memory(1000)
    m.allocate("P1", 300, 0)
    m.allocate("P2", 200, 1)
    m.allocate("P3", 100, 2)
    m.free("P2")
    m.free("P1")
    m.free("P3")
    if len(m.blocks) != 1 or m.blocks[0].size != 1000 or not m.blocks[0].is_free:
        raise AssertionError(
            f"coalescing falhou: esperado [livre:1000], obtido {m.blocks}"
        )


def generate_snapshots() -> None:
    """Dev: `python3 -c "import test_simulator as t; t.generate_snapshots()"`."""
    for _, input_rel, snap_rel in _CASES:
        summaries = _summaries(input_rel)
        (_ROOT / snap_rel).write_text(
            json.dumps(summaries, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"escrito {snap_rel}")


def main() -> int:
    _test_snapshots()
    _test_coalescing()
    print("OK — snapshots (3 algoritmos × 2 workloads) + coalescing")
    return 0


if __name__ == "__main__":
    sys.exit(main())
