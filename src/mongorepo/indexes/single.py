"""
Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
```
https://www.apache.org/licenses/LICENSE-2.0
```
File: single.py
Description:
    Single field index definition.
"""

# All Python Built-in Imports Here.
from __future__ import annotations
from typing import Any
from dataclasses import dataclass

# All Custom Imports Here.
from mongorepo.indexes.base import BaseIndex
from mongorepo.indexes.enums import SortOrder


# All Native Imports Here.

# All Attributes or Constants Here.


@dataclass(slots=True, kw_only=True)
class SingleFieldIndex(BaseIndex):
    """Single field MongoDB index.
    Example:
        SingleFieldIndex(
            field="email",
            unique=True,
        )
    """

    field: str

    order: SortOrder = SortOrder.ASC

    def keys(self) -> list[tuple[str, Any]]:
        return [
            (
                self.field,
                self.order.value,
            )
        ]


if __name__ == '__main__':
    pass
