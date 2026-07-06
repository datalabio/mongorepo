"""
Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
```
https://www.apache.org/licenses/LICENSE-2.0
```
File: enums.py
Description:

"""

# All Python Built-in Imports Here.
from __future__ import annotations
from enum import StrEnum


# All Custom Imports Here.

# All Native Imports Here.

# All Attributes or Constants Here.


class ReturnType(StrEnum):
    """Repository return strategy.
    DOCUMENT:
        Return DOCUMENT.
    ID:
        Return inserted/updated id(s).
    NONE:
        Return nothing.
    """
    DOCUMENT = "document"
    ID = "id"
    NONE = "none"


if __name__ == '__main__':
    pass
