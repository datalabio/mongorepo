"""
Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
```
https://www.apache.org/licenses/LICENSE-2.0
```
File: wildcard.py
Description:
    MongoDB wildcard index definition.
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
class WildcardIndex(BaseIndex):
    """
    MongoDB wildcard index.

    Examples:

        WildcardIndex()

        WildcardIndex(
            field="metadata.$**",
        )
    """

    field: str = "$**"

    def keys(self) -> list[tuple[str, Any]]:
        return [
            (
                self.field,
                1,
            )
        ]


if __name__ == '__main__':
    pass
