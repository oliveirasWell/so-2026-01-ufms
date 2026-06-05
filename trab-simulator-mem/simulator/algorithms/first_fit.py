"""First Fit.

Scans memory front to back and returns the index of the FIRST gap large
enough. Returns None if none fits.
"""

from __future__ import annotations

from simulator.memory import Memory


def choose(memory: Memory, size: int) -> int | None:
    for index, block in memory.gaps():
        if block.size >= size:
            return index
    return None
