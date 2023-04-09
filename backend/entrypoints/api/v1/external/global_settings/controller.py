from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from backend.logic import GlobalSettingsService, GlobalSettingsResponse, Logic


global_settings_router = APIRouter()


@global_settings_router.get('')
@inject
def get(
    global_settings: GlobalSettingsService = Depends(Provide[Logic.services.global_settings]),
) -> GlobalSettingsResponse:
    response = global_settings.get()

    return response
