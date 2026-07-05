"""
Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
```
https://www.apache.org/licenses/LICENSE-2.0
```
File: text.py
Description:
    MongoDB text index definition.
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
class TextIndex(BaseIndex):
    """
    MongoDB text index.

    Example:

        TextIndex(
            fields=[
                "title",
                "description",
            ],
            weights={
                "title": 10,
                "description": 2,
            },
        )
    """

    fields: list[str]

    weights: dict[str, int] | None = None

    default_language: str = "english"

    def keys(self) -> list[tuple[str, Any]]:
        return [
            (
                field,
                "text",
            )
            for field in self.fields
        ]

    def options(self) -> dict[str, Any]:
        options = super().options()

        options["default_language"] = (
            self.default_language
        )

        if self.weights:
            options["weights"] = self.weights

        return options


if __name__ == '__main__':
    pass
