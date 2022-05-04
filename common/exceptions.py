from rest_framework.views import exception_handler

from common.response import ResponseInstance


def custom_exception_handler(exception, context):
    exception_response = exception_handler(exception, context)

    error_code = ""

    status_code = exception_response.status_code

    if status_code == 400:
        error_code = 1304
    if status_code == 401:
        error_code = 1102
    if status_code == 403:
        error_code = 1101
    if status_code == 404:
        error_code = 1103

    return ResponseInstance.api_response(
        has_error=True,
        status_code=status_code,
        message=exception_response.data["detail"],
        error_code=error_code,
    )
