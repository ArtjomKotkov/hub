from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from application.logic import (
    Logic, UserService,
    GetUserRequest, GetUserResponse,
    ListUserRequest, ListUserResponse,
    DeleteUserRequest, DeleteUserResponse,
    UpdateUserRequest, UpdateUserResponse,
    UserUpdateFields,
)


user_router = APIRouter()


@user_router.get('/{user_id}')
@inject
def get(
    user_id: int,
    user_service: UserService = Depends(Provide[Logic.services.user]),
) -> GetUserResponse:
    response = user_service.get(GetUserRequest(id=user_id))

    return response


@user_router.get('/')
@inject
def list(
    user_service: UserService = Depends(Provide[Logic.services.user]),
) -> ListUserResponse:
    response = user_service.list(ListUserRequest())

    return response


@user_router.delete('/{user_id}')
@inject
def list(
    user_id: int,
    user_service: UserService = Depends(Provide[Logic.services.user]),
) -> DeleteUserResponse:
    response = user_service.delete(DeleteUserRequest(id=user_id))

    return response


@user_router.post('/{user_id}')
@inject
def update(
    user_id: int,
    data: UserUpdateFields,
    user_service: UserService = Depends(Provide[Logic.services.user]),
) -> UpdateUserResponse:
    response = user_service.update(UpdateUserRequest(id=user_id, fields=data))

    return response
