"""Textual printing of the memory state.

Each call to ``print_state`` shows the partitions and gaps of the same
instant. With ``show_layout=True`` it also prints a compact ASCII bar — a
proportional layout of the whole memory in a single line, handy to spot
fragmentation at a glance (enabled by the ``--layout`` CLI flag).
"""

from collections.abc import Callable

from models.memory.memory import Memory
from models.simulation.event_result import EventResult
from models.simulation.result_kind import ResultKind


def describe_result(result: EventResult) -> str:
    event = result.event
    if result.kind == ResultKind.ALLOCATED:
        return f"ALOC  {event.pid}={event.size}  → alocado na brecha #{result.gap_index}"
    if result.kind == ResultKind.FREED:
        return f"FREE {event.pid}  → liberado"
    if result.kind == ResultKind.FREED_MISSING:
        return f"FREE {event.pid}  → AVISO: pid inexistente (ignorado)"
    if result.kind == ResultKind.FAIL_EXTERNAL_FRAGMENTATION:
        return (
            f"ALOC  {event.pid}={event.size}  → FALHA: FRAGMENTAÇÃO EXTERNA "
            f"(soma das gaps comporta, mas nenhuma individualmente)"
        )
    if result.kind == ResultKind.FAIL_NO_SPACE:
        return f"ALOC  {event.pid}={event.size}  → FALHA: sem memória suficiente"
    return f"{event}"


def make_event_printer(
    *, show_layout: bool = False
) -> Callable[[int, EventResult, Memory], None]:
    """Build an ``on_event`` callback that prints each event and the resulting
    memory state. The event number is supplied by the engine, keeping all
    stdout in the presentation layer while the simulation engine stays pure.
    """

    def on_event(number: int, result: EventResult, memory: Memory) -> None:
        print("========================================================")
        print(f"Evento #{number}: {describe_result(result)}")
        print_state(memory, show_layout=show_layout)
        print()

    return on_event


def print_state(memory: Memory, *, show_layout: bool = False, bar_width: int = 60) -> None:
    print("  Partições ocupadas:")
    occupied = [b for b in memory.blocks if not b.is_free]
    if not occupied:
        print("    (nenhuma)")
    else:
        for b in occupied:
            print(f"    [{b.start:>5}–{b.end - 1:>5}] {b.pid:<6} tam={b.size}")

    print("  Gaps:")
    free_blocks = [b for b in memory.blocks if b.is_free]
    if not free_blocks:
        print("    (nenhuma)")
    else:
        for b in free_blocks:
            print(f"    [{b.start:>5}–{b.end - 1:>5}] LIVRE  tam={b.size}")

    if show_layout:
        print(f"  Layout: {_ascii_bar(memory, bar_width)}")


def _ascii_bar(memory: Memory, width: int) -> str:
    """Render the whole memory as a bar ``width`` characters wide."""
    total = memory.total_size
    parts: list[str] = []
    for b in memory.blocks:
        # At least 1 char per block so tiny blocks don't vanish.
        n = max(1, round(b.size / total * width))
        # Gaps use '.', occupied use the last char of the pid
        # ("P1"/"P2"/etc. -> "1"/"2"/etc., readable in didactic workloads).
        label = "." if b.is_free else b.pid[-1]
        parts.append(label * n)
    return "|" + "|".join(parts) + "|"
