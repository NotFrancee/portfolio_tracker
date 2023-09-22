import pandas as pd
import json
import os
from excel_interface import ExcelInterface
from classes.position import Position
from classes.trade import Trade
from market_interface import MarketInterface
from dotenv import load_dotenv


class Portfolio:
    """Portfolio Class

    Initializing pulls the trades from the xlsx file named "portfolio.xlsx"
    """

    def __init__(self):
        load_dotenv()
        self.data_handler = ExcelInterface("portfolio.xlsx")
        self.market_interface = MarketInterface()

        self.trades = self.data_handler.retrieve_trades()
        self.positions: dict[str, Position] = {}

        self._initialize_portfolio()

    def _initialize_portfolio(self):
        print("initializing portfolio...")
        self.compute_positions()
        self.update_live_prices()
        self.data_handler.dump_positions(self.positions.values())
        print("...initialized portfolio!")

    def compute_positions(self):
        trades_df = Trade.trades_to_df(self.trades)

        tickers = trades_df["ticker"].unique()

        for ticker in tickers:
            ticker_trades = trades_df[trades_df["ticker"] == ticker]
            exchange = ticker_trades["exchange"][0]
            currency = ticker_trades["currency"][0]
            broker = ticker_trades["broker"][0]

            position = Position(
                ticker, exchange, broker, currency, ticker_trades
            )

            self.positions[ticker] = position

        print("\tcomputed positions...")

    def update_live_prices(self):
        print("\tupdating mkt prices...")
        tickers = list(self.positions.keys())

        price_data = self.market_interface.get_stocks_prices(
            tickers, start="2020-1-1"
        )

        for ticker, position in self.positions.items():
            current_price = price_data.iloc[-1].loc[ticker, :]

            position.update_mkt_value(current_price)

    def _create_portfolio_snapshot(self, portfolio_history: dict[str, str]):
        self.update_live_prices()

        date = pd.Timestamp.today().strftime("%m/%d/%y")

        positions_data = {
            key: position.to_dict() for key, position in self.positions.items()
        }

        portfolio_history[date] = positions_data

    def update_portfolio_history(self):
        try:
            with open("portfolio_history.json", "r+", encoding="utf-8") as f:
                portfolio_history = json.load(f)
                self._create_portfolio_snapshot(portfolio_history)

                json.dump(portfolio_history, f)

        except FileNotFoundError:
            with open("portfolio_history.json", "w", encoding="utf-8") as f:
                portfolio_history = dict()
                self._create_portfolio_snapshot(portfolio_history)

                json.dump(portfolio_history, f)

    def reset_portfolio_history(self):
        os.remove("./portfolio_history.json")
        print("successfully reset portfolio history.")
