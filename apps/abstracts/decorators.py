# Python
import time
from typing import (
    Any,
    Callable
)


def performance_counter(func: Callable) -> Callable:
    def wrapper(*args: Any, **kwargs: Any) -> Callable:
        start: float = time.perf_counter()
        result: Callable = func(*args, **kwargs)
        end: float = time.perf_counter()
        print(f'{func.__name__}: {(end-start):.2f} seconds')
        return result
    return wrapper
