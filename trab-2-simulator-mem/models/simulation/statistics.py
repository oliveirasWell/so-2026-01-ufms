from dataclasses import dataclass, field


@dataclass
class Statistics:
    total_events: int = 0
    allocated: int = 0
    freed: int = 0
    freed_missing: int = 0
    external_fragmentation_failures: int = 0
    no_space_failures: int = 0
    usage_per_event: list[int] = field(default_factory=list)
    merges: int = 0
