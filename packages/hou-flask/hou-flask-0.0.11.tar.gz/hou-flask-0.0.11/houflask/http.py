import dataclasses
from functools import wraps
from typing import Dict, Iterable, Union, Callable
from uuid import UUID

import rapidjson
from flask import Response


def json_response(data: Union[Dict, Iterable], status=200):
    return Response(rapidjson.dumps(data), status, content_type="application/json")


def empty_response():
    return Response(status=204)


def dataclass_json_response(data, status: int = 200):
    """
    Turns a list or single instance of dataclasses into a json response
    """
    try:
        return json_response(dataclasses.asdict(data), status)
    except TypeError:
        return json_response((dataclasses.asdict(item) for item in data), status)


def uuid_converter(key_words: Iterable[str]) -> Callable:
    def _uuid_converter_decorator(func: Callable) -> Callable:
        @wraps(func)
        def _uuid_converter_wrapper(*args, **kwargs):
            for key_word in key_words:
                if key_word in kwargs:
                    kwargs[key_word] = UUID(kwargs[key_word])
            return func(*args, **kwargs)

        return _uuid_converter_wrapper

    return _uuid_converter_decorator
