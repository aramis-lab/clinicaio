#!/usr/bin/env python3
"""BIDS parser."""

import functools
import json
import logging


from ..directory import BIDSDirectory
from ..entities import Entity
from ..exception import BIDSPathError
from .subject import BIDSSubject


LOGGER = logging.getLogger(__name__)


class BIDSDatasetError(BIDSPathError):
    """Exceptions raised by the parser."""


class BIDSDataset(BIDSDirectory):
    """
    BIDS dataset parser.
    """

    SUBCLASSES_BY_ENTITY = {Entity.SUBJECT: BIDSSubject}

    @functools.cached_property
    def dataset_description(self):
        """
        Data from the dataset_description.json file.
        """
        path = self.path / "dataset_description.json"
        LOGGER.debug("Loading %s", path)
        try:
            with path.open("rb") as handle:
                return json.load(handle)
        except (OSError, json.JSONDecodeError) as err:
            raise BIDSDatasetError(err) from err

    @property
    def name(self) -> str:
        """
        The name of the dataset. REQUIRED.
        """
        return self.dataset_description["Name"]

    @property
    def bids_version(self) -> str:
        """
        The version of the BIDS standard that was used. REQUIRED.
        """
        return self.dataset_description["BIDSVersion"]
