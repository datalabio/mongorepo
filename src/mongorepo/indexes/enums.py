"""
Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
```
https://www.apache.org/licenses/LICENSE-2.0
```
File: enums.py
Description:
    Enumerations used by MongoDB index definitions.
"""

# All Python Built-in Imports Here.
from __future__ import annotations
from enum import IntEnum, StrEnum


# All Custom Imports Here.

# All Native Imports Here.

# All Attributes or Constants Here.


class SortOrder(IntEnum):
    """
    MongoDB index sort order.

    Example:

        SortOrder.ASC
        SortOrder.DESC
    """

    ASC = 1
    DESC = -1


class TextOrder(StrEnum):
    """
    MongoDB text index type.
    """

    TEXT = "text"


class HashedOrder(StrEnum):
    """
    MongoDB hashed index type.
    """

    HASHED = "hashed"


class Geo2DOrder(StrEnum):
    """
    MongoDB geo2d index type.
    """

    GEO2D = "2d"


class GeoSphereOrder(StrEnum):
    """
    MongoDB geosphere index type.
    """

    GEOSPHERE = "2dsphere"


if __name__ == '__main__':
    pass
