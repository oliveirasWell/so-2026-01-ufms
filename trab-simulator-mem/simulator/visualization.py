"""Textual printing of the memory state.

Each call to `print_state` shows three views of the same instant:

1. Occupied partitions — one line per block with pid and interval.
2. Gaps — one line per free space.
3. Compact ASCII bar — proportional layout of the whole memory in a
   single line, handy to spot fragmentation at a glance.

Code identifiers are English; the printed strings stay in Portuguese.
"""

from __future__ import annotations

from simulator.memory import Memory
from simulator.runner import EventResult


def describe_result(result: EventResult) -> str:
    event = result.event
    if result.kind == "ALLOCATED":
        return (
            f"ALOC  {event.pid}={event.size}  → alocado na brecha #{result.gap_index}"
        )
    if result.kind == "FREED":
        return f"LIBERA {event.pid}  → liberado"
    if result.kind == "FREED_MISSING":
        return f"LIBERA {event.pid}  → AVISO: pid inexistente (ignorado)"
    if result.kind == "FAIL_EXTERNAL_FRAGMENTATION":
        return (
            f"ALOC  {event.pid}={event.size}  → FALHA: FRAGMENTAÇÃO EXTERNA "
            f"(soma das brechas comporta, mas nenhuma individualmente)"
        )
    if result.kind == "FAIL_NO_SPACE":
        return f"ALOC  {event.pid}={event.size}  → FALHA: sem memória suficiente"
    return f"{event}"


def print_state(memory: Memory, bar_width: int = 60) -> None:
    print("  Partições ocupadas:")
    occupied = [b for b in memory.blocks if not b.is_free]
    if not occupied:
        print("    (nenhuma)")
    else:
        for b in occupied:
            print(f"    [{b.start:>5}–{b.end - 1:>5}] {b.pid:<6} tam={b.size}")

    print("  Brechas:")
    free_blocks = [b for b in memory.blocks if b.is_free]
    if not free_blocks:
        print("    (nenhuma)")
    else:
        for b in free_blocks:
            print(f"    [{b.start:>5}–{b.end - 1:>5}] LIVRE  tam={b.size}")

    print(f"  Layout: {_ascii_bar(memory, bar_width)}")


def _ascii_bar(memory: Memory, width: int) -> str:
    """Render the whole memory as a bar `width` characters wide."""
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
