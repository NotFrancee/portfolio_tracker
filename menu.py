# Main menu
from rich.console import Console
from rich.markdown import Markdown
from rich.style import Style
import os


class Menu:
    title_style = Style(bold=True, color="red")

    def __init__(
        self, console: Console, title: str, options: list[str]
    ) -> None:
        self.console = console
        self.title = title
        self.options = options

    def add_option(self, option):
        self.options.append(option)

    def print_options(self):
        for i, option in enumerate(main_menu_options):
            console.print(f"[bold]{i})[/bold] {option}")

    def convert_to_int(self, choice):
        options_lower = [option.lower() for option in self.options]
        index = None

        if choice is int:
            if int(choice) >= len(options_lower):
                raise Exception("overflow")

            index = choice
        else:
            if choice.lower() not in options_lower:
                raise Exception("not in options")

            index = options_lower.index(choice)

        return int(index)

    def run(self):
        console.print(self.title, style=self.title_style)

        while True:
            self.print_options()

            try:
                input_prompt = Markdown("*What do you want to do?*")
                choice = console.input(input_prompt)

                choice = self.convert_to_int(choice)
            except:
                print("smt wrong")
                continue

            match (choice):
                case 1:
                    print("case 1 triggered")
                    break

                # wrong way to approach

            break


main_menu_options = ["See Data", "Edit Data", "Quit"]

console = Console()

main_menu = Menu(console, "Main Menu", main_menu_options)

os.system("cls")
console.print(Markdown("# Portfolio Tracker tool"))

main_menu.run()
