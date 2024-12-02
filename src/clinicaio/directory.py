#!/usr/bin/env python3
"""Path functions and classes."""

import functools
import logging
from typing import Optional, Callable, Union

from .entities import Entity, EntityArg, EntityValue
from .exception import BIDSPathError
from .path import BIDSPath

LOGGER = logging.getLogger(__name__)


class _BIDSDirectoryMetaclass(type):
    """
    Metaclass for BIDSDirectory that automatically defines methods in subclasses
    based on configured subdirectory types for different entities.
    """

    def __new__(mcs, *args):
        new_cls = super().__new__(mcs, *args)
        new_cls.add_custom_subclass_methods()
        return new_cls


class BIDSDirectory(BIDSPath, metaclass=_BIDSDirectoryMetaclass):
    """
    A directory in a BIDS dataset.

    Attributes:
        SUBDIRECTORY_TYPES_BY_ENTITY:
            An optional dict mapping entity types to subclasses of BIDSPath or
            BIDSDirectory. This can be used conveniently convert child nodes of
            a directory to custom subclasses by entity. For example, the
            BIDSDataset class can automatically convert its child subjects to
            instances of the class BIDSSubject.

        SUBCLASSES_BY_SUFFIX:
            Similar to SUBCLASSES_BY_ENTITY, this is an optional dict mapping
            suffixes to subclasses of BIDSPath or BIDSDirectory. Currently
            SUBCLASSES_BY_ENTITY will take precedence but this behavior may be
            configured by overriding the maybe_convert_child method.
    """

    SUBCLASSES_BY_ENTITY = {}
    SUBCLASSES_BY_SUFFIX = {}

    def maybe_convert_child(self, bids_path: BIDSPath):
        for key, dct in (
            (bids_path.prime_entity, self.SUBCLASSES_BY_ENTITY),
            (bids_path.suffix, self.SUBCLASSES_BY_SUFFIX),
        ):
            if key is None:
                continue
            try:
                subcls = dct[key]
            except KeyError:
                continue
            else:
                LOGGER.debug("Converting %s to instance of %s.", bids_path, subcls)
                return subcls.from_bids_path(bids_path)
        return bids_path

    def get_child_paths(self, include_files: bool = True, include_dirs: bool = True):
        """
        Get an iterator over file paths in this directory.

        Args:
            include_files:
                Include file (i.e. non-directory) paths.

            include_dirs:
                Include directory paths.

        Returns:
            The iterator over Path instances of the selected paths.
        """
        paths = sorted(self.path.iterdir())
        if include_files and include_dirs:
            yield from paths
            return
        for path in paths:
            is_dir = path.is_dir()
            if is_dir:
                if include_dirs:
                    yield path
            elif include_files:
                yield path

    def get_child_bids_paths(self, **kwargs):
        """
        An iterable of BIDSPath instances of paths in this directory.

        Args:
            **kwargs:
                Keyword arguments passed through to get_paths.

        Returns:
            An iterator over BIDSPath instances.
        """
        path = self.path
        for child_path in self.get_child_paths(**kwargs):
            subpath = child_path.relative_to(path)
            yield self.__div__(subpath)

    @property
    def child_entities(self):
        """
        The set of entities found in this directory's child node filepaths.
        """
        entities = set()
        for path in self.get_child_bids_paths():
            entities.update(path.entities)
        return entities

    def get_children_by_entity(
        self,
        entity: EntityArg,
        value: EntityValue = None,
        include: bool = True,
        **kwargs,
    ):
        """
        Get an iterator over BIDS paths in this directory that match the target
        entity.

        Args:
            entity:
                The target entity.

            value:
                An optional entity value to match. If none, all paths with
                the given entity are matched.

            include:
                If True, return paths that match, else return paths that don't
                match.

            **kwargs:
                Keyword arguments passed through to get_bids_paths.

        Returns:
            A generator over instances of BIDSPath for each matching path.

        TODO:
            Maybe generalize this function to support multiple entities.
        """
        entity = Entity.convert(entity)
        for bids_path in self.get_child_bids_paths(**kwargs):
            match = False
            if value is None:
                match = bids_path.has_entity(entity)
            else:
                match = bids_path.matches_entity_value(entity, value)
            if match == include:
                yield bids_path

    def get_child_mapping_by_entity(self, entity: EntityArg, *args, **kwargs):
        """
        Get a dict mapping entity values to children of this directory
        containing that entity as instances of BIDSPath or a subclass thereof.

        Args:
            entity:
                The target entity.

            *args:
                Additional ositional arguments passed through to
                get_children_by_entity.

            **kwargs:
                Keyword arguments passed through to get_children_by_entity.

        Returns:
            A dict mapping entity values to instances of the class passed
            through to get_children_by_entity.
        """
        mapping = {}
        for child in self.get_children_by_entity(entity, *args, **kwargs):
            value = child.get_entity_value(entity)
            # Warn about multiple children sharing the same value.
            mapped_child = mapping.setdefault(value, child)
            if mapped_child != child:
                LOGGER.warning(
                    "Excluding %s from %s mapping because the value %s already maps to %s",
                    child,
                    entity,
                    value,
                    mapped_child,
                )
        return mapping

    def recurse_directory(
        self,
        filter_func: Optional[
            Callable[[Union[BIDSPath, "BIDSDirectory"]], bool]
        ] = None,
    ):
        """
        Recurse paths within this directory.

        Args:
            filter_func:
                A optional function that accepts a BIDSPath argument and returns
                a boolean to indicate if the path should be included in the
                results (True) or not (False).

        Returns:
            A generator over all directories and files in this directory, as
            instances of BIDSDirectory and BIDSPath, respectively, or subclasses
            thereof.
        """
        for subdir in self.get_child_bids_paths(include_files=False):
            if filter_func is None or filter_func(subdir):
                yield subdir
            yield from subdir.recurse_directory(filter_func=filter_func)
        for path in self.get_child_bids_paths(include_dirs=False):
            if filter_func is None or filter_func(path):
                yield path

    def check(self):
        super().check()
        # Ensure that this is a dictionary.
        path = self.path
        if path.exists() and not path.is_dir():
            raise BIDSPathError(f"{path} is not a directory.")
        for path in self.recurse_directory():
            path.check()

    @classmethod
    def add_custom_subclass_methods(cls):
        """
        Add custom caching accessors for the entity subdirectories specified in
        SUBDIRECTORY_TYPES_BY_ENTITY.
        """
        for entity, subdir_cls in cls.SUBCLASSES_BY_ENTITY.items():
            cls_name = subdir_cls.__name__
            display_name = entity.display_name
            plural = entity.display_name_plural

            # Define a property with a dict mapping entity values to instances
            # of a seclected subclass for that entity
            @property
            def entities_property(self, entity=entity):
                return self.get_child_mapping_by_entity(entity)

            entities_property.__doc__ = (
                f"This directory's {plural} as instances of {cls_name}."
            )
            entities_property_name = plural
            setattr(cls, entities_property_name, entities_property)
            getattr(cls, entities_property_name).__set_name__(
                cls, entities_property_name
            )

            # Define the accessor method to retrieve specific entities by value.
            def get_entity(self, label: EntityValue, _attr=plural):
                return getattr(self, _attr).get(label)

            get_entity = functools.partial(get_entity, _attr=plural)
            get_entity.__name__ = f"get_{display_name}"
            get_entity.__doc__ = f"""
            Get one {display_name} by entity value. This assumes that there is
            only one path per value of the entity.

            Args:
                value:
                    The target value.

            Returns:
                An instance of {cls_name} if the target entity exists, else None
            """
            setattr(cls, get_entity.__name__, get_entity)
