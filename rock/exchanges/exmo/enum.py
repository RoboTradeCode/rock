from enum import Enum


class EventType(str, Enum):
    UPDATE = "update"
    SNAPSHOT = "snapshot"


class OrderStatus(str, Enum):
    OPEN = "open"
    EXECUTING = "executing"
    CANCELLED = "cancelled"


class OrderType(str, Enum):
    BUY = "buy"
    SELL = "sell"
    MARKET_BUY = "market_buy"
    MARKET_SELL = "market_sell"
    MARKET_BUY_TOTAL = "market_buy_total"
    MARKET_SELL_TOTAL = "market_sell_total"
