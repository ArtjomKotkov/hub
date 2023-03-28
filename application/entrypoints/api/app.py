from fastapi import FastAPI

from .v1 import app_v1


app_api = FastAPI()
app_api.mount('/v1', app_v1)
