class Trade:
    """Trade class"""

    required_params = {
        "date",
        "ticker",
        "action",
        "amount",
        "price",
        "commissions",
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
