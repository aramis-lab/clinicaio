#!/usr/bin/env python3
"""Entity classes and functions."""


import enum
from typing import Union


class Entity(enum.StrEnum):
    """
    Recognized entities.
    """

    ANATOMY = "anat"
    SESSION = "ses"
    SUBJECT = "sub"

    @classmethod
    def convert(cls, arg: "EntityArg"):
        """
        Convert recognized entities to members of this class.

        Args:
            arg:
                The argument to convert.

        Returns:
            An instance of this class if the argument could be converted, else
            the original argument.
        """
        if isinstance(arg, cls):
            return arg
        try:
            return cls[arg]
        except KeyError:
            return arg

    @property
    def display_name(self):
        """
        Get the name of this entity for functions and user documentation.
        """
        return self.name.lower()

    @property
    def display_name_plural(self):
        """
        Get the plural of the display name.
        """
        # TODO
        # Add cases for exceptions when necessary.
        return f"{self.display_name}s"


EntityArg = Union[str, Entity]
EntityValue = Union[str, int]
