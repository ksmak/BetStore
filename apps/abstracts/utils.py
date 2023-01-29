# Python
from typing import Any
from datetime import (
    datetime,
    timedelta
)


def get_eta_time(
        seconds: int = 0, 
        minutes: int = 0,
        hours: int = 0,
        days: int = 0,
        weeks: int = 0,
    ) -> Any:
    
    return datetime.utcnow() + timedelta(
        seconds=seconds,
        minutes=minutes,
        hours=hours,
        days=days,
        weeks=weeks)
