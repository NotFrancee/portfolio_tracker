from rich.console import Console
from rich.markdown import Markdown
from app.prompts.validators import Validator


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
        self.validator = validator

    def run(self):
        inp = self.console.input(self.prompt)

        is_valid = self.validator.validate(inp)

        if is_valid:
            processed_input = self.validator.process(inp)
            return processed_input
        else:
            print("an error occurred")
