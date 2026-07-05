"""
Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
```
https://www.apache.org/licenses/LICENSE-2.0
```
File: helpers.py
Description:

"""

# All Python Built-in Imports Here.
from datetime import datetime, timezone


# All Custom Imports Here.

# All Native Imports Here.

# All Attributes or Constants Here.


def get_utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


if __name__ == '__main__':
    pass
