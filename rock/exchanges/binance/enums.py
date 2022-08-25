from enum import Enum, IntEnum


class EventCode(IntEnum):
    MAINTENANCE_IN_PROGRESS = 2


class EventType(str, Enum):
    INFO = "info"
    LOGGED_IN = "logged_in"
    SUBSCRIBED = "subscribed"
    UPDATE = "update"
    SNAPSHOT = "snapshot"
    ERROR = "error"
