"""
Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
```
https://www.apache.org/licenses/LICENSE-2.0
```
File: results.py
Description:
    Repository operation result objects.
"""

# All Python Built-in Imports Here.
from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, TypeVar

# All Custom Imports Here.

# All Native Imports Here.
from mongorepo.models import MongoModel

# All Attributes or Constants Here.
T = TypeVar(
    "T",
    bound=MongoModel,
)


# ==========================================================
# INSERT
# ==========================================================

@dataclass(slots=True)
class InsertResult(Generic[T]):
    """
    Result of insert_one().
    """

    inserted_id: str

    document: T | None = None


@dataclass(slots=True)
class InsertManyResult(Generic[T]):
    """
    Result of insert_many().
    """

    inserted_ids: list[str]

    documents: list[T] | None = None


# ==========================================================
# UPDATE
# ==========================================================

@dataclass(slots=True)
class UpdateResult(Generic[T]):
    """
    Result of update_one().
    """

    matched_count: int

    modified_count: int

    document: T | None = None

    upserted_id: str | None = None


@dataclass(slots=True)
class UpdateManyResult(Generic[T]):
    """
    Result of update_many().
    """

    matched_count: int

    modified_count: int

    documents: list[T] | None = None

    upserted_ids: list[str] | None = None


# ==========================================================
# DELETE
# ==========================================================

@dataclass(slots=True)
class DeleteResult(Generic[T]):
    """
    Result of delete_one().
    """

    deleted_count: int

    document: T | None = None


@dataclass(slots=True)
class DeleteManyResult(Generic[T]):
    """
    Result of delete_many().
    """

    deleted_count: int

    documents: list[T] | None = None


# ==========================================================
# BULK
# ==========================================================

@dataclass(slots=True)
class BulkResult:
    """
    Result of bulk_write().
    """

    inserted_count: int = 0

    matched_count: int = 0

    modified_count: int = 0

    deleted_count: int = 0

    upserted_count: int = 0

    inserted_ids: list[str] | None = None

    upserted_ids: list[str] | None = None


if __name__ == '__main__':
    pass
