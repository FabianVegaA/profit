from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from itertools import product
from functools import reduce
import operator


class StockBase(ABC):
    name: str

    @abstractmethod
    def price(self, date: datetime) -> Decimal:
        pass


@dataclass
class Portfolio[Stock: StockBase]:
    stocks: list[Stock]

    def profit(self, start: datetime, end: datetime) -> Decimal:
        return sum(
            (stock.price(end) - stock.price(start) for stock in self.stocks),
            start=Decimal(0),
        )

    def annual_profit(self, start: datetime, end: datetime) -> Decimal:
        years = Decimal((end - start).days / 365.25)
        return (
            reduce(
                operator.mul,
                (
                    (1 + (stock.price(end) - stock.price(start) / stock.price(start))) ** (1 / years)
                    for stock in self.stocks
                ),
            )
            - 1
        )
