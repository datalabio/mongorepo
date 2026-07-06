"""
Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
```
https://www.apache.org/licenses/LICENSE-2.0
```
File: base.py
Description:
    Base index definition.
"""

# All Python Built-in Imports Here.
from __future__ import annotations
from typing import Any
from dataclasses import dataclass
from abc import ABC, abstractmethod


# All Custom Imports Here.

# All Native Imports Here.

# All Attributes or Constants Here.


@dataclass(slots=True, kw_only=True)
class BaseIndex(ABC):
    """Base class for all MongoDB indexes."""

    name: str | None = None

    unique: bool = False

    sparse: bool = False

    background: bool = True

    hidden: bool = False

    @abstractmethod
    def keys(self) -> list[tuple[str, Any]]:
        """Return MongoDB index keys."""
        raise NotImplementedError

    def options(self) -> dict[str, Any]:
        """Return MongoDB index options."""
        options: dict[str, Any] = {}

        if self.name:
            options["name"] = self.name

        if self.unique:
            options["unique"] = True

        if self.sparse:
            options["sparse"] = True

        if self.background:
            options["background"] = True

        if self.hidden:
            options["hidden"] = True

        return options

    def to_pymongo(
            self,
    ) -> tuple[list[tuple[str, Any]], dict[str, Any]]:
        """Convert to PyMongo create_index arguments."""
        return (
            self.keys(),
            self.options(),
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"("
            f"name={self.name!r}, "
            f"keys={self.keys()!r}"
            f")"
        )


if __name__ == '__main__':
    pass
