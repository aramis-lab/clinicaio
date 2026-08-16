from collections import UserString
from enum import Enum
from typing import Optional, Union

__all__ = [
    "Label",
    "Index",
    "Suffix",
]


class Label(UserString):
    """Defines a label as defined in the BIDS specifications (i.e. an alphanumeric string)."""

    def __init__(self, value: Union[str, Enum]):
        super().__init__(self.validate(value))

    @classmethod
    def validate(cls, value: Union[str, Enum]) -> str:
        if isinstance(value, Enum):
            return value.value
        elif isinstance(value, str) and value.isalnum():
            return value
        raise ValueError(
            f"Label '{value}' is not a valid BIDS label: it must be string composed only by letters and/or numbers."
        )


Suffix = Label


class Index(UserString):
    """Defines an index as defined in the BIDS specifications as a positive integer with padding logic."""

    def __init__(self, value: int, length_as_string: Optional[int] = None):
        super().__init__(self.validate(value, length_as_string))

    @classmethod
    def validate(cls, value: int, length_as_string: Optional[int] = None) -> str:
        if not isinstance(value, int) or value < 0:
            raise ValueError(
                f"Index '{value}' is not a valid BIDS index: it must be a non-negative integer."
            )
        if length_as_string is None:
            length_as_string = len(str(value))
        if length_as_string <= 0:
            raise ValueError(
                f"The length of an Index should be at least 1, {length_as_string} was provided."
            )
        if len(str(value)) > length_as_string:
            raise ValueError(
                f"Cannot set index with value {value} with a length of {length_as_string}."
            )
        return str(value).zfill(length_as_string)
