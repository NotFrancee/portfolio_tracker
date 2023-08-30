from classes.portfolio import Portfolio
from rich.console import Console
from app.prompts.prompt_input import PromptInput
from app.prompts.validators import (
    DateValidator,
    TickerValidator,
    NumericValidator,
)
from app.prompts.prompt_choice import PromptChoice

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
            self.console, "Date (yyyy-mm-dd): ", DateValidator()
        ).run()

        ticker = PromptInput(self.console, "Ticker: ", TickerValidator()).run()
        exchange = PromptChoice(
            self.console, "Exchange", "Select Exchange: ", EXCHANGES
        ).run()
        broker = PromptChoice(
            self.console, "Brokers", "Select Broker: ", BROKERS
        ).run()
        currency = PromptChoice(
            self.console, "Currencies", "Select Curreny: ", CURRENCIES
        ).run()
        action = PromptChoice(
            self.console, "Actions", "Action: ", ACTIONS
        ).run()

        amount = PromptInput(
            self.console, "Amount: ", NumericValidator("int")
        ).run()
        price = PromptInput(
            self.console, "@ Price: ", NumericValidator("float")
        ).run()
        transaction_costs = PromptInput(
            self.console, "Transaction costs: ", NumericValidator("float")
        ).run()

        notes = PromptInput(self.console, "Notes: ")

        self.portfolio.new_trade(
            date,
            ticker,
            exchange,
            broker,
            action,
            currency,
            amount,
            price,
            transaction_costs,
            notes,
        )
