"""
Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
```
https://www.apache.org/licenses/LICENSE-2.0
```
File: repository
Description:

"""

# All Python Built-in Imports Here.
from __future__ import annotations
from typing import Any

# All Custom Imports Here.

# All Native Imports Here.
from mongorepo.errors import MongoRepoError


# All Attributes or Constants Here.


class RepositoryError(MongoRepoError):
    """Base exception for repository operations."""

    default_message = "Repository operation failed."


class CreateError(RepositoryError):
    """Raised when document creation fails."""

    default_message = "Failed to create document."


class ReadError(RepositoryError):
    """Raised when document retrieval fails."""

    default_message = "Failed to read document."


class UpdateError(RepositoryError):
    """Raised when document update fails."""

    default_message = "Failed to update document."


class DeleteError(RepositoryError):
    """Raised when document deletion fails."""

    default_message = "Failed to delete document."


class BulkOperationError(RepositoryError):
    """Raised when bulk operations fail."""

    default_message = "Bulk operation failed."


class DuplicateDocumentError(RepositoryError):
    """Raised when a document already exists."""

    default_message = "Document already exists."

    def __init__(
            self,
            collection: str | None = None,
            identifier: Any | None = None,
    ):
        if collection and identifier is not None:
            message = (
                f"Document already exists in "
                f"'{collection}' for identifier '{identifier}'."
            )
        else:
            message = self.default_message

        super().__init__(message)


class DocumentNotFoundError(RepositoryError):
    """Raised when a document cannot be found."""

    default_message = "Document not found."

    def __init__(
            self,
            collection: str | None = None,
            identifier: Any | None = None,
    ):
        if collection and identifier is not None:
            message = (
                f"Document not found in "
                f"'{collection}' for identifier '{identifier}'."
            )
        else:
            message = self.default_message

        super().__init__(message)


if __name__ == '__main__':
    pass
