from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from application.logic import AuthResponse, AuthRequest, AuthService, Logic


auth_router = APIRouter()


@auth_router.post('/auth')
@inject
def auth(
    data: AuthRequest,
    auth_service: AuthService = Depends(Provide[Logic.services.auth_service]),
) -> AuthResponse:
    response = auth_service.auth(data)

    return response
