"""
Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
```
https://www.apache.org/licenses/LICENSE-2.0
```
File: __init__.py
Description:

"""

# All Python Built-in Imports Here.

# All Custom Imports Here.

# All Native Imports Here.
from mongorepo.indexes.enums import SortOrder

from mongorepo.indexes.base import BaseIndex

from mongorepo.indexes.single import SingleFieldIndex
from mongorepo.indexes.compound import CompoundIndex

from mongorepo.indexes.ttl import TTLIndex
from mongorepo.indexes.text import TextIndex

from mongorepo.indexes.hashed import HashedIndex

from mongorepo.indexes.geo2d import Geo2DIndex

from mongorepo.indexes.partial import PartialIndex

from mongorepo.indexes.wildcard import WildcardIndex

# All Attributes or Constants Here.


__all__ = [
    "SortOrder",

    "BaseIndex",

    "SingleFieldIndex",
    "CompoundIndex",

    "TTLIndex",
    "TextIndex",

    "HashedIndex",

    "Geo2DIndex",

    "PartialIndex",

    "WildcardIndex",
]

if __name__ == '__main__':
    pass
