from decimal import Decimal
from .abc import Formatter
from .datetime import datetime_from_ms
from .enum import OrderStatus as ExmoOrderStatus
from .enum import OrderType as ExmoOrderType
from ..dataclasses import Balance, Order
from ..enum import OrderSide as BaseOrderSide
from ..enum import OrderStatus as BaseOrderStatus
from ..enum import OrderType as BaseOrderType
from ..typing import Asset


class BalanceFormatter(Formatter):
    @staticmethod
    def _from_snapshot(event: dict) -> Balance:
        assets = {}
        for currency, free in event["data"]["balances"].items():
            free = Decimal(free)
            used = Decimal(event["data"]["reserved"][currency])
            total = free + used
            assets[currency] = Asset(free=free, used=used, total=total)

        timestamp = datetime_from_ms(event["ts"])
        return Balance(assets, timestamp)

    @staticmethod
    def _from_update(event: dict) -> Balance:
        currency = event["data"]["currency"]
        free = Decimal(event["data"]["balance"])
        used = Decimal(event["data"]["reserved"])
        total = free + used

        assets = {currency: Asset(free=free, used=used, total=total)}
        timestamp = datetime_from_ms(event["ts"])
        return Balance(assets, timestamp)


class OrdersFormatter(Formatter):
    @staticmethod
    def _from_snapshot(event: dict) -> list[Order]:
        orders = [OrdersFormatter._order(event["ts"], data) for data in event["data"]]
        return orders

    @staticmethod
    def _from_update(event: dict) -> list[Order]:
        orders = [OrdersFormatter._order(event["ts"], event["data"])]
        return orders

    @staticmethod
    def _order(ts: int, data: dict) -> Order:
        client_order_id = str(data["client_id"])
        timestamp = datetime_from_ms(ts)
        order_status = OrdersFormatter._status(data["status"])
        symbol = data["pair"].replace("_", "/")
        order_type, order_side = OrdersFormatter._type_side(data["type"])
        price = Decimal(data["price"])
        amount = Decimal(data["original_quantity"])
        filled = amount - Decimal(data["quantity"])

        order = Order(
            id=data["order_id"],
            client_order_id=client_order_id,
            timestamp=timestamp,
            status=order_status,
            symbol=symbol,
            type=order_type,
            side=order_side,
            price=price,
            amount=amount,
            filled=filled,
        )
        return order

    @staticmethod
    def _status(exmo_status: ExmoOrderStatus) -> BaseOrderStatus:
        match exmo_status:
            case ExmoOrderStatus.OPEN:
                order_status = BaseOrderStatus.OPEN
            case ExmoOrderStatus.EXECUTING:
                order_status = BaseOrderStatus.OPEN
            case ExmoOrderStatus.CANCELLED:
                order_status = BaseOrderStatus.CLOSED
            case _:
                raise ValueError(f"Unsupported status: {exmo_status}")

        return order_status

    @staticmethod
    def _type_side(exmo_type: ExmoOrderType) -> tuple[BaseOrderType, BaseOrderSide]:
        match exmo_type:
            case ExmoOrderType.BUY:
                order_type, order_side = BaseOrderType.LIMIT, BaseOrderSide.BUY
            case ExmoOrderType.SELL:
                order_type, order_side = BaseOrderType.LIMIT, BaseOrderSide.SELL
            case ExmoOrderType.MARKET_BUY:
                order_type, order_side = BaseOrderType.MARKET, BaseOrderSide.BUY
            case ExmoOrderType.MARKET_SELL:
                order_type, order_side = BaseOrderType.MARKET, BaseOrderSide.SELL
            case ExmoOrderType.MARKET_BUY_TOTAL:
                order_type, order_side = BaseOrderType.MARKET, BaseOrderSide.BUY
            case ExmoOrderType.MARKET_SELL_TOTAL:
                order_type, order_side = BaseOrderType.MARKET, BaseOrderSide.SELL
            case _:
                raise ValueError(f"Unsupported type: {exmo_type}")

        return order_type, order_side
