"""
Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
```
https://www.apache.org/licenses/LICENSE-2.0
```
File: database
Description:

"""

# All Python Built-in Imports Here.
from __future__ import annotations

# All Custom Imports Here.

# All Native Imports Here.
from mongorepo.errors import MongoRepoError


# All Attributes or Constants Here.


class DatabaseError(MongoRepoError):
    """Base exception for all database-related failures."""

    default_message = "A database error occurred."


class DatabaseConfigurationError(DatabaseError):
    """Raised when database configuration is invalid."""

    default_message = "Invalid database configuration."


class DatabaseConnectionError(DatabaseError):
    """Raised when a connection to MongoDB cannot be established."""

    default_message = "Failed to connect to MongoDB."


class DatabaseDisconnectionError(DatabaseError):
    """Raised when MongoDB connection cannot be closed properly."""

    default_message = "Failed to disconnect from MongoDB."


class DatabaseCollectionError(DatabaseError):
    """Raised when a collection cannot be accessed or created."""

    default_message = "Collection operation failed."


class DatabaseSessionError(DatabaseError):
    """Raised when MongoDB session creation or usage fails."""

    default_message = "MongoDB session failed."


class DatabaseTransactionError(DatabaseError):
    """Raised when a transaction fails."""

    default_message = "MongoDB transaction failed."


class DatabaseOperationError(DatabaseError):
    """Generic database operation failure."""

    default_message = "Database operation failed."


class DatabaseHealthCheckError(DatabaseError):
    """Raised when database health verification fails."""

    default_message = "Database health check failed."


class DatabaseTimeoutError(DatabaseError):
    """Raised when a database operation exceeds the configured timeout."""

    default_message = "Database operation timed out."


if __name__ == '__main__':
    pass
