"""Best Fit.

Examines all gaps and returns the index of the one that leaves the
smallest leftover (`gap.size - size`). Tie: the leftmost gap wins (first
found), per the documented convention.
"""

from __future__ import annotations

from simulator.memory import Memory


def choose(memory: Memory, size: int) -> int | None:
    best_index: int | None = None
    smallest_leftover: int | None = None
    for index, block in memory.gaps():
        if block.size < size:
            continue
        leftover = block.size - size
        if smallest_leftover is None or leftover < smallest_leftover:
            smallest_leftover = leftover
            best_index = index
    return best_index
