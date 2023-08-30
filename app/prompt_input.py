from rich.console import Console
from rich.markdown import Markdown

import six
from abc import ABCMeta, abstractmethod


@six.add_metaclass(ABCMeta)
class Validator:
    """Base class for the validator. Override validate and process methods, which will later be used by the Prompt Class"""

    def __init__(self) -> None:
        pass

    @abstractmethod
    def validate(self, input: str):
        """You must override this function. Return false is not valid, True if valid"""
        pass

    @abstractmethod
    def process(self, input_str: str):
        pass


class DateValidator(Validator):
    def validate(self, input: str):
        print("wip")
        return super().validate(input)

    def process(self, input_str: str):
        print("wip")
        return super().process(input_str)


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
