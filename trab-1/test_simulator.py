"""Simulator regression test - frozen snapshot of metrics for inputs/workload.txt
across all 5 schedulers.

Run: python test_simulator.py  (exits 0 on success, AssertionError otherwise)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from shared.comparison import run_all
from shared.parser import parse_input

EXPECTED = {
    "FCFS": {
        "per_process": {
            "P1": {"finish": 26, "turnaround": 26, "waiting": 15, "response": 0},
            "P2": {"finish": 10, "turnaround": 9, "waiting": 5, "response": 5},
            "P3": {"finish": 33, "turnaround": 31, "waiting": 23, "response": 9},
            "P4": {"finish": 15, "turnaround": 11, "waiting": 10, "response": 10},
            "P5": {"finish": 19, "turnaround": 15, "waiting": 12, "response": 12},
            "P6": {"finish": 36, "turnaround": 30, "waiting": 25, "response": 14},
            "P7": {"finish": 28, "turnaround": 18, "waiting": 17, "response": 17},
        },
        "avg_turnaround": 20.0,
        "avg_waiting": 15.285714285714286,
        "avg_response": 9.571428571428571,
        "cpu_utilization": 0.75,
    },
    "SJF": {
        "per_process": {
            "P1": {"finish": 19, "turnaround": 19, "waiting": 8, "response": 0},
            "P2": {"finish": 31, "turnaround": 30, "waiting": 26, "response": 26},
            "P3": {"finish": 36, "turnaround": 34, "waiting": 26, "response": 6},
            "P4": {"finish": 7, "turnaround": 3, "waiting": 2, "response": 2},
            "P5": {"finish": 26, "turnaround": 22, "waiting": 19, "response": 19},
            "P6": {"finish": 22, "turnaround": 16, "waiting": 11, "response": 7},
            "P7": {"finish": 12, "turnaround": 2, "waiting": 1, "response": 1},
        },
        "avg_turnaround": 18.0,
        "avg_waiting": 13.285714285714286,
        "avg_response": 8.714285714285714,
        "cpu_utilization": 0.75,
    },
    "SJF (preemptive)": {
        "per_process": {
            "P1": {"finish": 27, "turnaround": 27, "waiting": 16, "response": 0},
            "P2": {"finish": 32, "turnaround": 31, "waiting": 27, "response": 27},
            "P3": {"finish": 37, "turnaround": 35, "waiting": 27, "response": 1},
            "P4": {"finish": 7, "turnaround": 3, "waiting": 2, "response": 2},
            "P5": {"finish": 23, "turnaround": 19, "waiting": 16, "response": 16},
            "P6": {"finish": 15, "turnaround": 9, "waiting": 4, "response": 2},
            "P7": {"finish": 12, "turnaround": 2, "waiting": 1, "response": 1},
        },
        "avg_turnaround": 18.0,
        "avg_waiting": 13.285714285714286,
        "avg_response": 7.0,
        "cpu_utilization": 0.7297297297297297,
    },
    "Priority": {
        "per_process": {
            "P1": {"finish": 22, "turnaround": 22, "waiting": 11, "response": 0},
            "P2": {"finish": 10, "turnaround": 9, "waiting": 5, "response": 5},
            "P3": {"finish": 36, "turnaround": 34, "waiting": 26, "response": 23},
            "P4": {"finish": 15, "turnaround": 11, "waiting": 10, "response": 10},
            "P5": {"finish": 31, "turnaround": 27, "waiting": 24, "response": 24},
            "P6": {"finish": 18, "turnaround": 12, "waiting": 7, "response": 5},
            "P7": {"finish": 24, "turnaround": 14, "waiting": 13, "response": 13},
        },
        "avg_turnaround": 18.428571428571427,
        "avg_waiting": 13.714285714285714,
        "avg_response": 11.428571428571429,
        "cpu_utilization": 0.75,
    },
    "Round Robin": {
        "per_process": {
            "P1": {"finish": 41, "turnaround": 41, "waiting": 30, "response": 0},
            "P2": {"finish": 19, "turnaround": 18, "waiting": 14, "response": 2},
            "P3": {"finish": 37, "turnaround": 35, "waiting": 27, "response": 4},
            "P4": {"finish": 13, "turnaround": 9, "waiting": 8, "response": 8},
            "P5": {"finish": 31, "turnaround": 27, "waiting": 24, "response": 10},
            "P6": {"finish": 34, "turnaround": 28, "waiting": 23, "response": 14},
            "P7": {"finish": 27, "turnaround": 17, "waiting": 16, "response": 16},
        },
        "avg_turnaround": 25.0,
        "avg_waiting": 20.285714285714285,
        "avg_response": 7.714285714285714,
        "cpu_utilization": 0.6585365853658537,
    },
}


def _snapshot(report) -> dict:
    return {
        "per_process": {
            pm.pid: {
                "finish": pm.finish,
                "turnaround": pm.turnaround,
                "waiting": pm.waiting,
                "response": pm.response,
            }
            for pm in report.per_process
        },
        "avg_turnaround": report.avg_turnaround,
        "avg_waiting": report.avg_waiting,
        "avg_response": report.avg_response,
        "cpu_utilization": report.cpu_utilization,
    }


def main() -> int:
    workload = parse_input(Path(__file__).parent / "inputs" / "workload.txt")
    actual = {report.algorithm: _snapshot(report) for _, report in run_all(workload)}
    if actual != EXPECTED:
        raise AssertionError(f"snapshot mismatch:\nexpected={EXPECTED}\nactual={actual}")
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
