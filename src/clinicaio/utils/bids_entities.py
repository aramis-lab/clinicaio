from typing import Any
from .caps import Space, Description, Resolution
from .pet import Tracer, SUVRReferenceRegion


class Entity:
    """Base class for BIDS entities."""

    key: str

    def __new__(cls, value: Any) -> str:
        """Returns key-value pair."""
        return cls.key + "-" + cls._process_value(value)

    @classmethod
    def _process_value(cls, value: Any) -> str:
        """Processes the value."""
        return str(value)


class SubjectEntity(Entity):
    """Class to model the Subject entity ('sub-...')."""

    key = "sub"

    @classmethod
    def _process_value(cls, value: int) -> str:
        if not isinstance(value, int):
            try:
                value = int(value)
            except TypeError as exc:
                raise ValueError(f"Subject ID should be an int. Got {value}") from exc
        if value < 1 or value > 999:
            raise ValueError(f"Subject ID should be between 1 and 999. Got {value}")

        return str(value).zfill(3)


class SessionEntity(Entity):
    """Class to model the Session entity ('ses-...')."""

    key = "ses"

    @classmethod
    def _process_value(cls, value: int) -> str:
        if not isinstance(value, int):
            try:
                value = int(value)
            except TypeError as exc:
                raise ValueError(f"Session ID should be an int. Got {value}") from exc
        if value < 0 or value > 999:
            raise ValueError(f"Session ID should be between 0 and 999. Got {value}")

        return "M" + str(value).zfill(3)


class SpaceEntity(Entity):
    """Class to model the Space entity ('space-...')."""

    key = "space"

    @classmethod
    def _process_value(cls, value: str) -> str:
        return Space(value).value


class DescriptionEntity(Entity):
    """Class to model the Description entity ('desc-...')."""

    key = "desc"

    @classmethod
    def _process_value(cls, value: str) -> str:
        return Description(value).value


class ResolutionEntity(Entity):
    """Class to model the Resolution entity ('res-...')."""

    key = "res"

    @classmethod
    def _process_value(cls, value: str) -> str:
        return Resolution(value).value


class TracerEntity(Entity):
    """Class to model the Tracer entity ('trc-...')."""

    key = "trc"

    @classmethod
    def _process_value(cls, value: str) -> str:
        return Tracer(value).value


class SUVREntity(Entity):
    """Class to model the SUVR Reference Region entity ('suvr-...')."""

    key = "suvr"

    @classmethod
    def _process_value(cls, value: str) -> str:
        return SUVRReferenceRegion(value).value
