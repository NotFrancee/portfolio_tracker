# Main menu
from rich.console import Console
from rich.markdown import Markdown
from rich.style import Style
import os
from pynput import keyboard
import time
from classes.portfolio import Portfolio

class OutOfIndexError(Exception):
    pass

class OptionNotFoundError(Exception): 
    pass

class Menu:
    title_style = Style(bold=True, color="red")

    def __init__(
        self, console: Console, title: str, options: dict[str, callable]
    ) -> None:
        self.console = console
        self.title = title
        self.options = options | {'Quit': self.quit}

        self.should_quit = False

    def clear_screen(self): 
        os.system('cls')
        self.console.print(self.title, style=self.title_style)
        self.console.print(Markdown("# Portfolio Tracker tool"))

    def quit(self): 
        print('Thanks! Quitting the program')
        self.should_quit = True

    def should_continue(self): 
        response = self.console.input('Want to do something else? (y/N)')

        if response.strip().lower() == 'y': 
            return True
        
        return False

    def print_options(self):
        for i, option in enumerate(self.options):
            self.console.print(f"[bold]{i})[/bold] {option}")

    def convert_to_int(self, choice: str):
        key = None
        options_as_arr = list(self.options)
        options_as_arr_lower = [option.lower() for option in options_as_arr]

        if choice.isnumeric(): 
            choice_index = int(choice)

            if choice_index >= len(self.options): 
                raise OutOfIndexError()

            key = options_as_arr[choice_index]

        else: 
            if choice.lower() not in options_as_arr_lower:
                raise OptionNotFoundError()
            
            key = options_as_arr[options_as_arr_lower.index(choice.lower())]

        corresponding_func = self.options[key]
        return corresponding_func

    def run(self):
        while True:
            self.clear_screen()
            self.print_options()

            try:
                input_prompt = Markdown("*What do you want to do?*")
                choice = self.console.input(input_prompt)

                func = self.convert_to_int(choice)
                func()
                print('executed fucntion')
            except OutOfIndexError:
                print('Index is out of range for the available options. Please try again with a smaller number')
                time.sleep(3)
                continue
            except OptionNotFoundError:
                print('The option specified is not present. Please choose among the available choices')
                time.sleep(3)
                continue
            
            # check if the program should end no matter what; if not, prompt the user on whether he wants to continue
            if not self.should_quit and self.should_continue(): 
                continue
            else: 
                break


class App():
    
    def __init__(self) -> None:
        self.main_menu_options = {"See Data": self.see_data, "Edit Data": self.edit_data}

        self.portfolio = Portfolio()
        self.console = Console()
        self.main_menu = Menu(self.console, "Main Menu", self.main_menu_options)

    def see_data(self): 
        self.portfolio.display_summary()

    def edit_data(self): 
        print('WIP')

    def run(self): 
        self.main_menu.run()


app = App()
app.run()