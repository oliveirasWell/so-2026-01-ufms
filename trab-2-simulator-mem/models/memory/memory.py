"""Model of the simulated memory.

Memory is an ordered list of contiguous blocks. Each block has a start
address, a size and a pid: if pid is None the block is a gap (free space);
otherwise it is a partition occupied by that process.

Every allocate/free operation keeps the invariant that the sum of the block
sizes equals ``total_size`` and that adjacent free blocks are always merged
(coalescing).
"""

from models.memory.block import Block


class Memory:
    def __init__(self, total_size: int) -> None:
        self.total_size = total_size
        self.blocks: list[Block] = [Block(start=0, size=total_size, pid=None)]
        self.merges = 0  # count of gap merges during free

    def gaps(self) -> list[tuple[int, Block]]:
        """List of (global_index, block) for every free block."""
        return [(i, b) for i, b in enumerate(self.blocks) if b.is_free]

    def eligible_gaps(self, size: int) -> list[tuple[int, Block]]:
        """(global_index, block) for every free block that fits ``size``."""
        return [(i, b) for i, b in self.gaps() if b.size >= size]

    def allocate(self, pid: str, size: int, gap_index: int) -> None:
        """Allocate ``pid`` into the gap at ``gap_index``.

        The gap must have size >= ``size``. Any leftover becomes a new gap
        right after the allocated partition.
        """
        gap = self.blocks[gap_index]
        assert gap.is_free, "index does not point to a gap"
        assert gap.size >= size, "gap smaller than request"

        occupied = Block(start=gap.start, size=size, pid=pid)
        leftover = gap.size - size

        if leftover == 0:
            self.blocks[gap_index] = occupied
        else:
            new_gap = Block(start=gap.start + size, size=leftover, pid=None)
            self.blocks[gap_index:gap_index + 1] = [occupied, new_gap]

    def free(self, pid: str) -> bool:
        """Free the block of process ``pid`` and merge with free neighbors.

        Returns True if a block was freed, False if no process had that pid
        (documented in the README — it only warns, never crashes).
        """
        idx = next((i for i, b in enumerate(self.blocks) if b.pid == pid), None)
        if idx is None:
            return False

        self.blocks[idx].pid = None
        self._merge_neighbors(idx)
        return True

    def _merge_neighbors(self, idx: int) -> None:
        # Merge with the right neighbor first (does not shift idx).
        if idx + 1 < len(self.blocks) and self.blocks[idx + 1].is_free:
            right = self.blocks.pop(idx + 1)
            self.blocks[idx].size += right.size
            self.merges += 1

        # Merge with the left neighbor.
        if idx - 1 >= 0 and self.blocks[idx - 1].is_free:
            left = self.blocks[idx - 1]
            left.size += self.blocks[idx].size
            self.blocks.pop(idx)
            self.merges += 1

    def used(self) -> int:
        """Sum of the sizes of the occupied blocks."""
        return sum(b.size for b in self.blocks if not b.is_free)

    def largest_gap(self) -> int:
        free = [b.size for b in self.blocks if b.is_free]
        return max(free) if free else 0

    def free_space(self) -> int:
        return sum(b.size for b in self.blocks if b.is_free)
