from classes.position import Position
from classes.trade import Trade
from market_interface import MarketInterface
from dotenv import load_dotenv
import pandas as pd

class Portfolio:
    """Portfolio Class

    Initializing pulls the trades from the xlsx file named "portfolio.xlsx"
    """

    def __init__(self):
        load_dotenv()
        self.market_interface = MarketInterface()

        self.trades = self._load_trades('trades.csv')
        self.positions = self._load_positions()

        self.update_live_data()

    def _load_trades(self, path: str): 
        # loads the trades from the csv
        trades = pd.read_csv(path)

        # converts the columns to lowercase and the actions to strings
        trades.columns = [col.lower().replace(' ', '_').strip() for col in trades.columns]
        trades['action'] = trades['action'].apply(lambda x: x.lower())
        trades['open_amount'] = trades['amount']

        return trades

    def _load_positions(self):
        trades = self.trades
        positions = {}

        # finds all the tickers
        tickers = trades["ticker"].unique()

        for ticker in tickers:
            # filters all the trades for that ticker and creates the position
            ticker_trades = trades[trades["ticker"] == ticker]
            position = Position(ticker, ticker_trades)

            positions[ticker] = position

        print("\tcomputed positions...")
        return positions

    def update_live_data(self):
        print("\tupdating mkt prices...")

        print('wip, TODO')
        return
        tickers = list(self.positions.keys())

        price_data = self.market_interface.get_stocks_prices(
            tickers, start="2020-1-1"
        )

        for ticker, position in self.positions.items():
            current_price = price_data.iloc[-1].loc[ticker, :]

            position.update_mkt_value(current_price)
