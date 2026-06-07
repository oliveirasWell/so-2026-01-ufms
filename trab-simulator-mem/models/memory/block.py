from dataclasses import dataclass


@dataclass
class Block:
    start: int
    size: int
    pid: str | None  # None => gap (free)

    @property
    def end(self) -> int:
        # Position right after the block's last byte (interval [start, end)).
        return self.start + self.size

    @property
    def is_free(self) -> bool:
        return self.pid is None
