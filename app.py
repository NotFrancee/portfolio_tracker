from classes.portfolio import Portfolio
from app.menu import Menu
from rich.console import Console


class App:
    """Class for the main App"""

    def __init__(self) -> None:
        """Here, specify the various menu options and initialize the variables"""

        self.main_menu_options = {
            "See Data": self.see_data,
            "Edit Data": self.edit_data,
        }

        self.portfolio = Portfolio()
        self.console = Console()
        self.main_menu = Menu(self.console, "Main Menu", self.main_menu_options)

    def see_data(self):
        """Function to visualize data about the portfolio"""

        self.portfolio.display_summary()

    def edit_data(self):
        """Function to edit the portfolio by adding trades"""
        print("WIP")

    def save_data(self):
        pass

    def run(self):
        """Runs the app"""

        self.main_menu.run()


app = App()
app.run()
