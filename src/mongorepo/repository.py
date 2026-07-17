"""
Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
```
https://www.apache.org/licenses/LICENSE-2.0
```
File: repository.py
Description:
    Generic MongoDB repository implementation.
"""

# All Python Built-in Imports Here.
from __future__ import annotations
from typing import ClassVar

from _testcapi import awaitType
# All Custom Imports Here.
from bson import ObjectId
from bson.errors import InvalidId
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.errors import DuplicateKeyError, PyMongoError, BulkWriteError

# All Native Imports Here.
from mongorepo import get_logger
from mongorepo.enums import ReturnType
from mongorepo.database import Database
from mongorepo.errors.query import AggregationError
from mongorepo.errors.configuration import ConfigurationError
from mongorepo.indexes import BaseIndex
from mongorepo.errors.repository import (
    DocumentNotFoundError,
    UpdateError,
    BulkOperationError,
    ReadError,
    DeleteError,
    DuplicateDocumentError,
    CreateError
)
from mongorepo.types import (
    Documents,
    Document,
    Filter,
    Update,
    Projection,
    Session,
    Sort,
    Pipeline,
)
from mongorepo.results import (
    DeleteResult,
    DeleteManyResult,
    InsertResult,
    InsertManyResult,
    UpdateResult,
    UpdateManyResult, IndexSyncResult,
    BulkResult,
)

# All Attributes or Constants Here.
logger = get_logger()


class BaseRepository:
    """Generic MongoDB repository.
    Example:
        class UserRepository(
            BaseRepository,
        ):
            collection_name = "users"
    """
    # Repository metadata
    collection_name: ClassVar[str]

    indexes: ClassVar[list[BaseIndex]] = []

    # Repository initialization
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if (cls.__name__ != "BaseRepository" and
                not getattr(cls, "collection_name", None)):
            raise ConfigurationError(
                f"{cls.__name__} must define 'collection_name'.")

    # -------------------------------------------------------------------------
    # Collection Helpers
    # -------------------------------------------------------------------------
    @classmethod
    def collection(cls) -> AsyncCollection:
        """Return MongoDB collection."""
        return Database.get_collection(cls.collection_name)

    @staticmethod
    def object_id(value: str) -> ObjectId:
        """Convert string to ObjectId."""
        try:
            return ObjectId(value)

        except InvalidId as exc:
            raise ValueError(f"Invalid ObjectId: {value}") from exc

    @staticmethod
    def object_ids(values: list[str]) -> list[ObjectId]:
        """Convert list of strings to ObjectIds."""
        return [BaseRepository.object_id(value, ) for value in values]

    # -------------------------------------------------------------------------
    # Normalizers
    # -------------------------------------------------------------------------
    @staticmethod
    def normalize_projection(projection: Projection) -> dict[str, int] | None:
        """Normalize projection.
        Supports:
            ["name", "email"]
        and:
            {
                "name": 1,
                "email": 1,
            }
        """
        if projection is None:
            return None

        if isinstance(projection, dict):
            return projection

        return {field: 1 for field in projection}

    @staticmethod
    def normalize_update(update: Update | None = None, **kwargs) -> Update:
        """Normalize update expression.
        Supports:
            {"$set": {...}}
        and:
            name="Amol",
            age=33
        """
        if update is not None:
            # MongoDB operators
            if any(key.startswith("$") for key in update):
                return update

            # Plain dictionary
            return {"$set": update}

        return {"$set": kwargs}

    @staticmethod
    def normalize_session(session: Session) -> Session:
        """Normalize MongoDB session."""
        return session

    # -------------------------------------------------------------------------
    # Document Helpers
    # -------------------------------------------------------------------------
    @classmethod
    def prepare_document(cls, document: Document) -> Document:
        """Prepare document for MongoDB.
        - Creates a copy.
        - Converts string _id to ObjectId.
        - Removes null _id.
        """
        document = document.copy()

        if "_id" not in document:
            return document

        # Remove empty _id
        if document["_id"] is None:
            document.pop("_id", None)

            return document

        # Convert string id
        if isinstance(document["_id"], str):
            document["_id"] = cls.object_id(document["_id"])

        return document

    # -------------------------------------------------------------------------
    # CREATE
    # -------------------------------------------------------------------------
    @classmethod
    async def create(
            cls,
            document: Document,
            *,
            session: Session = None,
            return_type: ReturnType = ReturnType.DOCUMENT
    ) -> InsertResult:
        """Create a single document."""
        try:
            document = cls.prepare_document(document)
            result = await cls.collection().insert_one(
                document,
                session=session
            )

            inserted_id = str(result.inserted_id)

            return InsertResult(
                acknowledged=result.acknowledged,
                inserted_id=inserted_id,
                document=(
                    document if return_type == ReturnType.DOCUMENT else None
                )
            )

        except DuplicateKeyError as exc:
            raise DuplicateDocumentError(cls.collection_name) from exc

        except PyMongoError as exc:
            raise CreateError(f"Failed to create document: {exc}") from exc

    @classmethod
    async def create_many(
            cls,
            documents: Documents,
            *,
            session: Session = None,
            ordered: bool = True,
            return_type: ReturnType = ReturnType.DOCUMENT,
    ) -> InsertManyResult:
        """Create multiple documents."""
        try:
            documents = [
                cls.prepare_document(document) for document in documents
            ]

            result = await (
                cls.collection().insert_many(
                    documents,
                    ordered=ordered,
                    session=session,
                )
            )

            inserted_ids = [str(id_) for id_ in result.inserted_ids]

            return InsertManyResult(
                acknowledged=result.acknowledged,
                inserted_ids=inserted_ids,
                documents=(
                    documents if return_type == ReturnType.DOCUMENT else []
                )
            )

        except DuplicateKeyError as exc:
            raise DuplicateDocumentError(cls.collection_name) from exc

        except PyMongoError as exc:
            raise CreateError(f"Failed to create documents: {exc}") from exc

    # -------------------------------------------------------------------------
    # READ
    # -------------------------------------------------------------------------
    @classmethod
    async def find_by_id(
            cls,
            id_: str,
            *,
            projection: Projection = None,
            session: Session = None,
    ) -> Document | None:
        """Find document by _id."""
        try:
            return await (
                cls.collection().find_one(
                    {"_id": cls.object_id(id_)},
                    projection=cls.normalize_projection(projection),
                    session=session
                )
            )

        except PyMongoError as exc:
            raise ReadError(f"Failed to find document by id: {exc}") from exc

    @classmethod
    async def find_one(
            cls,
            document_filter: Filter,
            *,
            projection: Projection = None,
            sort: Sort = None,
            session: Session = None,
    ) -> Document | None:
        """Find single document."""
        try:
            return await (
                cls.collection().find_one(
                    document_filter,
                    projection=cls.normalize_projection(projection),
                    sort=sort,
                    session=session,
                )
            )

        except PyMongoError as exc:
            raise ReadError(f"Failed to find document: {exc}") from exc

    @classmethod
    async def find(
            cls,
            document_filter: Filter | None = None,
            *,
            projection: Projection = None,
            sort: Sort = None,
            skip: int = 0,
            limit: int | None = None,
            session: Session = None,
    ) -> Documents:
        """Find multiple documents."""
        try:
            cursor = cls.collection().find(
                document_filter or {},
                projection=cls.normalize_projection(projection),
                sort=sort,
                skip=skip,
                session=session,
            )

            if limit is not None:
                cursor = cursor.limit(limit)

            return await cursor.to_list(length=None)

        except PyMongoError as exc:
            raise ReadError(f"Failed to find documents: {exc}") from exc

    @classmethod
    async def exists(
            cls,
            document_filter: Filter,
            *,
            session: Session = None,
    ) -> bool:
        """Check if document exists."""
        try:
            document = await (
                cls.collection().find_one(
                    document_filter,
                    projection={"_id": 1},
                    session=session,
                )
            )

            return document is not None

        except PyMongoError as exc:
            raise ReadError(
                f"Failed to check document existence: {exc}") from exc

    @classmethod
    async def count(
            cls,
            document_filter: Filter | None = None,
            *,
            session: Session = None,
    ) -> int:
        """Count documents."""
        try:
            return await (
                cls.collection().count_documents(
                    document_filter or {},
                    session=session,
                )
            )

        except PyMongoError as exc:
            raise ReadError(f"Failed to count documents: {exc}") from exc

    # -------------------------------------------------------------------------
    # UPDATE
    # -------------------------------------------------------------------------
    @classmethod
    async def save(
            cls,
            document: Document,
            *,
            session: Session = None,
    ) -> UpdateResult:
        """Replace entire document."""
        try:
            document = cls.prepare_document(document)

            object_id = document.get("_id")

            if object_id is None:
                raise ValueError("Document must contain '_id'.")

            result = await (
                cls.collection().replace_one(
                    {"_id": object_id},
                    document,
                    session=session,
                )
            )

            if result.matched_count == 0:
                raise DocumentNotFoundError(cls.collection_name)

            return UpdateResult(
                acknowledged=result.acknowledged,
                matched_count=result.matched_count,
                modified_count=result.modified_count,
                document=document,
            )

        except DocumentNotFoundError:
            raise

        except PyMongoError as exc:
            raise UpdateError(f"Failed to save document: {exc}") from exc

    @classmethod
    async def update_by_id(
            cls,
            id_: str,
            update: Update | None = None,
            *,
            session: Session = None,
            return_type: ReturnType = (
                    ReturnType.DOCUMENT
            ),
            **kwargs,
    ) -> UpdateResult:
        """Update document by id."""
        return await cls.update_one(
            {"_id": cls.object_id(id_)},
            update,
            session=session,
            return_type=return_type,
            **kwargs,
        )

    @classmethod
    async def update_one(
            cls,
            document_filter: Filter,
            update: Update | None = None,
            *,
            session: Session = None,
            return_type: ReturnType = ReturnType.DOCUMENT,
            **kwargs,
    ) -> UpdateResult:
        """Update a single document."""
        try:

            normalized_update = cls.normalize_update(update, **kwargs)

            result = await (
                cls.collection().update_one(
                    document_filter,
                    normalized_update,
                    session=session,
                )
            )

            if result.matched_count == 0:
                raise DocumentNotFoundError(cls.collection_name)

            document = None
            if return_type == ReturnType.DOCUMENT:
                document = await (
                    cls.collection().find_one(
                        document_filter,
                        session=session,
                    )
                )

            return UpdateResult(
                acknowledged=result.acknowledged,
                matched_count=result.matched_count,
                modified_count=result.modified_count,
                document=document,
                upserted_id=(
                    str(result.upserted_id) if result.upserted_id else None
                ),
            )

        except DocumentNotFoundError:
            raise

        except PyMongoError as exc:
            raise UpdateError(f"Failed to update document: {exc}") from exc

    @classmethod
    async def update_many(
            cls,
            document_filter: Filter,
            update: Update | None = None,
            *,
            session: Session = None,
            return_type: ReturnType = ReturnType.NONE,
            **kwargs,
    ) -> UpdateManyResult:
        """Update multiple documents."""
        try:
            normalized_update = cls.normalize_update(update, **kwargs)

            result = await (
                cls.collection().update_many(
                    document_filter,
                    normalized_update,
                    session=session,
                )
            )

            documents = []

            if return_type == ReturnType.DOCUMENT:
                cursor = cls.collection().find(
                    document_filter,
                    session=session
                )

                documents = await cursor.to_list(length=None)

            return UpdateManyResult(
                acknowledged=result.acknowledged,
                matched_count=result.matched_count,
                modified_count=result.modified_count,
                documents=documents,
            )

        except PyMongoError as exc:
            raise UpdateError(f"Failed to update documents: {exc}") from exc

    # -------------------------------------------------------------------------
    # DELETE
    # -------------------------------------------------------------------------
    @classmethod
    async def delete_by_id(
            cls,
            id_: str,
            *,
            session: Session = None,
            return_type: ReturnType = ReturnType.NONE,
    ) -> DeleteResult:
        """Delete document by id."""
        return await cls.delete_one(
            {"_id": cls.object_id(id_)},
            session=session,
            return_type=return_type,
        )

    @classmethod
    async def delete_one(
            cls,
            document_filter: Filter,
            *,
            session: Session = None,
            return_type: ReturnType = ReturnType.NONE,
    ) -> DeleteResult:
        """Delete a single document."""
        try:
            document = None

            # Fetch document only when requested
            if return_type == ReturnType.DOCUMENT:
                document = await (
                    cls.collection().find_one(
                        document_filter,
                        session=session,
                    )
                )

            result = await (
                cls.collection().delete_one(
                    document_filter,
                    session=session,
                )
            )

            if result.deleted_count == 0:
                raise DocumentNotFoundError(
                    cls.collection_name,
                )

            return DeleteResult(
                acknowledged=result.acknowledged,
                deleted_count=result.deleted_count,
                document=document,
            )

        except DocumentNotFoundError:
            raise

        except PyMongoError as exc:
            raise DeleteError(f"Failed to delete document: {exc}") from exc

    @classmethod
    async def delete_many(
            cls,
            document_filter: Filter,
            *,
            session: Session = None,
            return_type: ReturnType = ReturnType.NONE,
    ) -> DeleteManyResult:
        """Delete multiple documents."""
        try:
            documents = []

            # Fetch documents only when requested
            if return_type == ReturnType.DOCUMENT:
                cursor = cls.collection().find(
                    document_filter,
                    session=session,
                )

                documents = await cursor.to_list(length=None)

            result = await (
                cls.collection().delete_many(
                    document_filter,
                    session=session,
                )
            )

            return DeleteManyResult(
                acknowledged=result.acknowledged,
                deleted_count=result.deleted_count,
                documents=documents,
            )

        except PyMongoError as exc:
            raise DeleteError(f"Failed to delete documents: {exc}") from exc

    # -------------------------------------------------------------------------
    # UPSERT
    # -------------------------------------------------------------------------
    @classmethod
    async def upsert(
            cls,
            document_filter: Filter,
            update: Update | None = None,
            *,
            session: Session = None,
            return_type: ReturnType = ReturnType.NONE,
            **kwargs,
    ) -> UpdateResult:
        """Update existing document or insert a new one."""
        try:
            normalized_update = cls.normalize_update(update, **kwargs)

            result = await (
                cls.collection().update_one(
                    document_filter,
                    normalized_update,
                    upsert=True,
                    session=session,
                )
            )

            document = None
            if return_type == ReturnType.DOCUMENT:
                document = await (
                    cls.collection().find_one(
                        document_filter,
                        session=session,
                    )
                )

            return UpdateResult(
                acknowledged=result.acknowledged,
                matched_count=result.matched_count,
                modified_count=result.modified_count,
                document=document,
                upserted_id=(
                    str(result.upserted_id) if result.upserted_id else None
                ),
            )

        except PyMongoError as exc:
            raise UpdateError(f"Failed to upsert document: {exc}") from exc

    # -------------------------------------------------------------------------
    # BULK
    # -------------------------------------------------------------------------
    @classmethod
    async def bulk_write(
            cls,
            operations: list,
            *,
            session: Session = None,
            ordered: bool = True,
    ) -> BulkResult:
        """Execute bulk write operations."""
        try:
            result = await (
                cls.collection().bulk_write(
                    operations,
                    ordered=ordered,
                    session=session,
                )
            )

            return BulkResult(
                acknowledged=result.acknowledged,
                inserted_count=result.inserted_count,
                matched_count=result.matched_count,
                modified_count=result.modified_count,
                deleted_count=result.deleted_count,
                upserted_count=len(result.upserted_ids),
                inserted_ids=[],
                upserted_ids=[str(id_) for id_ in result.upserted_ids.values()]
            )

        except BulkWriteError as ex:
            raise BulkOperationError(str(ex.details)) from ex

        except Exception as ex:
            raise BulkOperationError(
                f"Failed to execute bulk operation: {ex}") from ex

    # -------------------------------------------------------------------------
    # AGGREGATION
    # -------------------------------------------------------------------------
    @classmethod
    async def aggregate(
            cls,
            pipeline: Pipeline,
            *,
            session: Session = None,
    ) -> Documents:
        """Execute aggregation pipeline.
        Args:
            pipeline:
                MongoDB aggregation pipeline.
            session:
                Optional MongoDB session.
        Returns:
            List of aggregation documents.
        Raises:
            AggregateError
        """
        try:
            cursor = cls.collection().aggregate(pipeline, session=session)

            return await cursor.to_list(length=None)

        except PyMongoError as exc:
            raise AggregationError(
                f"Failed to execute aggregation: {exc}") from exc

    @classmethod
    def aggregate_cursor(
            cls,
            pipeline: Pipeline,
            *,
            session: Session = None
    ):
        """Return aggregation cursor."""
        return cls.collection().aggregate(
            pipeline,
            session=session,
        )

    # -------------------------------------------------------------------------
    # INDEXES
    # -------------------------------------------------------------------------
    @classmethod
    async def create_indexes(cls) -> IndexSyncResult:
        """Create repository indexes."""
        try:
            result = IndexSyncResult()

            if not cls.indexes:
                return result

            existing_indexes = {
                index["name"] for index in await cls.list_indexes()
            }

            for index in cls.indexes:
                index_name = str(index.get_index_name())

                if index_name in existing_indexes:
                    result.skipped.append(index_name)
                    continue

                await cls.collection().create_indexes([index.to_index_model()])

                result.created.append(index_name)

            return result

        except PyMongoError as exc:
            raise IndexError(f"Failed to create indexes: {exc}") from exc

    @classmethod
    async def list_indexes(cls) -> Documents:
        """List collection indexes."""
        try:
            cursor = await cls.collection().list_indexes()
            return await cursor.to_list(length=None)

        except PyMongoError as exc:
            raise IndexError(f"Failed to list indexes: {exc}") from exc

    @classmethod
    async def drop_indexes(
            cls,
            *,
            keep_id_index: bool = True,
    ) -> IndexSyncResult:
        """Drop collection indexes."""
        try:
            result = IndexSyncResult()

            indexes = await cls.list_indexes()

            for index in indexes:
                index_name = index["name"]

                if keep_id_index and index_name == "_id_":
                    result.skipped.append(index_name)
                    continue

                await cls.collection().drop_index(index_name)

                result.dropped.append(index_name)

            return result

        except PyMongoError as exc:
            raise IndexError(f"Failed to drop indexes: {exc}") from exc

    @classmethod
    async def sync_indexes(
            cls,
            *,
            drop_obsolete: bool = False,
    ) -> IndexSyncResult:
        """Synchronize repository indexes."""
        try:
            result = IndexSyncResult()

            repository_indexes = {index.get_index_name(): index for index in cls.indexes}

            database_indexes = {
                index["name"]: index for index in await cls.list_indexes()
            }

            # Create missing indexes.
            for index_name, index in repository_indexes.items():
                if index_name in database_indexes:
                    result.skipped.append(index_name)
                    continue

                await cls.collection().create_indexes([index.to_index_model()])

                result.created.append(index_name)

            # Drop obsolete
            if drop_obsolete:
                for index_name, _ in database_indexes.items():
                    if index_name == "_id_":
                        continue

                    if index_name in repository_indexes:
                        continue

                    await cls.collection().drop_index(index_name)

                    result.dropped.append(index_name)

            return result

        except PyMongoError as exc:
            raise IndexError(f"Failed to synchronize indexes: {exc}") from exc


if __name__ == '__main__':
    pass
