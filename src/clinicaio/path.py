#!/usr/bin/env python3
"""Path functions and classes."""

import dataclasses
import logging
import pathlib
from collections import OrderedDict
from pathlib import Path
from typing import Union, Optional, List

from .entities import Entity, EntityArg, EntityValue


LOGGER = logging.getLogger(__name__)


# Key-value delimiter in filepaths.
KEY_DELIMITER = "-"

# Entity delimiter in filepaths.
COMPONENT_DELIMITER = "_"


def get_path(path: "PathArg"):
    """
    Get the underlying Path object from a PathArg.
    """
    if isinstance(path, BIDSPath):
        return path.path
    return Path(path)


# TODO: find the specification and apply it here
def check_name(name):
    """
    Check entity and suffix names for invalid characters. This is used for keys
    and suffixes.

    Raises:
        ValueError:
            The name is invalid.
    """
    if not isinstance(name, str):
        raise ValueError(f"Names must be strings, not {type(name)}.")
    if not name:
        raise ValueError("Empty strings are not permitted.")


@dataclasses.dataclass
class BIDSPath:
    """
    BIDS path with parsed metadata.
    """

    extensions: List[str]
    entities: OrderedDict[str, Union[str, int]] = dataclasses.field(
        default_factory=OrderedDict
    )
    suffix: Optional[str] = None
    parent: Optional[Union["BIDSDirectory", pathlib.Path]] = None

    def __post_init__(self):
        """
        Validate that the data is BIDS-compliant.
        """
        if any(not ext.startswith(".") for ext in self.extensions):
            raise ValueError('All extensions should start with ".".')

        if not (self.entities or self.suffix):
            raise ValueError("BIDS paths must contain at least one entity or a suffix.")

        if not isinstance(self.entities, OrderedDict):
            self.entities = OrderedDict(self.entities)

        for key, value in self.entities.items():
            check_name(key)
            if isinstance(value, str):
                check_name(value)
            # TODO: check if non-negativity is a criterion
            elif isinstance(value, int):
                if value < 0:
                    raise ValueError("Entity indices must be non-negative.")
            else:
                raise ValueError(
                    "Entity values must be either a valid string or a non-negative integer."
                )

        if self.suffix is not None:
            check_name(self.suffix)

    def asdict(self):
        """
        Get the dict of attributes for this dataclass.

        Returns:
            The shallow copy of dict of attributes that can be used to
            instantiate a new instance via unpacking.
        """
        names = (field.name for field in dataclasses.fields(self))
        return {name: getattr(self, name) for name in names}

    @property
    def prime_entity(self):
        """
        The first entity in this path, or None if this path has no entities.
        """
        for ent in self.entities:
            return ent
        return None

    @property
    def path(self):
        """
        The pathlib.Path object for this BIDSPath.
        """
        components = []
        if self.entities:
            components.append(
                COMPONENT_DELIMITER.join(
                    KEY_DELIMITER.join((k, str(v))) for (k, v) in self.entities.items()
                )
            )
        if self.suffix:
            components.append(self.suffix)

        stem = COMPONENT_DELIMITER.join(components)
        exts = "".join(self.extensions)
        name = f"{stem}{exts}"
        if self.parent:
            return get_path(self.parent) / name
        return pathlib.Path(name)

    def check(self):
        """
        Check for errors in this path. Override this in subclasses to add
        specific logic for that subclass, such as checking entity values in
        names or that required files exist in a directory. The method should
        raise BIDSPathError or a subclass thereof if the check fails.
        """

    def __str__(self):
        return str(self.path)

    def __repr__(self):
        return f"{self.__class__.__qualname__}({self.path})"

    @classmethod
    def from_path(
        cls,
        path: "PathArg",
        parent: Optional["BIDSDirectory"] = None,
        is_root: bool = False,
    ):
        """
        Create an instance of this class from a path and parent.

        Args:
            path:
                The path.

            parent:
                An optional BIDSDirectory subclass to return when the parent
                directory is requested.

            is_root:
                If True, treat path as the root directory of a dataset and skip
                entity checking. The filename's stem will be set to the suffix.

        Returns:
            An instance of this class.
        """
        path = get_path(path)
        if parent is None:
            parent = path.resolve().parent
        extensions = path.suffixes
        if is_root:
            return cls(
                extensions=extensions, entities={}, suffix=path.stem, parent=parent
            )

        entities, suffix = cls.get_entities_and_suffix(path)
        return cls(
            extensions=extensions, entities=entities, suffix=suffix, parent=parent
        )

    @classmethod
    def from_bids_path(cls, bids_path: "BIDSPath"):
        """
        Create an instance of this class from another BIDSPath instance or
        subclass thereof.

        Args:
            bids_path:
                The BIDSPath instance.

        Returns:
            An instance of this class. If the input argument is already a direct
            instance of this class then it will be returned unchanged. Otherwise
            a new instance of this class will be created with shallow copies of
            the attributes in the input path.
        """
        # Do not use isinstance here despite the linter's recommendation. We do
        # not want to match subclasses.
        if type(bids_path) is cls:  # pylint: disable=unidiomatic-typecheck
            return bids_path
        return cls(**bids_path.asdict())

    @classmethod
    def get_entities_and_suffix(cls, path: pathlib.Path):
        """
        Parse the entities and suffix from a path.

        Args:
            path:
                The pathlib.Path object to parse.

        Returns:
            The OrderedDict of entities and the suffix.
        """
        stem = path.stem
        # Python dictionaries are not guaranteed to be ordered but this makes
        # the intention explicit and guarantees retrocompatibility.
        entities = OrderedDict()
        for ent in stem.split(COMPONENT_DELIMITER):
            # Try to split the entity. If it doesn't split into a key-value pair
            # then it's the suffix, which mush appear as the final component.
            try:
                key, value = ent.split(KEY_DELIMITER, 1)
            except ValueError:
                return entities, ent
            # Transform known keys into instances of BIDSKey.
            key = Entity.convert(key)
            entities[key] = value
        # No suffix found.
        return entities, None

    def get_entity_value(self, entity: EntityArg):
        """
        Get the value of an entity if it exits.

        Args:
            entity:
                The entity name.

        Returns:
            The entity value as a string if present, else None.
        """
        entity = Entity.convert(entity)
        return self.entities.get(entity)

    def has_entity(self, entity: EntityArg):
        """
        Check if this path contains the given entity.

        Args:
            entity:
                The entity to check.

        Returns:
            True if this path contains the entity, else False.
        """
        entity = Entity.convert(entity)
        return entity in self.entities

    def matches_entity_value(self, entity: EntityArg, value: EntityValue):
        """
        Check if this path matches the given entity value. If the value to match
        is an integer, the internal value will be converted to an integer before
        matching.

        Args:
            entity:
                The entity to match.

            value:
                The value to match.

        Returns:
            True if the values match, else False. Missing entities will also
            return False.
        """
        entity = Entity.convert(entity)
        try:
            my_value = self.entities[entity]
        except KeyError:
            return False

        if isinstance(value, int):
            try:
                return int(my_value) == value
            except ValueError:
                LOGGER.warning(
                    "Value of entity %s is not an integer in %s", entity, self
                )
                return False

        return my_value == value

    def is_dir(self):
        """
        True if this path is a directory, else False.
        """
        return self.path.is_dir()

    def resolve(self):
        """
        Resolve the path (equivalent to pathlib.Path.resolve()).
        """
        if self.parent:
            self.parent.resolve()
            return
        self.parent = self.path.resolve().parent

    def maybe_convert_child(self, bids_path: "BIDSPath"):
        """
        Optionally convert a child BIDSPath instance to a different BIDSPath
        type. This function is invoked by the __div__ operator and can be
        overridden in subclasses to customize child paths by e.g. entity.

        When cnoverting types, it is recommended to invoke the from_bids_path()
        method of the target class with the given bids_path argument.

        Args:
            bids_path:
                The child BIDSPath instance.

        Returns:
            A child BIDSPath instance.
        """
        return bids_path

    def __div__(self, value: "PathArg"):
        """
        Emulate Path's division operator.

        Args:
            value:
                The value to join to the path.

        Returns:
            The joined path as a BIDSPath or subclass thereof.
        """
        my_type = type(self)
        value = get_path(value)
        child_path = self.path / value
        # This handles BIDSDirectory instances without needing to know the type
        # here.
        if child_path.is_dir():
            return self.maybe_convert_child(my_type.from_path(child_path, parent=self))
        return self.maybe_convert_child(BIDSPath.from_path(child_path, parent=self))

    @property
    def depth(self):
        """
        The depth of this path within a dataset's file hierarchy, or None if it
        is not part of one.
        """
        parent = self.parent
        if parent is None:
            return None
        if isinstance(parent, pathlib.Path):
            return 0
        depth = parent.depth
        if depth is None:
            return None
        return depth + 1


PathArg = Union[str | Path | BIDSPath]
