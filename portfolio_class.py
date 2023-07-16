from data_handler import DataHandler
from position_class import Position
from trade_class import Trade


class Portfolio:
    """Portfolio Class

    Initializing pulls the trades from the xlsx file named "portfolio.xlsx"
    """

    def __init__(self):
        self.data_handler = DataHandler("portfolio.xlsx")

        self.trades = self.data_handler.retrieve_trades()
        self.positions: dict[str, Position] = {}

    def compute_positions(self):
        trades_df = Trade.trades_to_df(self.trades)

        tickers = trades_df["ticker"].unique()

        for ticker in tickers:
            ticker_trades = trades_df[trades_df["ticker"] == ticker]
            position = Position(ticker, ticker_trades)

            self.positions[ticker] = position

        self.data_handler.dump_positions(self.positions.values())

        print("updated positions!")
