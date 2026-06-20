"""
Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
```
https://www.apache.org/licenses/LICENSE-2.0
```
File: __init__
Description:

"""

# All Python Built-in Imports Here.
from __future__ import annotations
from typing import Any


# All Custom Imports Here.

# All Native Imports Here.

# All Attributes or Constants Here.


class MongoRepoError(Exception):
    """
    Base exception for all mongorepo exceptions.
    """

    default_message = "An unknown mongorepo error occurred."

    def __init__(
            self,
            message: str | None = None,
            *,
            details: Any | None = None,
    ):
        self.message = message or self.default_message
        self.details = details

        super().__init__(self.message)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(message={self.message!r}, details={self.details!r})"
        )


if __name__ == '__main__':
    pass
