"""First Fit.

Scans memory front to back and returns the index of the FIRST gap large
enough. Returns None if none fits.
"""

from models.memory.memory import Memory


def choose(memory: Memory, size: int) -> int | None:
    eligible = memory.eligible_gaps(size)
    return eligible[0][0] if eligible else None
