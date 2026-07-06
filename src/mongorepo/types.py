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
from pymongo.asynchronous.client_session import AsyncClientSession

# All Native Imports Here.

# All Attributes or Constants Here.


# -----------------------------------------------------------------------------
# MongoDB Documents
# -----------------------------------------------------------------------------

Document: TypeAlias = dict[str, Any]

Documents: TypeAlias = list[Document]

# -----------------------------------------------------------------------------
# Query Types
# -----------------------------------------------------------------------------

Filter: TypeAlias = dict[str, Any]

Update: TypeAlias = dict[str, Any]

Pipeline: TypeAlias = list[dict[str, Any]]

# -----------------------------------------------------------------------------
# Projection
# -----------------------------------------------------------------------------

Projection: TypeAlias = list[str] | dict[str, int] | None

# -----------------------------------------------------------------------------
# Sorting
# -----------------------------------------------------------------------------

SortField: TypeAlias = tuple[str, int]

Sort: TypeAlias = list[SortField] | None

# -----------------------------------------------------------------------------
# MongoDB Session
# -----------------------------------------------------------------------------

Session: TypeAlias = AsyncClientSession | None

if __name__ == '__main__':
    pass
