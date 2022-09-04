from abc import ABC, abstractmethod
from .dataclasses import Balance
from .typing import ExchangeConfig

"""
ROCK — RObotrade Ccxt Killer
"""


class Exchange(ABC):
    @abstractmethod
    def __init__(self, config: ExchangeConfig):
        ...

    @abstractmethod
    async def init(self) -> None:
        """
        Инициализировать асинхронные соединения
        """
        ...

    @abstractmethod
    async def watch_balance(self) -> Balance:
        """
        Получить обновление баланса
        """
        ...

    @abstractmethod
    async def watch_orders(self) -> dict:
        """
        Получить обновление ордеров
        """
        ...
