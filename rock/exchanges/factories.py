from .base import Exchange
from .enums import ExchangeName
from .exmo.exmo import Exmo
from .types import ExchangeConfig


class ExchangeFactory:
    @staticmethod
    def create_exchange(name: ExchangeName, config: ExchangeConfig) -> Exchange:
        match name:
            case ExchangeName.EXMO:
                exchange = Exmo(config)
            case _:
                raise ValueError(f"Unsupported exchange: {name}")

        return exchange
