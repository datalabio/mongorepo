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
from typing import Any, ClassVar, Generic, TypeVar, get_args
from pymongo.errors import PyMongoError

from mongorepo.errors.repository import ReadError
from mongorepo.types import Filter, Projection, Sort

# All Custom Imports Here.
from bson import ObjectId
from bson.errors import InvalidId
from pydantic import BaseModel
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.client_session import AsyncClientSession
from pymongo.errors import DuplicateKeyError, PyMongoError

# All Native Imports Here.
from mongorepo import get_logger
from mongorepo.database import Database
from mongorepo.enums import ReturnDocument
from mongorepo.errors.repository import DuplicateDocumentError, CreateError
from mongorepo.indexes import BaseIndex
from mongorepo.exceptions import ConfigurationError

from mongorepo.types import Projection

# All Attributes or Constants Here.
logger = get_logger("repository")
T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T]):
    """
    Generic MongoDB repository.

    Example:

        class UserRepository(
            BaseRepository[UserModel]
        ):

            collection_name = "users"
    """

    model: ClassVar[type[T]]

    # Must be overridden by child repositories
    collection_name: ClassVar[str]

    # Optional index definitions
    indexes: ClassVar[list[BaseIndex]] = []

    def __init_subclass__(cls, **kwargs):
        """
        Discover model from Generic[T].
        """
        super().__init_subclass__(**kwargs)

        # Validate collection name
        if (
                cls.__name__ != "BaseRepository"
                and not getattr(cls, "collection_name", None)
        ):
            raise ConfigurationError(
                f"{cls.__name__} must define "
                f"'collection_name'."
            )

        # Discover model from Generic[T]
        if hasattr(cls, "__orig_bases__"):
            for base in cls.__orig_bases__:

                args = get_args(base)

                if args:
                    cls.model = args[0]
                    break

        # Validate model
        if (
                cls.__name__ != "BaseRepository"
                and not hasattr(cls, "model")
        ):
            raise ConfigurationError(
                f"Unable to discover model "
                f"for repository "
                f"{cls.__name__}."
            )

    # =========================================================================
    # Database Helpers
    # =========================================================================
    @classmethod
    def collection(cls) -> AsyncCollection:
        """
        Return MongoDB collection.
        """
        return Database.get_collection(cls.collection_name)

    # =========================================================================
    # Serialization Helpers
    # =========================================================================

    @classmethod
    def to_model(cls, document: dict | None) -> T | None:
        """
        Convert MongoDB document
        to Pydantic model.
        """
        if document is None:
            return None

        return cls.model.from_mongo(
            document
        )

    @classmethod
    def to_models(cls, documents: list[dict]) -> list[T]:
        """
        Convert list of MongoDB
        documents to models.
        """
        return [
            cls.model.from_mongo(
                document,
            )
            for document in documents
        ]

    @staticmethod
    def to_document(model: MongoModel) -> dict:
        """
        Convert model to MongoDB
        document.
        """
        return model.to_mongo()

    @staticmethod
    def to_documents(models: list[MongoModel]) -> list[dict]:
        """
        Convert model list to
        MongoDB documents.
        """
        return [
            model.to_mongo()
            for model in models
        ]

    # =========================================================================
    # Generic Normalizer Helpers
    # =========================================================================

    @staticmethod
    def normalize_projection(
            projection: Projection,
    ) -> dict[str, int] | None:
        """Normalize projection.
        Supports:
            ["name", "email"]
        and:
            {"name": 1, "email": 1}
        """
        if projection is None:
            return None

        if isinstance(
                projection,
                dict,
        ):
            return projection

        return {
            field: 1
            for field in projection
        }

    @staticmethod
    def normalize_update(update: dict | None = None, **kwargs) -> dict:
        """Normalize update expression.
        Supports:
            {"$set": {...}}
        and:
            field1=value1,
            field2=value2
        """
        if update is not None:
            # Raw MongoDB operator
            if any(
                    key.startswith("$")
                    for key in update
            ):
                return update

            # Plain dictionary
            return {
                "$set": update,
            }

        # Keyword arguments
        return {"$set": kwargs}

    # =========================================================================
    # ObjectId Helpers
    # =========================================================================
    @staticmethod
    def object_id(value: str) -> ObjectId:
        """
        Convert string to ObjectId.
        """
        try:
            return ObjectId(
                value,
            )

        except InvalidId as exc:
            raise ValueError(
                f"Invalid ObjectId: "
                f"{value}"
            ) from exc

    @staticmethod
    def object_ids(values: list[str]) -> list[ObjectId]:
        """
        Convert list of strings
        to ObjectIds.
        """
        return [
            BaseRepository.object_id(
                value,
            )
            for value in values
        ]

    # ==========================================================
    # Session Helpers
    # ==========================================================
    @staticmethod
    def normalize_session(
            session: AsyncClientSession | None
    ) -> (AsyncClientSession | None):
        """
        Normalize session object.
        """
        return session

    # =========================================================================
    # CREATE
    # =========================================================================
    @classmethod
    async def create(
            cls,
            document: T,
            *,
            session: AsyncClientSession | None = None,
            return_document: ReturnDocument = ReturnDocument.MODEL,
    ) -> T | str | None:
        """
        Create a document.

        Args:
            document:
                Document to create.

            session:
                Optional MongoDB session.

            return_document:
                Return Document model

        Returns:
            Created model.

        Raises:
            CreateError
            DuplicateDocumentError
        """
        try:

            mongo_document = cls.to_document(document)

            result = await cls.collection().insert_one(
                mongo_document,
                session=session,
            )

            inserted_id = str(result.inserted_id)

            if return_document == ReturnDocument.NONE:
                return None

            if return_document == ReturnDocument.ID:
                return inserted_id

            document.id = inserted_id

            return document

        except DuplicateKeyError as exc:

            raise DuplicateDocumentError(
                cls.collection_name,
            ) from exc

        except PyMongoError as exc:

            raise CreateError(
                f"Failed to create "
                f"document: {exc}"
            ) from exc

    @classmethod
    async def create_many(
            cls,
            documents: list[T],
            *,
            session: AsyncClientSession | None = None,
            ordered: bool = True,
            return_document: ReturnDocument = ReturnDocument.MODEL,
    ) -> list[T] | None:
        """
        Create multiple documents.

        Args:
            documents:
                Documents to create.

            session:
                Optional MongoDB session.

            ordered:
                MongoDB ordered insert mode.

            return_document:
                return document.

        Returns:
            Created models.

        Raises:
            CreateError
            DuplicateDocumentError
        """
        try:

            mongo_documents = [
                cls.to_document(
                    document,
                )
                for document in documents
            ]

            result = await (
                cls.collection().insert_many(
                    mongo_documents,
                    ordered=ordered,
                    session=session,
                )
            )

            ids = [str(id_) for id_ in result.inserted_ids]

            if return_document == ReturnDocument.NONE:
                return None

            if return_document == ReturnDocument.ID:
                return ids

            for document, id_ in zip(documents, ids, strict=True):
                document.id = id_

            return documents

        except DuplicateKeyError as exc:

            raise DuplicateDocumentError(
                cls.collection_name,
            ) from exc

        except PyMongoError as exc:

            raise CreateError(
                f"Failed to create "
                f"documents: {exc}"
            ) from exc

    # =========================================================================
    # Read
    # =========================================================================

    @classmethod
    async def find_by_id(
        cls,
        id_: str,
        *,
        projection: Projection = None,
        session: AsyncClientSession | None = None,
    ) -> T | None:
        """Find document by id."""
        try:

            document = await (
                cls.collection().find_one(
                    {
                        "_id": cls.object_id(
                            id_,
                        )
                    },
                    projection=cls.normalize_projection(
                        projection,
                    ),
                    session=session,
                )
            )

            return cls.to_model(
                document,
            )

        except PyMongoError as exc:

            raise ReadError(
                f"Failed to find "
                f"document by id: {exc}"
            ) from exc

    @classmethod
    async def find_one(
        cls,
        document_filter: Filter,
        *,
        projection: Projection = None,
        sort: Sort = None,
        session: AsyncClientSession | None = None,
    ) -> T | None:
        """
        Find a single document.
        """
        try:

            document = await (
                cls.collection().find_one(
                    document_filter,
                    projection=cls.normalize_projection(
                        projection,
                    ),
                    sort=sort,
                    session=session,
                )
            )

            return cls.to_model(
                document,
            )

        except PyMongoError as exc:

            raise ReadError(
                f"Failed to find "
                f"document: {exc}"
            ) from exc

    @classmethod
    async def find(
        cls,
        document_filter: Filter | None = None,
        *,
        projection: Projection = None,
        sort: Sort = None,
        skip: int = 0,
        limit: int | None = None,
        session: AsyncClientSession | None = None,
    ) -> list[T]:
        """
        Find multiple documents.
        """
        try:

            cursor = cls.collection().find(
                document_filter or {},
                projection=cls.normalize_projection(
                    projection,
                ),
                sort=sort,
                skip=skip,
                session=session,
            )

            if limit:
                cursor = cursor.limit(
                    limit,
                )

            documents = await cursor.to_list(
                length=None,
            )

            return cls.to_models(
                documents,
            )

        except PyMongoError as exc:

            raise ReadError(
                f"Failed to find "
                f"documents: {exc}"
            ) from exc

    @classmethod
    async def exists(
        cls,
        document_filter: Filter,
        *,
        session: AsyncClientSession | None = None,
    ) -> bool:
        """
        Check if document exists.
        """
        try:

            document = await (
                cls.collection().find_one(
                    document_filter,
                    projection={
                        "_id": 1,
                    },
                    session=session,
                )
            )

            return document is not None

        except PyMongoError as exc:

            raise ReadError(
                f"Failed to check "
                f"document existence: {exc}"
            ) from exc

    @classmethod
    async def count(
        cls,
        document_filter: Filter | None = None,
        *,
        session: AsyncClientSession | None = None,
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

    # ==========================================================
    # UPDATE
    # ==========================================================

    @classmethod
    async def update(
        cls,
        id_: str,
        update: Update | None = None,
        *,
        session: AsyncClientSession | None = None,
        return_document: ReturnDocument = (
            ReturnDocument.MODEL
        ),
        **kwargs,
    ) -> T | str | None:
        """
        Update document by id.
        """
        return await cls.update_one(
            {
                "_id": cls.object_id(
                    id_,
                )
            },
            update,
            session=session,
            return_document=return_document,
            **kwargs,
        )

    @classmethod
    async def update_one(
        cls,
        filter: Filter,
        update: Update | None = None,
        *,
        session: AsyncClientSession | None = None,
        return_document: ReturnDocument = (
            ReturnDocument.MODEL
        ),
        **kwargs,
    ) -> T | str | None:
        """
        Update a single document.
        """
        try:

            normalized_update = (
                cls.normalize_update(
                    update,
                    **kwargs,
                )
            )

            result = await (
                cls.collection().update_one(
                    filter,
                    normalized_update,
                    session=session,
                )
            )

            if result.matched_count == 0:

                raise DocumentNotFoundError(
                    cls.collection_name,
                )

            if (
                return_document
                == ReturnDocument.NONE
            ):
                return None

            document = await (
                cls.collection().find_one(
                    filter,
                    session=session,
                )
            )

            if document is None:

                raise DocumentNotFoundError(
                    cls.collection_name,
                )

            if (
                return_document
                == ReturnDocument.ID
            ):
                return str(
                    document["_id"]
                )

            return cls.to_model(
                document,
            )

        except DocumentNotFoundError:

            raise

        except PyMongoError as exc:

            raise UpdateError(
                f"Failed to update "
                f"document: {exc}"
            ) from exc
    @classmethod
    async def update_many(
        cls,
        filter: Filter,
        update: Update | None = None,
        *,
        session: AsyncClientSession | None = None,
        return_document: ReturnDocument = (
            ReturnDocument.NONE
        ),
        **kwargs,
    ):
        """
        Update multiple documents.
        """

if __name__ == '__main__':
    pass
