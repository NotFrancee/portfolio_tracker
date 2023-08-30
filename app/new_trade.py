from classes.portfolio import Portfolio
from rich.console import Console
from app.prompt_input import PromptInput, Validator


EXCHANGES = ["NYSE", "MIL", "NDQ"]
BROKERS = ["IBKR", "Degiro"]
CURRENCIES = ["USD", "EUR"]
ACTIONS = ["buy", "sell"]


class DateValidator(Validator):
    def validate(self, input: str):
        return True

    def process(self, input_str: str):
        return True


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
