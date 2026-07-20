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
from enum import Enum


# All Custom Imports Here.

# All Native Imports Here.

# All Attributes or Constants Here.


class SortOrder(int, Enum):
    """MongoDB index sort order.
    Example:
        SortOrder.ASC
        SortOrder.DESC
    """

    ASC = 1
    DESC = -1


class TextOrder(str, Enum):
    """MongoDB text index type."""

    TEXT = "text"


class HashedOrder(str, Enum):
    """MongoDB hashed index type."""

    HASHED = "hashed"


class Geo2DOrder(str, Enum):
    """MongoDB geo2d index type."""

    GEO2D = "2d"


class GeoSphereOrder(str, Enum):
    """MongoDB geosphere index type."""

    GEOSPHERE = "2dsphere"


if __name__ == '__main__':
    pass
