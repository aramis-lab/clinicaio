


class Label(UserString):
    def __init__(self, value: str):
        super().__init__(self.validate(value))

    @classmethod
    def validate(cls, value: str) -> str:
        if value.isalnum():
            return value
        raise ValueError(
            f"Label '{value}' is not a valid BIDS label: it must be composed only by letters and/or numbers."
        )
    
class Index:
    value: PositiveInt
    length_as_string: PositiveInt # for padding with zeros

    # Implement the constraint and the string representation taking into account the padding...
class Entity:
    key: Label
    value : Label | Index

    def __str__(self) -> str:
        return f"{self.key}-{self.value}"

class SubjectEntity(Entity):
    key = Label("sub")

    def __init__(self, value: str):
        self.value = Label(value)

...