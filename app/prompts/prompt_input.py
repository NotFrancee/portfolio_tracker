from rich.console import Console
from rich.markdown import Markdown
from app.prompts.validators import Validator


class PromptInput:
    """Prompt Class"""

    def __init__(
        self,
        console: Console,
        prompt_md: str,
        validator: Validator = None,
    ) -> None:
        self.console = console
        self.prompt = Markdown(prompt_md)
        self.validator = validator

    def run(self):
        while True:
            inp = self.console.input(self.prompt)

            if self.validator:
                is_valid = self.validator.validate(inp)

                if is_valid:
                    return self.validator.process(inp)
            else:
                return inp
