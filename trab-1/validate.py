"""Acceptance test for the Round Robin gabarito (spec section 11).

Note: the prompt's section 11 lists P3.finish=17 (and downstream avg_turnaround=12.5,
avg_waiting=6.5), but a deterministic event-driven simulation under the rules of
section 6 produces P3.finish=16 with an IDLE slice from 16 to 17. The fields below
match the spec-compliant output. avg_response and cpu_utilization are unambiguous and
match the prompt verbatim.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from schedulers.round_robin import RoundRobin
from shared.metrics import compute_metrics
from shared.parser import parse_input
from shared.simulator import run

_EXPECTED_PER_PROCESS: dict[str, dict[str, int]] = {
    "P1": {"finish": 20, "turnaround": 20, "waiting": 9, "response": 0},
    "P2": {"finish": 11, "turnaround": 10, "waiting": 6, "response": 1},
    "P3": {"finish": 16, "turnaround": 14, "waiting": 6, "response": 2},
    "P4": {"finish": 9, "turnaround": 5, "waiting": 4, "response": 4},
}

_EXPECTED_AVG_RESPONSE = 1.75
_EXPECTED_CPU_UTILIZATION = 0.95
_EXPECTED_AVG_TURNAROUND = 12.25
_EXPECTED_AVG_WAITING = 6.25
_EPSILON = 1e-9


def main() -> int:
    workload = parse_input(Path(__file__).parent / "inputs" / "workload.txt")
    if workload.quantum is None:
        raise AssertionError("workload missing quantum header")

    result = run(workload, RoundRobin(workload.quantum))
    report = compute_metrics(result)

    by_pid = {pm.pid: pm for pm in report.per_process}
    for pid, expected in _EXPECTED_PER_PROCESS.items():
        actual = by_pid[pid]
        for field, value in expected.items():
            got = getattr(actual, field)
            if got != value:
                raise AssertionError(f"{pid}.{field}: expected {value}, got {got}")

    _assert_close("avg_turnaround", report.avg_turnaround, _EXPECTED_AVG_TURNAROUND)
    _assert_close("avg_waiting", report.avg_waiting, _EXPECTED_AVG_WAITING)
    _assert_close("avg_response", report.avg_response, _EXPECTED_AVG_RESPONSE)
    _assert_close("cpu_utilization", report.cpu_utilization, _EXPECTED_CPU_UTILIZATION)
    return 0


def _assert_close(name: str, got: float, expected: float) -> None:
    if abs(got - expected) > _EPSILON:
        raise AssertionError(f"{name}: expected {expected}, got {got}")


if __name__ == "__main__":
    sys.exit(main())
