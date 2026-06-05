"""Worst Fit.

Examines all gaps and returns the index of the LARGEST gap that fits.
Tie: the leftmost gap wins (first found). The idea is to leave the biggest
possible leftover for other processes.
"""

from __future__ import annotations

from simulator.memory import Memory


def choose(memory: Memory, size: int) -> int | None:
    worst_index: int | None = None
    largest_size: int | None = None
    for index, block in memory.gaps():
        if block.size < size:
            continue
        if largest_size is None or block.size > largest_size:
            largest_size = block.size
            worst_index = index
    return worst_index
