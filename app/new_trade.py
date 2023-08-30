from classes.portfolio import Portfolio
from rich.console import Console
from app.prompts.prompt_input import PromptInput
from app.prompts.validators import DateValidator

EXCHANGES = ["NYSE", "MIL", "NDQ"]
BROKERS = ["IBKR", "Degiro"]
CURRENCIES = ["USD", "EUR"]
ACTIONS = ["buy", "sell"]


class NewTradePrompter:
    """Page to create a new trade"""

    def __init__(self, portfolio: Portfolio, console: Console) -> None:
        self.portfolio = portfolio
        self.console = console

    def run(self):
        # date, ticker, exchange, broker, currency, action, amount, price, transaction costs, notes+
        date = PromptInput(
            self.console, "Date (yyyy-mm-dd): ", DateValidator
        ).run()

        print(date)

        trade_data = {}

        self.portfolio.new_trade(trade_data)
