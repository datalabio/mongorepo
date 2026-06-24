"""
Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
```
https://www.apache.org/licenses/LICENSE-2.0
```
File: test_database
Description:

"""

# All Python Built-in Imports Here.
import asyncio

# All Custom Imports Here.

# All Native Imports Here.
from mongorepo.database import Database


# All Attributes or Constants Here.

async def try_connection(uri, database_name):
    await Database.connect(uri=uri, database_name=database_name)
    collection = Database.get_collection('beta_users')

    for x in await collection.find(limit=10).to_list(None):
        print(x)


if __name__ == '__main__':
    _db_uri = ""
    _db_name = ""
    asyncio.run(try_connection(_db_uri, _db_name))
