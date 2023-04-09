from typing import Optional

from pydantic import BaseModel

from ..shared import RequestorRequest


__all__ = [
    'UserSettingsFields',
    'GetUserSettingsRequest',
    'UpdateUserSettingsRequest',
]


class UserSettingsFields(BaseModel):
    calories_limit: Optional[int]
    height: Optional[int]
    weight: Optional[int]
    age: Optional[int]


class GetUserSettingsRequest(RequestorRequest):
    id: int


class UpdateUserSettingsRequest(RequestorRequest):
    id: int
    fields: UserSettingsFields
