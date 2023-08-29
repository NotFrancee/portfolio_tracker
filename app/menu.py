# Main menu
from rich.console import Console
from rich.markdown import Markdown
from rich.style import Style
import os
from pynput import keyboard
import time


class OutOfIndexError(Exception):
    """Exception to use when the index specified for the menu is out of range"""

    pass


class OptionNotFoundError(Exception):
    """Exception to use when the option specified is not in the options list"""

    pass


class Menu:
    """Class component for Menus"""

    title_style = Style(bold=True, color="red")

    def __init__(
        self, console: Console, title: str, options: dict[str, callable]
    ) -> None:
        """Inits the class. The function needs
        * The console object from the rich package,
        * The title of the menu,
        * The dictionary with option names and the function to call
        """

        self.console = console
        self.title = title
        self.options = options | {"Quit": self.quit}

        self.should_quit = False

    def clear_screen(self):
        """Clears the screen, reprinting the main title of the program and the title of the menu"""

        os.system("cls")
        self.console.print(Markdown("# Portfolio Tracker tool"))
        self.console.print(self.title, style=self.title_style)

    def quit(self):
        """Quits the program"""

        print("Thanks! Quitting the program")
        self.should_quit = True

    def should_continue(self):
        """Prompts the user on whether he wants to do another action on the menu"""

        response = self.console.input("Want to do something else? (y/N)")

        if response.strip().lower() == "y":
            return True

        return False

    # TODO
    def press_enter_to_continue(self):
        enter_pressed = False

        def trigger_enter_pressed():
            enter_pressed = True

        self.console.print(Markdown("_Press Enter to continue_"))

        while not enter_pressed:
            print("current state of the variable", enter_pressed)

            def on_press(key: keyboard.Key):
                print(key)
                if key == keyboard.Key.enter:
                    print("enter key presse 2 ")
                    trigger_enter_pressed()
                    kb_listener.stop()

            with keyboard.Listener(on_press=on_press) as kb_listener:
                kb_listener.join()

            # kb_listener = keyboard.Listener(on_press=on_press)
            # kb_listener.start()
            # kb_listener.join()

            print("fasdfasfasfasfsfdaaf")

    def print_options(self):
        """Displays all the available options to the user"""

        for i, option in enumerate(self.options):
            self.console.print(f"[bold]{i})[/bold] {option}")

    def get_function(self, choice: str):
        """Converts the choice to the function to call. This function recognizes whether the user specified the index of the option
        or the name of the option itself
        """

        key = None
        # creates two lists so that the user can ignore case when specifying the option
        options_as_arr = list(self.options)
        options_as_arr_lower = [option.lower() for option in options_as_arr]

        # if the choice is numeric, this means the user specified the index of the option
        if choice.isnumeric():
            choice_index = int(choice)

            # if the index speicified is too large, raise an Exception
            if choice_index >= len(self.options):
                raise OutOfIndexError()

            key = options_as_arr[choice_index]

        # else, it means the user specified the name of the option
        else:
            # if the option is not present in the list of keys, raise an Exception
            if choice.lower() not in options_as_arr_lower:
                raise OptionNotFoundError()

            # the key must be case-sensitive to retrieve the function, so get the index from the list of lowercase options
            key = options_as_arr[options_as_arr_lower.index(choice.lower())]

        # select and return the corresponding function
        corresponding_func = self.options[key]
        return corresponding_func

    def run(self):
        """Shows and runs the menu"""

        while True:
            # clears the screen and shows the options to the user
            self.clear_screen()
            self.print_options()

            # prompts the user for the option and calls the function
            try:
                input_prompt = Markdown("_What do you want to do?_")
                choice = self.console.input(input_prompt)

                func = self.get_function(choice)
                func()

            except OutOfIndexError:
                print(
                    "Index is out of range for the available options. Please try again with a smaller number"
                )
                time.sleep(3)
                continue
            except OptionNotFoundError:
                print(
                    "The option specified is not present. Please choose among the available choices"
                )
                time.sleep(3)
                continue

            # check if the user chose to quit; if not, prompt the user on whether he wants to continue
            if not self.should_quit and self.should_continue():
                continue

            break
