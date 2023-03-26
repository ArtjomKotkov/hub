from pydantic import BaseModel


__all__ = [
    'CreateTokensResponse',
    'RefreshTokenResponse',
]


class CreateTokensResponse(BaseModel):
    auth_token: str
    refresh_token: str


class RefreshTokenResponse(CreateTokensResponse): ...
