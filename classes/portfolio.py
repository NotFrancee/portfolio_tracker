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

        self.trades = self._load_trades("trades.csv")
        self.positions: dict[str, Position] = self._load_positions()

        self.update_live_data()

    def _load_trades(self, path: str):
        # loads the trades from the csv
        trades = pd.read_csv(path)

        # converts the columns to lowercase and the actions to strings
        trades.columns = [
            col.lower().replace(" ", "_").strip() for col in trades.columns
        ]
        trades["action"] = trades["action"].apply(lambda x: x.lower())
        trades["open_amount"] = trades["amount"]

        return trades

    def _load_positions(self):
        trades = self.trades
        positions = {}

        # finds all the tickers
        tickers: list[str] = trades["ticker"].unique()

        for ticker in tickers:
            # filters all the trades for that ticker and creates the position
            ticker_trades = trades[trades["ticker"] == ticker]
            position = Position(ticker, ticker_trades)

            positions[ticker] = position

        print("\tcomputed positions...")
        return positions

    # TODO
    def update_live_data(self):
        print("\tupdating mkt prices...")

        tickers = list(self.positions.keys())

        price_data = self.market_interface.get_stocks_prices(
            tickers, start="2020-1-1"
        )

        for ticker, position in self.positions.items():
            current_price = price_data.iloc[-1].loc[ticker, :]

            position.update_mkt_value(current_price)

    def generate_positions_df(self):
        df_base = {
            ticker: position.to_row()
            for ticker, position in self.positions.items()
        }

        df = pd.DataFrame(
            df_base.values(),
            index=df_base.keys(),
            columns=Position.to_row_columns.values(),
        )

        return df.drop("Ticker", axis=1)

    # TODO
    def display_summary(self):
        print("PORTFOLIO SUMMARY")

        positions_df = self.generate_positions_df()

        print(positions_df.to_string())

    def new_trade(self, trade_data):
        trade = Trade(trade_data)
        print(self.trades)
        print("total cols: ", len(self.trades.columns))
        print("total cols: ", len(trade.to_row()))
        print("now adding\n", trade)

        self.trades.add(trade.to_row())

        print(self.trades)

    def calculate_portfolio_value(self):
        cost_basis = 0
        market_value = 0
        real_pnl = 0

        for position in self.positions.values():
            print(position)
            cost_basis += position.cost_basis
            market_value += position.mkt_value
            real_pnl += position.realized_pnl

        unrealized_pnl = market_value - real_pnl

        return cost_basis, market_value, unrealized_pnl, real_pnl

    def load_hist_data(self):
        try:
            with open("portfolio_hist_data.pickle", "rb") as f:
                data = pickle.load(f)
        except:
            data = {}

        return data

    def dump_daily_data(self):
        data = self.load_hist_data()
        self.update_live_data()
        (
            cost_basis,
            market_value,
            unrealized_pnl,
            real_pnl,
        ) = self.calculate_portfolio_value()

        portfolio_data = {
            "positions": {
                ticker: position.to_dict()
                for ticker, position in self.positions.items()
            },
            "portfolio_value": market_value,
            "cost_basis": cost_basis,
            "realized_pnl": real_pnl,
            "unrealized_pnl": unrealized_pnl,
        }

        today = pd.Timestamp.today().date()

        with open("portfolio_hist_data.pickle", "ab") as f:
            data[today.strftime("%Y-%m-%d")] = portfolio_data

            pickle.dump(data, f)
            print("Dumped Data\n", data)
