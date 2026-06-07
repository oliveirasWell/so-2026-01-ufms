"""Best Fit.

Among the gaps that fit, returns the index of the one leaving the smallest
leftover (i.e. the smallest gap that still fits). Tie: the leftmost gap wins,
since ``min`` keeps the first item on equal keys.
"""

from models.memory.memory import Memory


def choose(memory: Memory, size: int) -> int | None:
    eligible = memory.eligible_gaps(size)
    if not eligible:
        return None
    index, _ = min(eligible, key=lambda item: item[1].size)
    return index
