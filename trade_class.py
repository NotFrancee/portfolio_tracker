from exceptions import MissingRequiredParams
import pandas as pd


class Trade:
    """Trade class"""

    required_params = {
        "date",
        "ticker",
        "action",
        "amount",
        "price",
        "transaction_costs",
    }

    to_row_columns = {
        "date": "Date",
        "ticker": "Ticker",
        "action": "Action",
        "amount": "Amount",
        "price": "Price",
        "transaction_costs": "Transaction Costs",
        "cost_basis": "Cost Basis",
        "unit_cost_basis": "Unit Cost Basis",
    }

    def __init__(self, trade_data: dict[str, str]):
        if not self.required_params.issubset(set(trade_data)):
            raise Exception("you did not provide the required params")

        self.date = trade_data["date"]
        self.ticker = trade_data["ticker"]
        self.action = trade_data["action"].lower()
        self.amount = float(trade_data["amount"])
        self.price = float(trade_data["price"])
        self.commissions = float(trade_data["commissions"])

        self.trade_data = trade_data

    def __str__(self) -> str:
        return "\n".join(
            [f"{key}: {value}" for key, value in self.trade_data.items()]
        )

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
