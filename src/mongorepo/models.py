"""
Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
```
https://www.apache.org/licenses/LICENSE-2.0
```
File: models.py
Description:
    Base models used throughout mongorepo.
"""

# All Python Built-in Imports Here.
from __future__ import annotations
from datetime import datetime

# All Custom Imports Here.
from pydantic import Field, BaseModel, ConfigDict

# All Native Imports Here.
from mongorepo.helpers import get_utc_now
from mongorepo.data_types import PyObjectId


# All Attributes or Constants Here.


class MongoModel(BaseModel):
    """Base MongoDB document model."""
    id: PyObjectId = Field(
        default_factory=PyObjectId,
        alias='_id',
        description='MongoDB Document id.'
    )

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        extra="forbid",
    )


class TimestampedMongoModel(MongoModel):
    """MongoDB model with timestamps."""
    created_at: datetime | None = Field(
        default_factory=get_utc_now,
        description='Timestamp of creation')

    updated_at: datetime | None = Field(
        default=None,
        description='Timestamp of last update')


if __name__ == '__main__':
    pass
