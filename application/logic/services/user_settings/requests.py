from typing import Optional

from pydantic import BaseModel


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


class GetUserSettingsRequest(BaseModel):
    id: int


class UpdateUserSettingsRequest(BaseModel):
    id: int
    fields: UserSettingsFields
