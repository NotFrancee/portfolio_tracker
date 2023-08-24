from consolemenu.prompt_utils import PromptUtils
from consolemenu.validators.base import BaseValidator
from consolemenu import Screen
from classes.portfolio import Portfolio
import pandas as pd

import time


class TickerValidator(BaseValidator):
    def validate(self, input_string: str) -> bool:
        return len(input_string) < 5


class DateValidator(BaseValidator):
    def validate(self, input_string: str) -> bool:
        print(input_string)

        return True


class CostValidator(BaseValidator):
    def validate(self, input_string: str) -> bool:
        return float(input_string) > 0


def prompt_date(promptutil: PromptUtils):
    validator = DateValidator()
    try:
        date_input = promptutil.input(
            "Date: ", default=pd.Timestamp.today(), validators=validator
        )

        return pd.to_datetime(date_input.input_string)
    except Exception as err:
        print(err)


def prompt_ticker(promptutil: PromptUtils):
    validator = TickerValidator()
    ticker_input = promptutil.input("Ticker: ", validators=validator)
    ticker = ticker_input.input_string.upper().strip()

    return ticker


def prompt_number(promptutil: PromptUtils, prompt: str):
    validator = CostValidator()

    prompt_input = promptutil.input(prompt, validators=validator)

    return float(prompt_input.input_string)


def prompt_multiple_choice(
    promptutil: PromptUtils, choices: list[str], title: str, prompt: str
):
    index = promptutil.prompt_for_numbered_choice(choices, title, prompt)

    return choices[index]


def new_trade_action(portfolio: Portfolio):
    try:
        exchanges = ["NYSE", "MIL", "NDQ"]
        brokers = ["IBKR", "Degiro"]
        currencies = ["USD", "EUR"]
        actions = ["buy", "sell"]

        screen = Screen()
        promptutil = PromptUtils(screen)

        date = prompt_date(promptutil)
        ticker = prompt_ticker(promptutil)
        exchange = prompt_multiple_choice(
            promptutil, exchanges, "Exchange", "choose exchange"
        )
        broker = prompt_multiple_choice(
            promptutil, brokers, "Broker", "choose exchange"
        )
        currency = prompt_multiple_choice(
            promptutil, currencies, "Currency", "choose exchange"
        )
        action = prompt_multiple_choice(
            promptutil, actions, "Action", "choose exchange"
        )

        amount = prompt_number(promptutil, "Amount: ")
        price = prompt_number(promptutil, "Price: ")
        transaction_costs = prompt_number(promptutil, "Transaction costs: ")

        notes = ""

        trade_data = {
            "date": str(date.date()),
            "ticker": ticker,
            "exchange": exchange,
            "broker": broker,
            "currency": currency,
            "action": action,
            "amount": amount,
            "price": price,
            "transaction_costs": transaction_costs,
            "notes": notes,
        }

        portfolio.new_trade(trade_data)

        print("done, created trade")
        print("now restart app")
        promptutil.enter_to_continue()

    except Exception as err:
        print(err)
        time.sleep(15)
