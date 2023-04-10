# Python
from typing import Any
from datetime import (
    datetime,
    timedelta
)


def get_eta_time(seconds: int) -> Any:
    return datetime.utcnow() + timedelta(seconds=seconds)


def cache_for(
    seconds: int = 0,
    minutes: int = 0,
    hours: int = 0
) -> int:
    if (not isinstance(seconds, int)) or \
       (not isinstance(minutes, int)) or \
       (not isinstance(hours, int)):
        raise ValueError("Not is number.")
    if (seconds < 0) or (minutes < 0) or (hours < 0):
        raise ValueError("Invalid number.")
    return (seconds + 1) * (minutes + 1) * (hours + 1)
