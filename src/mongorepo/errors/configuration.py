"""
Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
```
https://www.apache.org/licenses/LICENSE-2.0
```
File: configuration.py
Description:

"""

# All Python Built-in Imports Here.
from __future__ import annotations

# All Custom Imports Here.

# All Native Imports Here.
from mongorepo.errors import MongoRepoError


# All Attributes or Constants Here.


class ConfigurationError(MongoRepoError):
    """Base configuration error."""

    default_message = "Invalid mongorepo configuration."


class RepositoryConfigurationError(ConfigurationError):
    """Repository configuration error."""

    default_message = "Invalid repository configuration."


class IndexConfigurationError(ConfigurationError):
    """Index configuration error."""

    default_message = "Invalid index configuration."


if __name__ == '__main__':
    pass
