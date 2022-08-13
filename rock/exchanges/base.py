from abc import ABC, abstractmethod
from .types import ExchangeConfig

"""
ROCK — RObotrade Ccxt Killer
"""


# TODO: Add REST commands
# TODO: Use dataclasses as return type
class Exchange(ABC):
    @abstractmethod
    def __init__(self, config: ExchangeConfig):
        ...

    @abstractmethod
    async def watch_order_book(self, symbol: str, limit: int) -> dict:
        ...

    @abstractmethod
    async def watch_balance(self) -> dict:
        ...

    @abstractmethod
    async def watch_order(self) -> dict:
        ...
