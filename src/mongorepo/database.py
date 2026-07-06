"""
Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
```
https://www.apache.org/licenses/LICENSE-2.0
```
File: database
Description:
 MongoDB connection management for mongorepo.
"""

# All Python Built-in Imports Here.
from __future__ import annotations
from typing import ClassVar

# All Custom Imports Here.
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.client_session import AsyncClientSession

# All Native Imports Here.
from mongorepo import get_logger
from mongorepo.errors.database import *

# All Attributes or Constants Here.
logger = get_logger()


class Database:
    """Global MongoDB connection manager."""
    _client: ClassVar[AsyncMongoClient | None] = None
    _database: ClassVar[AsyncDatabase | None] = None

    _uri: ClassVar[str | None] = None
    _database_name: ClassVar[str | None] = None

    @classmethod
    async def connect(
            cls,
            *,
            uri: str,
            database_name: str,
            **kwargs,
    ) -> None:
        """Create a MongoDB connection.
        Args:
            uri: MongoDB connection URI.
            database_name: Database name.
            **kwargs: Additional AsyncMongoClient options.

        Raises:
            ConfigurationError
            DatabaseConnectionError
        """
        if not uri:
            raise DatabaseConfigurationError(
                "MongoDB URI is required."
            )

        if not database_name:
            raise DatabaseConfigurationError(
                "Database name is required."
            )

        try:
            client = AsyncMongoClient(
                uri,
                **kwargs,
            )

            await client.admin.command({"ping": 1})

            cls._client = client
            cls._database = client[database_name]

            cls._uri = uri
            cls._database_name = database_name

            logger.info(
                f"Connected to MongoDB database '{database_name}'."
            )

        except Exception as exc:
            raise DatabaseConnectionError(
                f"Failed to connect to MongoDB: {exc}"
            ) from exc

    @classmethod
    async def disconnect(cls) -> None:
        """Close the MongoDB connection."""
        try:
            if cls._client:
                await cls._client.close()

            cls._client = None
            cls._database = None

            logger.info(
                "Disconnected from MongoDB."
            )

        except Exception as exc:
            raise DatabaseDisconnectionError(
                f"Failed to disconnect from MongoDB: {exc}"
            ) from exc

    @classmethod
    def get_client(cls) -> AsyncMongoClient:
        """Return active MongoDB client.

        Raises:
            DatabaseConnectionError
        """
        if cls._client is None:
            raise DatabaseConnectionError(
                "Database connection has not been established."
            )

        return cls._client

    @classmethod
    def get_database(cls) -> AsyncDatabase:
        """Return active database.

        Raises:
            DatabaseConnectionError
        """
        if cls._database is None:
            raise DatabaseConnectionError(
                "Database connection has not been established."
            )

        return cls._database

    @classmethod
    def get_collection(
            cls,
            name: str,
    ) -> AsyncCollection:
        """Return a collection instance.

        Args:
            name: Collection name.

        Raises:
            CollectionError
        """
        try:
            return cls.get_database()[name]

        except Exception as exc:
            raise DatabaseCollectionError(
                f"Failed to access collection '{name}'."
            ) from exc

    @classmethod
    async def is_alive(cls) -> bool:
        """Verify MongoDB availability.

        Returns:
            bool
        """
        try:
            await cls.get_client().admin.command(
                {"ping": 1}
            )

            return True

        except Exception as exc:
            raise DatabaseHealthCheckError(
                f"Database health check failed: {exc}"
            ) from exc

    @classmethod
    async def start_session(cls) -> AsyncClientSession:
        """Start MongoDB session."""
        try:

            return cls.get_client().start_session()

        except Exception as exc:
            raise DatabaseSessionError(
                f"Failed to start "
                f"session: {exc}"
            ) from exc


if __name__ == '__main__':
    pass
