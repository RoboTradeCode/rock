from .exchanges import Exchange, Exmo
from .exchanges.enum import ExchangeName
from .exchanges.typing import ExchangeConfig


class ExchangeFactory:
    @staticmethod
    def create_exchange(name: ExchangeName, config: ExchangeConfig) -> Exchange:
        match name:
            case ExchangeName.EXMO:
                exchange = Exmo(config)
            case _:
                raise ValueError(f"Unsupported exchange: {name}")

        return exchange
