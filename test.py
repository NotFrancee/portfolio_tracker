from app.new_trade import NewTradePrompter
from classes.portfolio import Portfolio
from rich.console import Console

portfolio = Portfolio(pull_live_data=False)
console = Console()

tradeprompter = NewTradePrompter(portfolio, console)

tradeprompter.run()
