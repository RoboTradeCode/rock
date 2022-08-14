from rock.exchanges.base import Exchange
from rock.exchanges.types import ExchangeConfig
from websockets import WebSocketClientProtocol


class Exmo(Exchange):
    def __init__(self, config: ExchangeConfig):
        self.config = config
        self.clients: dict[str, WebSocketClientProtocol] = {}

    async def get_order_book_update(self, symbol: str, limit: int) -> dict:
        ...

    async def get_balance_update(self) -> dict:
        ...

    async def get_order_update(self) -> dict:
        ...
