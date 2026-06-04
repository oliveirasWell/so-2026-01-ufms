"""Estatísticas descritivas do *input* (workload), separadas das métricas
de execução do escalonador.

Útil para raciocinar sobre como a forma do workload (variância de bursts,
mix CPU/E/S, dispersão de chegadas) influencia o resultado de cada
algoritmo.
"""

import sys
from dataclasses import dataclass
from statistics import mean, pstdev
from typing import TextIO

from models.process.workload import Workload


@dataclass(frozen=True)
class WorkloadStats:
    n_processes: int
    avg_process_time: float
    avg_cpu: float
    avg_io: float
    min_process_time: int
    max_process_time: int
    stdev_process_time: float
    avg_bursts: float
    avg_arrival: float
    arrival_span: int
    total_cpu_demand: int
    total_io_demand: int
    cpu_io_ratio: float | None
    quantum: int
    context_switch_cost: int


def compute_workload_stats(workload: Workload) -> WorkloadStats:
    procs = workload.processes
    n = len(procs)
    if n == 0:
        return WorkloadStats(
            n_processes=0,
            avg_process_time=0.0,
            avg_cpu=0.0,
            avg_io=0.0,
            min_process_time=0,
            max_process_time=0,
            stdev_process_time=0.0,
            avg_bursts=0.0,
            avg_arrival=0.0,
            arrival_span=0,
            total_cpu_demand=0,
            total_io_demand=0,
            cpu_io_ratio=None,
            quantum=workload.quantum,
            context_switch_cost=workload.context_switch_cost,
        )

    cpu_per_proc = [p.cpu_total for p in procs]
    io_per_proc = [p.io_total for p in procs]
    total_per_proc = [c + i for c, i in zip(cpu_per_proc, io_per_proc)]
    arrivals = [p.arrival for p in procs]
    total_io = sum(io_per_proc)
    total_cpu = sum(cpu_per_proc)

    return WorkloadStats(
        n_processes=n,
        avg_process_time=mean(total_per_proc),
        avg_cpu=mean(cpu_per_proc),
        avg_io=mean(io_per_proc),
        min_process_time=min(total_per_proc),
        max_process_time=max(total_per_proc),
        stdev_process_time=pstdev(total_per_proc) if n > 1 else 0.0,
        avg_bursts=mean(len(p.bursts) for p in procs),
        avg_arrival=mean(arrivals),
        arrival_span=max(arrivals) - min(arrivals),
        total_cpu_demand=total_cpu,
        total_io_demand=total_io,
        cpu_io_ratio=(total_cpu / total_io) if total_io > 0 else None,
        quantum=workload.quantum,
        context_switch_cost=workload.context_switch_cost,
    )


def print_workload_stats(
    stats: WorkloadStats,
    file: TextIO | None = None,
    *,
    title: str = "Workload — características do input",
) -> None:
    out = file or sys.stdout

    ratio_repr = f"{stats.cpu_io_ratio:.2f}" if stats.cpu_io_ratio is not None else "— (sem E/S)"
    rows = [
        ("Processos", f"{stats.n_processes}"),
        ("Tempo médio por processo", f"{stats.avg_process_time:.2f} ticks  (CPU+E/S)"),
        ("Tempo médio de CPU", f"{stats.avg_cpu:.2f} ticks"),
        ("Tempo médio de E/S", f"{stats.avg_io:.2f} ticks"),
        ("Tempo mín / máx por processo", f"{stats.min_process_time} / {stats.max_process_time} ticks"),
        ("Desvio-padrão do tempo total", f"{stats.stdev_process_time:.2f} ticks"),
        ("Bursts médios por processo", f"{stats.avg_bursts:.2f}"),
        ("Chegada média / janela", f"{stats.avg_arrival:.2f}  /  {stats.arrival_span} ticks"),
        ("Demanda total CPU / E/S", f"{stats.total_cpu_demand} / {stats.total_io_demand} ticks"),
        ("Razão CPU / E/S", ratio_repr),
        ("Quantum / custo troca de contexto", f"{stats.quantum} / {stats.context_switch_cost}"),
    ]

    label_w = max(len(label) for label, _ in rows)
    value_w = max(len(value) for _, value in rows)
    inner_w = label_w + 3 + value_w
    border = "─" * (inner_w + 4)

    out.write(f"┌{border}┐\n")
    out.write(f"│  {title.ljust(inner_w)}  │\n")
    out.write(f"├{border}┤\n")
    for label, value in rows:
        out.write(f"│  {label.ljust(label_w)} : {value.ljust(value_w)}  │\n")
    out.write(f"└{border}┘\n")
