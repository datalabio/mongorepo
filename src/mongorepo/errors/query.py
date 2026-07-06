"""
Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
```
https://www.apache.org/licenses/LICENSE-2.0
```
File: query
Description:

"""

# All Python Built-in Imports Here.
from __future__ import annotations

# All Custom Imports Here.

# All Native Imports Here.
from mongorepo.errors import MongoRepoError


# All Attributes or Constants Here.

class QueryError(MongoRepoError):
    """Raised when query construction is invalid."""

    default_message = "Invalid query."


class PaginationError(QueryError):
    """Raised when pagination parameters are invalid."""

    default_message = "Invalid pagination parameters."


class AggregationError(QueryError):
    """Raised when aggregation pipeline execution fails."""

    default_message = "Aggregation pipeline failed."


if __name__ == '__main__':
    pass
