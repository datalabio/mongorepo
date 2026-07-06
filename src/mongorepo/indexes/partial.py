"""
Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
```
https://www.apache.org/licenses/LICENSE-2.0
```
File: partial.py
Description:
    MongoDB partial index definition.
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
class PartialIndex(BaseIndex):
    """MongoDB partial index.
    Example:
        PartialIndex(
            fields=[
                ("email", SortOrder.ASC),
            ],
            filter={
                "deleted": False,
            },
        )
    """

    fields: list[tuple[str, SortOrder]]

    filter: dict[str, Any]

    def keys(self) -> list[tuple[str, Any]]:
        return [
            (
                field,
                order.value,
            )
            for field, order in self.fields
        ]

    def options(self) -> dict[str, Any]:
        options = super().options()

        options["partialFilterExpression"] = (
            self.filter
        )

        return options


if __name__ == '__main__':
    pass
