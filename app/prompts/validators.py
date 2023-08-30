import six
from abc import ABCMeta, abstractmethod
import pandas as pd
import re


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


@six.add_metaclass(ABCMeta)
class Validator:
    """Base class for the validator.
    Override validate and process methods, which will later be used by the Prompt Class
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def validate(self, input_str: str):
        """You must override this function.
        Return false is not valid, True if valid
        """

        return True

    @abstractmethod
    def process(self, input_str: str):
        return input_str


class DateValidator(Validator):
    """Validate dates"""

    def validate(self, input_str: str):
class NumericValidator(Validator):
    """Validate int/float inputs"""

    def __init__(self, numeric_type) -> None:
        super().__init__()

        self.numeric_type = numeric_type

    def validate(self, input_str: str):
        match self.numeric_type:
            case "int":
                if not input_str.isnumeric():
                    return False

            case "float":
                if not isfloat(input_str):
                    return False

            case _:
                print("unsupported numeric type")

        return True

    def process(self, input_str: str):
        return (
            int(input_str) if self.numeric_type == "int" else float(input_str)
        )
