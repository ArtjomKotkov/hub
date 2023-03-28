from fastapi import FastAPI

from .auth import auth_router


app_external = FastAPI()
app_external.include_router(auth_router)

