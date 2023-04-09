from pydantic import BaseModel

from ...models import UserSettings


__all__ = [
    'GetUserSettingsResponse',
    'UpdateUserSettingsResponse',
]


class GetUserSettingsResponse(BaseModel):
    entity: UserSettings


class UpdateUserSettingsResponse(BaseModel):
    entity: UserSettings
