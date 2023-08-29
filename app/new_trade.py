from classes.portfolio import Portfolio


from rich.markdown import Markdown
from rich.console import Console
import six
from abc import ABCMeta, abstractmethod


@six.add_metaclass(ABCMeta)
class Validator:
    def __init__(self) -> None:
        pass

    @abstractmethod
    def validate(self, input: str):
        """You must override this function. Return false is not valid, True if valid"""
        pass


class Prompt:
    """Prompt Class"""

    def __init__(
        self,
        console: Console,
        prompt_md: str,
        input_type: type,
        validator: Validator,
    ) -> None:
        self.console = console
        self.prompt = Markdown(prompt_md)
        self.input_type = input_type
        self.validator = validator

    def run(self):
        inp = self.console.input(self.prompt)

        is_valid = self.validator.validate(inp)

        if is_valid:
            return self.input_type(inp)
        else:
            print("an error occurred")


EXCHANGES = ["NYSE", "MIL", "NDQ"]
BROKERS = ["IBKR", "Degiro"]
CURRENCIES = ["USD", "EUR"]
ACTIONS = ["buy", "sell"]


class NewTradePrompter:
    def __init__(self, portfolio: Portfolio) -> None:
        self.portfolio = portfolio

    def run(self):
        # date, ticker, exchange, broker, currency, action, amount, price, transaction costs, notes

        trade_data = {}

        self.portfolio.new_trade(trade_data)
