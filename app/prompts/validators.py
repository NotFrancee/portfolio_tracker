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
