# Import the necessary packages
from consolemenu import Screen, ConsoleMenu
from consolemenu.items import FunctionItem, SubmenuItem
from consolemenu.prompt_utils import PromptUtils
from classes.portfolio import Portfolio
from app.new_trade import new_trade_action


def delete_trade_action():
    print("Process delete trade here")
    PromptUtils(Screen()).enter_to_continue()


def get_portfolio_summary_action(portfolio: Portfolio):
    portfolio.display_summary()
    PromptUtils(Screen()).enter_to_continue()


class App:
    """Class for the main menu of the app"""

    menu = None

    def initialize_menu(self):
        self.menu = ConsoleMenu(
            "Portfolio Tracker ", "Welcome to the portfolio tracker"
        )

    def create_edit_submenu(self):
        # create the menu to edit data
        edit_data = ConsoleMenu(
            "Edit Data", "Edit, add or delete data from the db"
        )

        new_trade = FunctionItem(
            "New Trade", new_trade_action, [self.portfolio]
        )
        delete_trade = FunctionItem("Edit Trade", delete_trade_action)

        edit_data.append_item(new_trade)
        edit_data.append_item(delete_trade)

        edit_data_submenu_item = SubmenuItem("Edit Data", edit_data, self.menu)

        self.menu.append_item(edit_data_submenu_item)

    def create_summary_item(self):
        get_summary = FunctionItem(
            "See Portfolio Summary",
            get_portfolio_summary_action,
            [self.portfolio],
        )

        self.menu.append_item(get_summary)

    def start(self) -> None:
        self.initialize_menu()
        self.create_edit_submenu()
        self.create_summary_item()

        # Finally, we call show to show the menu and allow the user to interact
        self.menu.start()
        self.menu.join()

    def __init__(self) -> None:
        self.portfolio = Portfolio()


app = App()

app.start()
