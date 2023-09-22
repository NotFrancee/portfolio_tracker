from exceptions import MissingRequiredParams
import pandas as pd


class Trade:
    """Trade class"""

    required_params = {
        "date",
        "ticker",
        "exchange",
        "broker",
        "action",
        "currency",
        "amount",
        "price",
        "transaction_costs",
    }

    to_row_columns = {
        "date": "Date",
        "ticker": "Ticker",
        "exchange": "Exchange",
        "broker": "Broker",
        "action": "Action",
        "amount": "Amount",
        "currency": "Currency",
        "price": "Price",
        "transaction_costs": "Transaction Costs",
        "cost_basis": "Cost Basis",
        "unit_cost_basis": "Unit Cost Basis",
    }

    def __init__(self, trade_data: dict[str, str]):
        if not self.required_params.issubset(set(trade_data)):
            raise MissingRequiredParams(self.required_params, set(trade_data))

        self.date = trade_data["date"]
        self.ticker = trade_data["ticker"]
        self.exchange = trade_data["exchange"]
        self.broker = trade_data["broker"]
        self.action = trade_data["action"].lower()
        self.amount = float(trade_data["amount"])
        self.currency = trade_data["currency"]
        self.price = float(trade_data["price"])
        self.transaction_costs = float(trade_data["transaction_costs"])

        self.trade_data = trade_data

        cost_basis = self.amount * self.price
        if self.action == "sell":
            cost_basis -= self.transaction_costs
        else:
            cost_basis += self.transaction_costs
        self.cost_basis = cost_basis

        self.unit_cost_basis = self.cost_basis / self.amount

    def __str__(self) -> str:
        res = []
        res.append(
            f"Summary for {self.ticker} {self.action.upper()} trade on {self.date}"
        )
        res.append(
            f"{self.amount} @ {self.currency} {self.price} (transaction costs: {self.transaction_costs})"
        )
        res.append(
            f"\tTotal Cost Basis: {self.cost_basis}\n\tUnit Cost Basis: {self.unit_cost_basis}"
        )

        return "\n".join(res)

    def to_row(self) -> list:
        res = [getattr(self, key) for key in self.to_row_columns]

        return res

    @staticmethod
    def trades_to_df(trades: list) -> pd.DataFrame:
        trades_rows = [trade.to_row() for trade in trades]
        trades_df = pd.DataFrame(trades_rows, columns=Trade.to_row_columns)
        trades_df = trades_df.set_index("date")
        trades_df.loc[:, "open_amount"] = trades_df["amount"]

        return trades_df
