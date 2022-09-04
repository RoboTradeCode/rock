from abc import ABC, abstractmethod
from .enum import EventType


class Formatter(ABC):
    @classmethod
    def format(cls, event: dict):
        match event.get("event"):
            case EventType.SNAPSHOT:
                formatted = cls._from_snapshot(event)
            case EventType.UPDATE:
                formatted = cls._from_update(event)
            case _:
                raise ValueError(f"Unsupported event: {event}")

        return formatted

    @staticmethod
    @abstractmethod
    def _from_snapshot(event: dict):
        ...

    @staticmethod
    @abstractmethod
    def _from_update(event: dict):
        ...
