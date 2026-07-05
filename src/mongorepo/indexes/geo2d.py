"""
Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
```
https://www.apache.org/licenses/LICENSE-2.0
```
File: geo2d.py
Description:
    MongoDB geo2d index definition.
"""

# All Python Built-in Imports Here.
from __future__ import annotations
from typing import Any
from dataclasses import dataclass

# All Custom Imports Here.

# All Native Imports Here.
from mongorepo.indexes.base import BaseIndex


# All Attributes or Constants Here.


@dataclass(slots=True, kw_only=True)
class Geo2DIndex(BaseIndex):
    """
    MongoDB geo2d index.

    Example:

        Geo2DIndex(
            field="location",
        )
    """

    field: str

    def keys(self) -> list[tuple[str, Any]]:
        return [
            (
                self.field,
                "2d",
            )
        ]


if __name__ == '__main__':
    pass
