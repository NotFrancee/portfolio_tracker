from trade_class import Trade


class Position:
    """Position Object"""

    to_row_columns = {
        "ticker": "Ticker",
        "amount": "Amount",
        "cost_basis": "Cost Basis",
        "unit_cost_basis": "Unit Cost Basis",
        "realized_pnl": "Realized PnL",
    }

    def __init__(self, ticker: str, initial_trades: list[Trade]):
        self.ticker = ticker
        self.trades = initial_trades

        self.pos_amount = 0
        self.total_cost = 0
        self.average_cost = 0

        self.realized_pnl = 0

        self.refresh()

    def compute_position_data(self):
        pos_amount = 0
        total_cost = 0
        realized_pnl = 0

        for trade in self.trades:
            if trade.action.lower() == "buy":
                pos_amount += trade.amount
                total_cost += trade.price * trade.amount
            else:
                pos_amount -= trade.amount
                # how to do that?
                # realized_pnl += trade.amount *
                # realized profit

        self.pos_amount = pos_amount
        self.total_cost = total_cost
        self.average_cost = total_cost / pos_amount
        self.realized_pnl = realized_pnl

    def refresh(self):
        print("refreshing position...", end="")
        self.compute_position_data()
        print("...done")

    def __str__(self) -> str:
        res = f"Summary for Position on {self.ticker}"

        data = [
            f"Amount: {self.pos_amount}",
            f"Cost: {self.total_cost}",
            f"Avg Cost: {self.average_cost}",
            "Value: WIP",
            "Summary of Trades",
        ]

        trades_str = [str(trade) for trade in self.trades]

        return "\n".join([res] + data + trades_str)

    def to_row(self):
        res = [getattr(self, key) for key in self.to_row_columns]

        return res
