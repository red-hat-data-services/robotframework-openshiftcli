from functools import wraps
from typing import Callable


def deprecated(new_keyword: str) -> Callable:
    def inner(func) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs) -> Callable:
            message = f"This keyword is deprecated, please use {new_keyword} keyword instead"
            self.output_streamer.stream(message, 'warn')
            func(self, *args, **kwargs)
        return wrapper
    return inner
