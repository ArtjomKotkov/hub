from pydantic import BaseModel


__all__ = [
    'GlobalSettingsFields',
    'GlobalSettingsResponse',
]


class GlobalSettingsFields(BaseModel):
    refresh_token_cookie_name: str
    auth_token_cookie_name: str
    auth_token_expires_in: int
    refresh_token_expires_in: int


class GlobalSettingsResponse(BaseModel):
    entity: GlobalSettingsFields
