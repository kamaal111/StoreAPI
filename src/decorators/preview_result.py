import json
import functools
from returns.result import Success


def preview_result(path: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            is_preview: bool = kwargs.get("preview")  # type: ignore
            if not is_preview:
                return func(*args, **kwargs)

            with open(path, "r") as file:
                return Success(json.loads(file.read()))

        return wrapper

    return decorator
