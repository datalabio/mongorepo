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
from dataclasses import dataclass, field

# All Custom Imports Here.

# All Native Imports Here.
from mongorepo.types import Document, Documents


# All Attributes or Constants Here.


# -----------------------------------------------------------------------------
# INSERT
# -----------------------------------------------------------------------------
@dataclass(slots=True)
class InsertResult:
    """Result of insert_one()."""

    acknowledged: bool = True

    inserted_id: str | None = None

    document: Document | None = None


@dataclass(slots=True)
class InsertManyResult:
    """Result of insert_many()."""

    acknowledged: bool = True

    inserted_ids: list[str] = field(
        default_factory=list,
    )

    documents: Documents = field(
        default_factory=list,
    )


# -----------------------------------------------------------------------------
# UPDATE
# -----------------------------------------------------------------------------
@dataclass(slots=True)
class UpdateResult:
    """Result of update."""
    acknowledged: bool = True

    matched_count: int = 0

    modified_count: int = 0

    document: Document | None = None

    upserted_id: str | None = None

    @property
    def was_upserted(self) -> bool:
        return self.upserted_id is not None


@dataclass(slots=True)
class UpdateManyResult:
    """Result of update_many()."""

    acknowledged: bool = True

    matched_count: int = 0

    modified_count: int = 0

    documents: Documents = field(
        default_factory=list,
    )

    upserted_ids: list[str] = field(
        default_factory=list,
    )


# -----------------------------------------------------------------------------
# DELETE
# -----------------------------------------------------------------------------
@dataclass(slots=True)
class DeleteResult:
    """Result of delete_one()."""

    acknowledged: bool = True

    deleted_count: int = 0

    document: Document | None = None


@dataclass(slots=True)
class DeleteManyResult:
    """Result of delete_many()."""

    acknowledged: bool = True

    deleted_count: int = 0

    documents: Documents = field(
        default_factory=list,
    )


# -----------------------------------------------------------------------------
# BULK
# -----------------------------------------------------------------------------
@dataclass(slots=True)
class BulkResult:
    """Result of bulk_write()."""

    acknowledged: bool = True

    inserted_count: int = 0

    matched_count: int = 0

    modified_count: int = 0

    deleted_count: int = 0

    upserted_count: int = 0

    inserted_ids: list[str] = field(
        default_factory=list,
    )

    upserted_ids: list[str] = field(
        default_factory=list,
    )


# -----------------------------------------------------------------------------
# INDEXES
# -----------------------------------------------------------------------------
@dataclass(slots=True)
class IndexSyncResult:
    """Result of index synchronization."""

    created: list[str] = field(
        default_factory=list,
    )

    dropped: list[str] = field(
        default_factory=list,
    )

    skipped: list[str] = field(
        default_factory=list,
    )


if __name__ == '__main__':
    pass
