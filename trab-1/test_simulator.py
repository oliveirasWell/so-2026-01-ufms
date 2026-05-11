import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from shared.runner import run_simulation
from shared.parser import parse_input

_ROOT = Path(__file__).resolve().parent
_SNAPSHOT_JSON = _ROOT / "snapshots" / "workload_metrics.json"
_WORKLOAD_JSON = _ROOT / "inputs" / "workload.json"


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
    workload = parse_input(_WORKLOAD_JSON)
    _, _, reports = run_simulation(workload)
    actual = {report.algorithm: _snapshot(report) for report in reports}
    expected = json.loads(_SNAPSHOT_JSON.read_text(encoding="utf-8"))
    if actual != expected:
        raise AssertionError("metrics diverge from snapshot;")
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
