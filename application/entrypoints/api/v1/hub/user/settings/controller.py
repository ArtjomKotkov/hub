from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from application.logic import (
    Logic, UserSettingsService,
    GetUserSettingsRequest, GetUserSettingsResponse,
    UpdateUserSettingsRequest, UpdateUserSettingsResponse,
    UserSettingsFields,
)


user_settings_router = APIRouter()


@user_settings_router.get('/{user_id}')
@inject
def get(
    user_id: int,
    user_settings_service: UserSettingsService = Depends(Provide[Logic.services.user_settings]),
) -> GetUserSettingsResponse:
    response = user_settings_service.get(GetUserSettingsRequest(id=user_id))

    return response


@user_settings_router.post('/{user_id}')
@inject
def get(
    user_id: int,
    data: UserSettingsFields,
    user_settings_service: UserSettingsService = Depends(Provide[Logic.services.user_settings]),
) -> UpdateUserSettingsResponse:
    response = user_settings_service.update(UpdateUserSettingsRequest(id=user_id, fields=data))

    return response
