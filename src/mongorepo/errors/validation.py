"""
Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
```
https://www.apache.org/licenses/LICENSE-2.0
```
File: validation
Description:

"""

# All Python Built-in Imports Here.
from __future__ import annotations

# All Custom Imports Here.

# All Native Imports Here.
from mongorepo.errors import MongoRepoError


# All Attributes or Constants Here.


class ValidationError(MongoRepoError):
    """Raised when validation fails before reaching MongoDB."""

    default_message = "Validation failed."


if __name__ == '__main__':
    pass
