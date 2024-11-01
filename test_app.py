from collections.abc import Iterator, Sequence
from unittest import TestCase
from faker import Faker
from typing import NamedTuple
from contextlib import suppress
from datetime import datetime, timedelta
from dataclasses import dataclass
from decimal import Decimal

from app import StockBase, Portfolio

faker = Faker()


class StockData(NamedTuple):
    price: Decimal
    date: datetime


@dataclass
class MockedStock(StockBase):
    name: str
    ordered_prices: Sequence[StockData]

    def price(self, date: datetime) -> Decimal:
        with suppress(KeyError):
            return {stock_data.date: stock_data.price for stock_data in self.ordered_prices}[date]
        raise ValueError(f"Stock price not found for date {date}")


def stock_data_generator(profit: Decimal, start_date: datetime, end_date: datetime) -> Iterator[StockData]:
    initial_price, date = Decimal(0), start_date
    yield StockData(price=initial_price, date=date)
    while date < end_date - timedelta(days=1):
        date += timedelta(days=1)
        yield StockData(price=faker.pydecimal(), date=date)
    yield StockData(price=initial_price + profit, date=end_date)


class TestStockDataGenerator(TestCase):
    def test_stock_data_generator(self):
        start_date, end_date = datetime(2021, 1, 1), datetime(2021, 1, 2)
        stock_data = list(stock_data_generator(Decimal("2.00"), start_date, end_date))
        self.assertSequenceEqual(
            stock_data,
            [
                StockData(price=Decimal(0), date=start_date),
                StockData(price=Decimal("2.00"), date=end_date),
            ],
        )


class TestStockBase(TestCase):
    def test_stock_base(self):
        stock = MockedStock(
            name="AAPL",
            ordered_prices=list(stock_data_generator(Decimal(2), datetime(2021, 1, 1), datetime(2021, 1, 2))),
        )
        self.assertEqual(stock.price(datetime(2021, 1, 1)), Decimal(0))
        self.assertEqual(stock.price(datetime(2021, 1, 2)), Decimal(2))


class TestPorfolio(TestCase):
    def __case_portfolio(
        self, range_dates: tuple[datetime, datetime]
    ) -> Iterator[tuple[Portfolio[MockedStock], Decimal]]:
        yield Portfolio(stocks=[]), Decimal(0)
        yield (
            Portfolio(
                stocks=[
                    MockedStock(
                        name="AAPL",
                        ordered_prices=list(stock_data_generator(Decimal(2), *range_dates)),
                    )
                ]
            ),
            Decimal(2),
        )
        yield (
            Portfolio(
                stocks=[
                    MockedStock(
                        name="AAPL",
                        ordered_prices=list(stock_data_generator(Decimal(3), *range_dates)),
                    ),
                    MockedStock(
                        name="GOOGL",
                        ordered_prices=list(stock_data_generator(Decimal(3), *range_dates)),
                    ),
                ]
            ),
            Decimal(6),
        )
        yield (
            Portfolio(
                stocks=[
                    MockedStock(
                        name="AAPL",
                        ordered_prices=list(stock_data_generator(Decimal(-1), *range_dates)),
                    )
                ]
            ),
            Decimal(-1),
        )

    def test_portfolio(self):
        range_dates = datetime(2021, 1, 1), datetime(2021, 1, 2)
        for portfolio, expected_profit in self.__case_portfolio(range_dates):
            with self.subTest(portfolio=portfolio, expected_profit=expected_profit):
                self.assertEqual(
                    portfolio.profit(*range_dates),
                    expected_profit,
                )
