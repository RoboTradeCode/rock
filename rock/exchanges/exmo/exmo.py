from typing import Callable
from websockets import ConnectionClosed
from .enum import EventType
from .formatters import BalanceFormatter, OrdersFormatter
from .websocket import Websocket
from ..abc import Exchange
from ..dataclasses import Balance, Order
from ..typing import ExchangeConfig
from asyncio import Lock

GENERAL_ENDPOINT = "ws-api.exmo.com"


def reconnect(io: Callable) -> Callable:
    async def wrapped(self, *args, **kwargs):
        for _ in range(3):
            try:
                return await io(self, *args, **kwargs)
            except ConnectionClosed:
                await self.init()

    return wrapped


class Exmo(Exchange):
    def __init__(self, config: ExchangeConfig):
        _uri = f"wss://{GENERAL_ENDPOINT}/v1/private"
        _api_key = config["api_key"]
        _api_secret = config["api_secret"]

        self.balance_client = Websocket(_uri, _api_key, _api_secret)
        self.orders_client = Websocket(_uri, _api_key, _api_secret)
        self._lock = Lock()

    async def init(self) -> None:
        """
        Инициализировать асинхронные соединения
        """
        # TODO: Разделить инициализацию разных сокетов
        async with self._lock:
            await self._connect()
            await self._login()
            await self._subscribe()

    @reconnect
    async def watch_balance(self) -> Balance:
        """
        Получить обновление баланса
        """
        while event := await self.balance_client.recv():
            if event.get("event") in [EventType.SNAPSHOT, EventType.UPDATE]:
                balance = BalanceFormatter.format(event)
                return balance

    @reconnect
    async def watch_orders(self) -> list[Order]:
        """
        Получить обновление ордеров
        """
        while event := await self.orders_client.recv():
            if event.get("event") in [EventType.SNAPSHOT, EventType.UPDATE]:
                orders = OrdersFormatter.format(event)
                return orders

    async def _connect(self) -> None:
        """
        Установить соединение с сервером
        """
        await self.balance_client.connect()
        await self.orders_client.connect()

    async def _login(self) -> None:
        """
        Аутентифицироваться на сервере
        """
        await self.balance_client.login()
        await self.orders_client.login()

    async def _subscribe(self) -> None:
        """
        Подписаться на получение данных
        """
        await self.balance_client.subscribe(["spot/wallet"])
        await self.orders_client.subscribe(["spot/orders"])
