"""Shared type aliases for the simulator."""

from collections.abc import Callable

from models.memory.memory import Memory

# A gap-choosing strategy: given the memory and a request size, return the
# index of the chosen gap, or None when no gap fits.
ChooseFunction = Callable[[Memory, int], int | None]
