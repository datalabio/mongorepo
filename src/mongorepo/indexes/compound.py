"""
Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
```
https://www.apache.org/licenses/LICENSE-2.0
```
File: compound.py
Description:
    Compound MongoDB index definition.
Example:
from mongorepo.indexes import SingleFieldIndex, CompoundIndex, SortOrder

indexes = [

    SingleFieldIndex(
        field="email",
        unique=True,
        name="email_unique",
    ),

    CompoundIndex(
        fields=[
            (
                "status",
                SortOrder.ASC,
            ),
            (
                "created_at",
                SortOrder.DESC,
            ),
        ],
        name="status_created_idx",
    ),
]
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
class CompoundIndex(BaseIndex):
    """
    Compound MongoDB index.

    Example:

        CompoundIndex(
            fields=[
                ("status", SortOrder.ASC),
                ("created_at", SortOrder.DESC),
            ]
        )
    """

    fields: list[tuple[str, SortOrder]]

    def keys(self) -> list[tuple[str, Any]]:
        return [
            (
                field,
                order.value,
            )
            for field, order in self.fields
        ]


if __name__ == '__main__':
    pass
