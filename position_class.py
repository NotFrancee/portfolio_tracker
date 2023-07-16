from trade_class import Trade
import pandas as pd


class Position:
    """Position Object"""

    to_row_columns = {
        "ticker": "Ticker",
        "amount": "Amount",
        "cost_basis": "Cost Basis",
        "unit_cost_basis": "Unit Cost Basis",
        "realized_pnl": "Realized PnL",
    }

    def __init__(self, ticker: str, initial_trades: pd.DataFrame):
        # initialize trades df

        # self.trades = trades_to_df(initial_trades)
        self.trades = initial_trades

        self.ticker = ticker
        self.amount = 0
        self.cost_basis = 0
        self.unit_cost_basis = 0
        self.unrealized_pnl = 0
        self.realized_pnl = 0

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
            print("analyzing one of the previous trades")
            print(f"\tremaining quantity: {remaining_quantity}")
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
        print(past_buy_trades)

    def _initialize_position_data(self):
        print(f"initializing position data for {self.ticker}...")
        print(self.trades)

        for trade in self.trades.itertuples():
            if trade.action == "buy":
                self._handle_buy_trade(trade)
            elif trade.action == "sell":
                self._handle_sell_trade(trade)
            else:
                print("invalid action")

    def new_trade(self, trade: Trade):
        self.trades_df.loc[trade.date] = trade.to_row()

        self.refresh()

    def refresh(self):
        print("refreshing position...", end="")
        self._initialize_position_data()
        print("...done")

    def __str__(self) -> str:
        res = f"Summary for Position on {self.ticker}"

        data = [
            f"Amount: {self.amount}",
            f"Cost Basis: {self.cost_basis}",
            f"Unit Cost Basis: {self.unit_cost_basis}",
            f"Real. PnL: {self.realized_pnl}",
            f"Unreal. PnL: {self.unrealized_pnl}",
            "Value: WIP",
        ]

        # trades_str = [str(trade) for trade in self.trades.iterrows()]

        return "\n".join([res] + data)

    def to_row(self):
        res = [getattr(self, key) for key in self.to_row_columns]

        return res
