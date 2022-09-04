from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from .enum import OrderStatus, OrderType, OrderSide
from .typing import Asset


@dataclass
class Balance:
    assets: dict[str, Asset]
    timestamp: datetime


@dataclass
class Order:
    id: str
    client_order_id: str
    timestamp: datetime
    status: OrderStatus
    symbol: str
    type: OrderType
    side: OrderSide
    price: Decimal
    amount: Decimal
    filled: Decimal
