from enum import StrEnum


class EventType(StrEnum):
    ALLOC = "ALLOC"
    FREE = "FREE"
