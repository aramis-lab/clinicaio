__all__ = ["greet"]


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
