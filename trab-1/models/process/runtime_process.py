from dataclasses import dataclass

from models.process.process import Process


@dataclass
class RuntimeProcess:
    process: Process
    burst_index: int = 0
    cpu_remaining: int = 0
    io_remaining: int = 0
    finish: int | None = None

    @property
    def pid(self) -> str:
        return self.process.pid
