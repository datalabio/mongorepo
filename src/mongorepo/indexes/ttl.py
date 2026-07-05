"""
Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
```
https://www.apache.org/licenses/LICENSE-2.0
```
File: ttl.py
Description:
    MongoDB TTL index definition.
"""

# All Python Built-in Imports Here.
from __future__ import annotations
from typing import Any
from dataclasses import dataclass

# All Custom Imports Here.

# All Native Imports Here.
from mongorepo.indexes.base import BaseIndex
from mongorepo.indexes.enums import SortOrder


# All Attributes or Constants Here.


@dataclass(slots=True, kw_only=True)
class TTLIndex(BaseIndex):
    """
    MongoDB TTL index.

    Example:

        TTLIndex(
            field="expires_at",
            expire_after_seconds=3600,
        )
    """

    field: str

    order: SortOrder = SortOrder.ASC

    expire_after_seconds: int = 0

    def keys(self) -> list[tuple[str, Any]]:
        return [
            (
                self.field,
                self.order.value,
            )
        ]

    def options(self) -> dict[str, Any]:
        options = super().options()

        options["expireAfterSeconds"] = (
            self.expire_after_seconds
        )

        return options


if __name__ == '__main__':
    pass
