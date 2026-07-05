"""
Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
```
https://www.apache.org/licenses/LICENSE-2.0
```
File: types.py
Description:

"""

# All Python Built-in Imports Here.
from __future__ import annotations
from typing import Any, TypeAlias

# All Custom Imports Here.

# All Native Imports Here.

# All Attributes or Constants Here.

Filter: TypeAlias = dict[str, Any]

Projection: TypeAlias = (
        list[str]
        | dict[str, int]
        | None)

Sort: TypeAlias = (
        list[tuple[str, int]]
        | None
)

Update: TypeAlias = dict[str, Any]

Pipeline: TypeAlias = list[dict[str, Any]]

if __name__ == '__main__':
    pass
