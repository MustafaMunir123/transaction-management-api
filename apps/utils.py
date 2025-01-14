# Standard Library Imports
from typing import Any

# Third Party Imports
from django.core.cache import cache
from django.core.exceptions import FieldError, ObjectDoesNotExist
from django.db import IntegrityError, OperationalError
from rest_framework import status
from rest_framework.views import Response, exception_handler


def success_response(status, data, success=True):
    Response.status_code = status
    msg = {"success": success, "data": data}
    return Response(msg)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    print(exc)
    if response is not None:
        response.data = error_response(str(exc))
        return response.data
    elif (
        isinstance(exc, FieldError)
        or isinstance(exc, AttributeError)
        or isinstance(exc, TypeError)
        or isinstance(exc, AssertionError)
        or isinstance(exc, OperationalError)
    ):
        response = error_response(str(exc))
    elif isinstance(exc, IntegrityError):
        response = error_response(str(exc).strip("\n").split("DETAIL:  ")[-1])
    elif isinstance(exc, ValueError) or isinstance(exc, ObjectDoesNotExist):
        response = error_response(str(exc))
    elif isinstance(exc, KeyError):
        response = error_response("Invalid Parameters")
    else:
        response = response

    return response


def error_response(error_msg):
    return Response(
        {"success": False, "error": error_msg},
        status=status.HTTP_400_BAD_REQUEST,
    )


class CacheUtils:
    @staticmethod
    def set_cache(cache_key, data) -> None:
        cache.set(cache_key, data, 600)

    @staticmethod
    def get_cache(cache_key) -> Any:
        cached_data = cache.get(cache_key)
        return cached_data

    @staticmethod
    def delete_cache():
        cache.clear()
