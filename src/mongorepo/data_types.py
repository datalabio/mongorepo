"""
Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
```
https://www.apache.org/licenses/LICENSE-2.0
```
File: data_types.py
Description:

"""

# All Python Built-in Imports Here.
from typing import Annotated

# All Custom Imports Here.
from bson import ObjectId
from pydantic import BeforeValidator, PlainSerializer


# All Native Imports Here.

# All Attributes or Constants Here.

def _serialize_object_id(value: str | ObjectId | None) -> str | None:
    if value is None:
        return None

    return str(value)


PyObjectId = Annotated[
    str,
    BeforeValidator(str),
    PlainSerializer(_serialize_object_id, when_used="always")
]

if __name__ == '__main__':
    pass
