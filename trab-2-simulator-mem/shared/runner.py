"""Runs a workload through one or all allocation algorithms."""

from algorithms.instantiate_algorithms import instantiate_algorithms
from models.simulation.simulation_result import SimulationResult
from models.workload.workload import Workload
from shared.simulator import run
from shared.visualization import make_event_printer


def run_simulation(
    workload: Workload,
    algo_key: str | None = None,
    *,
    verbose: bool = False,
    show_layout: bool = False,
) -> list[SimulationResult]:
    """``algo_key=None`` runs all three; otherwise only the requested one.

    With ``verbose=True`` each event is printed as it is processed (and
    ``show_layout=True`` adds the ASCII memory bar). Callers that only need the
    aggregated results (notebooks) leave it ``False``.
    """
    on_event = make_event_printer(show_layout=show_layout) if verbose else None
    results: list[SimulationResult] = []
    for name, choose in instantiate_algorithms(algo_key):
        memory, stats = run(workload, choose, on_event=on_event)
        results.append(SimulationResult(algorithm=name, memory=memory, stats=stats))
    return results
