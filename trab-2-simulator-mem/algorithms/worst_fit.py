"""Worst Fit.

Among the gaps that fit, returns the index of the LARGEST one, leaving the
biggest possible leftover for other processes. Tie: the leftmost gap wins,
since ``max`` keeps the first item on equal keys.
"""

from models.memory.memory import Memory


def choose(memory: Memory, size: int) -> int | None:
    eligible = memory.eligible_gaps(size)
    if not eligible:
        return None
    index, _ = max(eligible, key=lambda item: item[1].size)
    return index
