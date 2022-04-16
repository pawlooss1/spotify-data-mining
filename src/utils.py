import time
from typing import Callable, Type, TypeVar


R = TypeVar('R')
T = TypeVar('T')


def retry(times: int, exceptions: Type[Exception]) -> Callable:

    def decorator(func: Callable[[R], T]) -> Callable[[R], T]:

        def inner(*args, **kwargs) -> T:
            attempt = 0
            while attempt < times:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    print(f"Exception thrown when attempting to run {func.__name__}, attempt {attempt} of {times}")
                    attempt += 1
                    time.sleep(3)
            return func(*args, **kwargs)

        return inner

    return decorator
