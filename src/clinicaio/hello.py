__all__ = [
    "greet",
    "say_goodbye",
]


def greet(name: str):
    """Greet the person with provided name.

    Parameters
    ----------
    name : str
        The name of the person to greet.
    """
    print(_build_greeting_message(name))


def _build_greeting_message(name: str) -> str:
    return f"Hello {name} !"


def say_goodbye(name: str):
    """Say goodbye to the person with the provided name.

    Parameters
    ----------
    name : str
        The name of the person to say goodbye to.
    """
    print(_build_good_bye_message(name))


def _build_good_bye_message(name: str) -> str:
    return f"Goodbye {name} !"
