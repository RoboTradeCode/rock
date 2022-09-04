from decimal import Decimal
from typing import TypedDict, Optional


class ExchangeConfig(TypedDict):
    api_key: Optional[str]
    api_secret: Optional[str]


class Asset(TypedDict):
    free: Decimal
    used: Decimal
    total: Decimal
