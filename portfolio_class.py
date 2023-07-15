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

    def create_new_position(self, initial_trade: Trade):
        ticker = initial_trade.ticker
        position = Position(ticker, initial_trades=[initial_trade])

        self.positions[ticker] = position

    def update_position(self, trade: Trade):
        position = self.positions[trade.ticker]

        # TODO

    def compute_positions(self):
        trades = self.trades
        if len(trades) == 0:
            print("there are no trades.")
            return

        for trade in trades:
            if trade.ticker in self.positions:
                self.update_position(trade)
            else:
                self.create_new_position(trade)

        self.data_handler.dump_positions(self.positions.values())

        print("updated positions!")
