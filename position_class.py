import pandas as pd


class Position:
    """Position Object"""

    to_row_columns = {
        "ticker": "Ticker",
        "broker": "Broker",
        "amount": "Amount",
        "cost_basis": "Cost Basis",
        "unit_cost_basis": "Unit Cost Basis",
        "last_price": "Last Price",
        "mkt_value": "Market Value",
        "realized_pnl": "Realized PnL",
    }

    def __init__(self, ticker: str, broker: str, initial_trades: pd.DataFrame):
        # self.trades = trades_to_df(initial_trades)
        self.trades = initial_trades.drop("ticker", axis=1)

        self.ticker = ticker
        self.amount = 0
        self.cost_basis = 0
        self.unit_cost_basis = 0
        self.unrealized_pnl = 0
        self.realized_pnl = 0
        self.broker = broker

        self.last_price = None
        self.mkt_value = None

        self._initialize_position_data()

    def _handle_buy_trade(self, trade):
        self.cost_basis += trade.cost_basis
        self.amount += trade.amount

    def _handle_sell_trade(self, trade):
        past_buy_trades: pd.DataFrame = self.trades[
            (self.trades.index < trade.Index)
            & (self.trades["action"] == "buy")
            & (self.trades["open_amount"] > 0)
        ]

        remaining_quantity = trade.amount

        for previous_trade in past_buy_trades.itertuples():
            if previous_trade.amount <= remaining_quantity:
                past_buy_trades.loc[previous_trade.Index, "open_amount"] = 0

                remaining_quantity -= previous_trade.amount

                # book PnL
                self.cost_basis -= previous_trade.cost_basis
                trade_pnl = trade.cost_basis - previous_trade.cost_basis
                self.realized_pnl += trade_pnl
                self.unrealized_pnl -= trade_pnl

            else:
                past_buy_trades.loc[
                    previous_trade.Index, "open_amount"
                ] -= remaining_quantity

                self.cost_basis -= previous_trade.price * remaining_quantity
                trade_pnl = (
                    trade.cost_basis - previous_trade.price * remaining_quantity
                )
                self.realized_pnl += trade_pnl
                self.unrealized_pnl -= trade_pnl

                remaining_quantity = 0

                # book PnL

                break

        self.amount -= trade.amount
        self.unit_cost_basis = self.cost_basis / self.amount

    def _initialize_position_data(self):
        for trade in self.trades.itertuples():
            if trade.action == "buy":
                self._handle_buy_trade(trade)
            elif trade.action == "sell":
                self._handle_sell_trade(trade)
            else:
                print("invalid action")

    def update_mkt_value(self, price_data):
        current_price = price_data["close"]
        self.last_price = current_price
        self.mkt_value = current_price * self.amount

    def __str__(self) -> str:
        res = []
        res.append(f"Summary for Position on {self.ticker}")

        res += [
            f"Amount: {self.amount}",
            f"Cost Basis: {self.cost_basis}",
            f"Unit Cost Basis: {self.unit_cost_basis}",
            f"Real. PnL: {self.realized_pnl}",
            f"Unreal. PnL: {self.unrealized_pnl}",
            f"Last Price: {self.last_price}",
            f"Mkt Value: {self.mkt_value}",
            "TRADES SUMMARY",
        ]

        res.append(self.trades.to_string())

        return "\n".join(res)

    def to_row(self):
        res = [getattr(self, key) for key in self.to_row_columns]

        return res
