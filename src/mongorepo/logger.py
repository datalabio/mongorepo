"""
Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
```
https://www.apache.org/licenses/LICENSE-2.0
```
File: logging
Description:
    Logging utilities for mongorepo.
    This package intentionally does not configure logging.
    Applications using mongorepo are responsible for configuring
    logging handlers, formatters, and levels.
"""

# All Python Built-in Imports Here.
from __future__ import annotations
import logging

# All Custom Imports Here.

# All Native Imports Here.

# All Attributes or Constants Here.
LOGGER_NAME = "mongorepo"


def get_logger(name: str | None = None) -> logging.Logger:
    """
    Return a logger instance.
    Examples:
        logger = get_logger()

        logger = get_logger("database")

        logger = get_logger("repository.user")
    """
    if not name:
        return logging.getLogger(LOGGER_NAME)

    return logging.getLogger(f"{LOGGER_NAME}.{name}")


if __name__ == '__main__':
    pass
