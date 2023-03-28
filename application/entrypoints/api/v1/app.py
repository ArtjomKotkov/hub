from fastapi import FastAPI

from .hub import app_hub
from .external import app_external


app_v1 = FastAPI()
app_v1.mount('/hub', app_hub)
app_v1.mount('/', app_external)

