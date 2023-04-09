from fastapi import APIRouter, Depends, Response
from dependency_injector.wiring import Provide, inject

from backend.settings import Settings
from backend.logic import AuthResponse, AuthRequest, AuthService, Logic


auth_router = APIRouter()


@auth_router.post('')
@inject
def auth(
    response: Response,
    data: AuthRequest,
    auth_service: AuthService = Depends(Provide[Logic.services.auth_service]),
) -> AuthResponse:
    service_response = auth_service.auth(data)

    response.set_cookie(Settings.AUTH_TOKEN_COOKIE_NAME, service_response.auth_token)
    response.set_cookie(Settings.REFRESH_TOKEN_COOKIE_NAME, service_response.refresh_token)

    return service_response
