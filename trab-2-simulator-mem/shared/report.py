"""Final simulation report.

The assignment requires reporting "memory utilization" and the "number of
processes that could not be allocated for lack of contiguous space". We report
those two plus a few extra statistics useful to check the algorithms' behavior:
final utilization, per-category failure counts, largest residual gap and number
of merges performed.
"""

from models.memory.memory import Memory
from models.simulation.simulation_result import SimulationResult
from models.simulation.statistics import Statistics
from shared.evaluation import pick_winners

_COMPARISON_COLUMNS = (
    "allocated",
    "external_fragmentation_failures",
    "no_space_failures",
    "merges",
    "final_utilization_pct",
    "final_largest_gap",
)

_COLUMN_LABELS = {
    "allocated": "Alocados",
    "external_fragmentation_failures": "Rej. frag.",
    "no_space_failures": "Rej. s/ mem",
    "merges": "Fusões",
    "final_utilization_pct": "Util. final %",
    "final_largest_gap": "Maior brecha",
}


def print_reports(results: list[SimulationResult]) -> None:
    for result in results:
        print(f"=== {result.algorithm} ===")
        print_report(result.memory, result.stats)
        print()

    if len(results) > 1:
        print_comparison(
            [(r.algorithm, snapshot_summary(r.memory, r.stats)) for r in results]
        )


def print_report(memory: Memory, stats: Statistics) -> None:
    total = memory.total_size
    average_usage = (
        sum(stats.usage_per_event) / len(stats.usage_per_event)
        if stats.usage_per_event
        else 0
    )
    final_usage = memory.used()
    total_rejected = stats.external_fragmentation_failures + stats.no_space_failures

    print("==================== RELATÓRIO FINAL ====================")
    print(f"  Memória total ............... {total}")
    print(f"  Eventos processados ......... {stats.total_events}")
    print()
    print(f"  Utilização média ............ {average_usage / total * 100:6.2f}% "
          f"({average_usage:.1f} / {total})")
    print(f"  Utilização final ............ {final_usage / total * 100:6.2f}% "
          f"({final_usage} / {total})")
    print(f"  Maior brecha final .......... {memory.largest_gap()}")
    print(f"  Soma das gaps finais ..... {memory.free_space()}")
    print(f"  Fusões realizadas (FREE) .. {stats.merges}")
    print()
    print(f"  Processos alocados .......... {stats.allocated}")
    print(f"  Processos liberados ......... {stats.freed}")
    print(f"  LIBERAs de pid inexistente .. {stats.freed_missing}")
    print()
    print(f"  Rejeitados por fragmentação . {stats.external_fragmentation_failures}")
    print(f"  Rejeitados por falta de mem . {stats.no_space_failures}")
    print(f"  Rejeitados (total) .......... {total_rejected}")
    print("=========================================================")


def snapshot_summary(memory: Memory, stats: Statistics) -> dict:
    """JSON-serializable summary (basis for snapshots and the comparison)."""
    total = memory.total_size
    return {
        "allocated": stats.allocated,
        "freed": stats.freed,
        "freed_missing": stats.freed_missing,
        "external_fragmentation_failures": stats.external_fragmentation_failures,
        "no_space_failures": stats.no_space_failures,
        "merges": stats.merges,
        "final_utilization_pct": round(memory.used() / total * 100, 2),
        "final_largest_gap": memory.largest_gap(),
        "final_free_space": memory.free_space(),
    }


def print_comparison(reports: list[tuple[str, dict]]) -> None:
    """TSV table + per-metric winner."""
    print("Comparação")
    print("\t".join(("algoritmo",) + _COMPARISON_COLUMNS))
    for name, summary in reports:
        print("\t".join([name] + [str(summary[c]) for c in _COMPARISON_COLUMNS]))

    print()
    print("Vencedor por métrica (menos falhas/rejeições e mais utilização é melhor)")
    for metric, name in pick_winners(dict(reports)).items():
        print(f"  {metric}: {name}")


def to_markdown(reports: list[tuple[str, dict]]) -> str:
    """Comparison as a rendered Markdown table + winners — for the notebook."""
    labels = [_COLUMN_LABELS[c] for c in _COMPARISON_COLUMNS]
    lines = [
        "| Algoritmo | " + " | ".join(labels) + " |",
        "| :-- |" + " --: |" * len(_COMPARISON_COLUMNS),
    ]
    for name, summary in reports:
        cells = [str(summary[c]) for c in _COMPARISON_COLUMNS]
        lines.append(f"| {name} | " + " | ".join(cells) + " |")

    lines += ["", "**Vencedor por métrica**", "", "| Métrica | Vencedor |", "| :-- | :-- |"]
    lines += [f"| `{metric}` | {name} |" for metric, name in pick_winners(dict(reports)).items()]
    return "\n".join(lines)
