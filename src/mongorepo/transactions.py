"""
Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
```
https://www.apache.org/licenses/LICENSE-2.0
```
File: transactions.py
Description:

"""

# All Python Built-in Imports Here.
from __future__ import annotations

# All Custom Imports Here.
from pymongo.asynchronous.client_session import AsyncClientSession

# All Native Imports Here.
from mongorepo.database import Database
from mongorepo.errors.database import DatabaseTransactionError


# All Attributes or Constants Here.


class Transaction:
    """MongoDB transaction context manager.
    Example:
        async with Transaction() as session:

            await UserRepository.create(
                user,
                session=session
            )
    """

    def __init__(self):
        self._session: AsyncClientSession | None = None

    @property
    def session(self) -> AsyncClientSession:
        """Return MongoDB session."""
        if self._session is None:
            raise RuntimeError("Transaction not started.")

        return self._session

    async def __aenter__(self) -> AsyncClientSession:
        """Start transaction."""
        try:

            self._session = Database.get_client().start_session()

            await self._session.start_transaction()

            return self._session

        except Exception as exc:

            raise DatabaseTransactionError(
                f"Failed to start transaction: {exc}") from exc

    async def __aexit__(self, exc_type, exc, tb) -> bool:
        """Commit or rollback transaction."""
        try:
            if self._session is None:
                return False

            if exc is None:
                await self._session.commit_transaction()

            else:
                await self._session.abort_transaction()

        except Exception as transaction_exc:
            raise DatabaseTransactionError(
                f"Transaction failed: {transaction_exc}"
            ) from transaction_exc

        finally:

            if self._session is not None:
                await self._session.end_session()

        return False


if __name__ == '__main__':
    pass
