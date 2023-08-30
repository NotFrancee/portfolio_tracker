from rich.console import Console
from rich.markdown import Markdown
from app.prompts.validators import Validator


class PromptChoice:
    """Prompt to choose between different items"""

    def __init__(
        self,
        console: Console,
        title: str,
        prompt_md: str,
        options: list[str],
    ) -> None:
        self.console = console
        self.title = title
        self.prompt = Markdown(prompt_md + "(specify index)")
        self.options = options

    def print_options(self):
        """Displays all the available options to the user"""

        self.console.print(f"[bold red]{self.title}[/bold red]")
        for i, option in enumerate(self.options):
            self.console.print(f"[bold]{i})[/bold] {option}")

    def run(self):
        self.print_options()

        while True:
            inp = self.console.input(self.prompt)

            if not inp.isnumeric():
                print("The specified input is not a number, please try again")
                continue
            elif not (0 <= int(inp) <= len(self.options) - 1):
                print("index out of range, try again")
                continue

            index = int(inp)

            choice = self.options[index]
            return choice


class PromptInput:
    """Prompt Class"""

    def __init__(
        self,
        console: Console,
        prompt_md: str,
        validator: Validator,
    ) -> None:
        self.console = console
        self.prompt = Markdown(prompt_md)
        self.validator = validator()

    def run(self):
        while True:
            inp = self.console.input(self.prompt)

            is_valid = self.validator.validate(inp)

            if is_valid:
                return self.validator.process(inp)
