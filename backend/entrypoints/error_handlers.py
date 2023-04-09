from fastapi import Request
from fastapi.responses import JSONResponse

from errors import Error


__all__ = [
    'errors_handler',
]


def errors_handler(_: Request, exception: Error):
    return JSONResponse(
        status_code=exception.code,
        content={'code': exception.description},
    )
