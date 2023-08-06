# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Source catalog and object base classes."""
import copy
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.utils import lazyproperty
from gammapy.utils.array import _is_int
from gammapy.utils.table import table_from_row_data, table_row_to_dict

__all__ = ["SourceCatalog", "SourceCatalogObject"]


class SourceCatalogObject:
    """Source catalog object.

    This class can be used directly, but it's mostly used as a
    base class for the other source catalog classes.

    The catalog data on this source is stored in the `source.data`
    attribute as a dict.

    The source catalog object is decoupled from the source catalog,
    it doesn't hold a reference back to it.
    The catalog table row index is stored in `_table_row_index` though,
    because it can be useful for debugging or display.
    """

    _source_name_key = "Source_Name"
    _source_index_key = "catalog_row_index"

    def __init__(self, data, data_extended=None):
        self.data = data
        if data_extended:
            self.data_extended = data_extended

    @property
    def name(self):
        """Source name (str)"""
        name = self.data[self._source_name_key]
        return name.strip()

    @property
    def index(self):
        """Row index of source in catalog (int)"""
        return self.data[self._source_index_key]

    @property
    def _data_python_dict(self):
        """Convert ``data`` to a Python dict with Python types.

        The dict is readily JSON or YAML serializable.
        Quantity unit information is stripped.

        This is mainly used at the moment to pass the data to
        the gamma-sky.net webpage.
        """
        out = {}
        for key, value in self.data.items():
            if isinstance(value, int):
                out_val = value
            else:
                # This works because almost all values in ``data``
                # are Numpy objects, and ``tolist`` works for Numpy
                # arrays and scalars.
                out_val = np.asarray(value).tolist()

            out[key] = out_val

        return out

    @property
    def position(self):
        """Source position (`~astropy.coordinates.SkyCoord`)."""
        table = table_from_row_data([self.data])
        return _skycoord_from_table(table)[0]


class SourceCatalog:
    """Generic source catalog.

    This class can be used directly, but it's mostly used as a
    base class for the other source catalog classes.

    This is a thin wrapper around `~astropy.table.Table`,
    which is stored in the ``catalog.table`` attribute.

    Parameters
    ----------
    table : `~astropy.table.Table`
        Table with catalog data.
    source_name_key : str
        Column with source name information
    source_name_alias : tuple of str
        Columns with source name aliases. This will allow accessing the source
        row by alias names as well.
    """

    source_object_class = SourceCatalogObject

    # TODO: at the moment these are duplicated in SourceCatalogObject.
    # Should we share them somehow?
    _source_index_key = "catalog_row_index"

    def __init__(self, table, source_name_key="Source_Name", source_name_alias=()):
        self.table = table
        self._source_name_key = source_name_key
        self._source_name_alias = source_name_alias

    def __str__(self):
        return self.description + f" with {len(self.table)} objects."

    @lazyproperty
    def _name_to_index_cache(self):
        # Make a dict for quick lookup: source name -> row index
        names = dict()
        for idx, row in enumerate(self.table):
            name = row[self._source_name_key]
            names[name.strip()] = idx
            for alias_column in self._source_name_alias:
                for alias in row[alias_column].split(","):
                    if not alias == "":
                        names[alias.strip()] = idx
        return names

    def row_index(self, name):
        """Look up row index of source by name.

        Parameters
        ----------
        name : str
            Source name

        Returns
        -------
        index : int
            Row index of source in table
        """
        index = self._name_to_index_cache[name]
        row = self.table[index]
        # check if name lookup is correct other wise recompute _name_to_index_cache

        possible_names = [row[self._source_name_key]]
        for alias_column in self._source_name_alias:
            possible_names += row[alias_column].split(",")

        if name not in possible_names:
            self.__dict__.pop("_name_to_index_cache")
            index = self._name_to_index_cache[name]
        return index

    def source_name(self, index):
        """Look up source name by row index.

        Parameters
        ----------
        index : int
            Row index of source in table
        """
        source_name_col = self.table[self._source_name_key]
        name = source_name_col[index]
        return name.strip()

    def __getitem__(self, key):
        """Get source by name.

        Parameters
        ----------
        key : str or int
            Source name or row index

        Returns
        -------
        source : `SourceCatalogObject`
            An object representing one source
        """
        if isinstance(key, str):
            index = self.row_index(key)
        elif _is_int(key):
            index = key
        else:
            raise TypeError(
                f"Invalid type: {key!r}\n"
                "Key must be source name string or row index integer. "
            )

        return self._make_source_object(index)

    def _make_source_object(self, index):
        """Make one source object.

        Parameters
        ----------
        index : int
            Row index

        Returns
        -------
        source : `SourceCatalogObject`
            Source object
        """
        data = table_row_to_dict(self.table[index])
        data[self._source_index_key] = index

        try:
            name_extended = data["Extended_Source_Name"].strip()
            idx = self._lookup_extended_source_idx[name_extended]
            data_extended = table_row_to_dict(self.extended_sources_table[idx])
        except KeyError:
            data_extended = None

        source = self.source_object_class(data, data_extended)
        return source

    @lazyproperty
    def _lookup_extended_source_idx(self):
        names = [_.strip() for _ in self.extended_sources_table["Source_Name"]]
        idx = range(len(names))
        return dict(zip(names, idx))

    @property
    def _data_python_list(self):
        """Convert catalog to a Python list with Python types.

        The list is readily JSON or YAML serializable.
        Quantity unit information is stripped.

        This is mainly used at the moment to pass the data to
        the gamma-sky.net webpage.
        """
        return [source._data_python_dict for source in self]

    @property
    def positions(self):
        """Source positions (`~astropy.coordinates.SkyCoord`)."""
        return _skycoord_from_table(self.table)

    def copy(self):
        """Copy catalog"""
        return copy.deepcopy(self)


def _skycoord_from_table(table):
    try:
        keys = table.colnames
    except AttributeError:
        keys = list(table.keys())

    if {"RAJ2000", "DEJ2000"}.issubset(keys):
        lon, lat, frame = "RAJ2000", "DEJ2000", "icrs"
    elif {"RA", "DEC"}.issubset(keys):
        lon, lat, frame = "RA", "DEC", "icrs"
    elif {"ra", "dec"}.issubset(keys):
        lon, lat, frame = "ra", "dec", "icrs"
    elif {"GLON", "GLAT"}.issubset(keys):
        lon, lat, frame = "GLON", "GLAT", "galactic"
    elif {"glon", "glat"}.issubset(keys):
        lon, lat, frame = "glon", "glat", "galactic"
    else:
        raise KeyError("No column GLON / GLAT or RA / DEC or RAJ2000 / DEJ2000 found.")

    unit = table[lon].unit.to_string() if table[lon].unit else "deg"

    return SkyCoord(table[lon], table[lat], unit=unit, frame=frame)
