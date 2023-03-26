from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from dependency_injector.wiring import Provide, inject

from .telegram import telegram_app
from application.logic import AuthService, AuthRequest, Logic, AuthResponse

entrypoints = FastAPI()

entrypoints.mount('/telegram', telegram_app)

origins = [
    "http://akotasadgsdg.com",
]

entrypoints.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@entrypoints.post('/auth', response_model=AuthResponse)
@inject
def test(request: AuthRequest, auth_service: AuthService = Depends(Provide[Logic.services.auth_service])):
    return auth_service.auth(request)
