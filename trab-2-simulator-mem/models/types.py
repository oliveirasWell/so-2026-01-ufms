"""Shared type aliases for the simulator."""

from collections.abc import Callable

from models.memory.memory import Memory
from models.simulation.event_result import EventResult

# A gap-choosing strategy: given the memory and a request size, return the
# index of the chosen gap, or None when no gap fits.
ChooseFunction = Callable[[Memory, int], int | None]

# Per-event callback: (1-based event number, classified result, current memory).
OnEvent = Callable[[int, EventResult, Memory], None]
