#!/usr/bin/env python3
"""
Load and parse the BIDS schema.
"""

import functools
import importlib
import importlib.resources
import json


THIS_PKG = __name__.rsplit(".", 1)[0]


class SchemaParser:
    """
    Parse schema data and generate corresponding code in this package.
    """

    @functools.cached_property
    def schema(self):
        """
        The schema data as a single object from this packages internal
        resources.
        """
        resources_module = f'{THIS_PKG}.resources'
        schema_path = importlib.resources.files(resources_module) / "schema.json"
        with (
            importlib.resources.as_file(schema_path) as schema_path,
            schema_path.open("rb") as handle,
        ):
            return json.load(handle)

    @staticmethod
    def _get_submodule(submodule):
        """
        Load a submodule from this package.

        Args:
            submodule:
                The relative path to the submodule to load.

        Returns:
            The loaded submodule object.
        """
        return importlib.import_module(submodule, package=THIS_PKG)

    # TODO
    # Move the dynamic version variables elsewhere.
    def set_versions(self):
        """
        Set the BIDS and schema version variables in the version submodule.
        """
        mod = self._get_submodule(".version")
        schema = self.schema
        for name in ("BIDS version", "Schema version"):
            field_name = name.replace(" ", "_").lower()
            var_name = field_name.upper()
            value = schema[field_name]
            setattr(mod, var_name, value)
            #  getattr(mod, var_name).__doc__ = f"{name} as a string."
            setattr(mod, f"{var_name}_TUPLE", value.split("."))
            #  getattr(mod, f"{var_name}_TUPLE").__doc__ = f"{name} as a tuple."

    def insert_code(self):
        """
        Insert code to implement the schema.
        """
        self.set_versions()
