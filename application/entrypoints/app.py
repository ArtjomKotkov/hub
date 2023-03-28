from fastapi import FastAPI
from fastapi.responses import JSONResponse

from pydantic import BaseConfig

from errors import Error

from .api import app_api


app_entrypoints = FastAPI()
BaseConfig.arbitrary_types_allowed = True

app_entrypoints.mount('/api', app_api)


@app_entrypoints.exception_handler(Error)
def errors_handler(exception: Error):
    return JSONResponse(
        status_code=exception.code,
        content={"message": exception.description},
    )
