from pydantic import BaseModel


__all__ = [
    'CreateTokensRequest',
    'DeleteTokensRequest',
    'RefreshTokenRequest',
]


class CreateTokensRequest(BaseModel):
    id: int


class DeleteTokensRequest(BaseModel):
    auth_token: str


class RefreshTokenRequest(BaseModel):
    auth_token: str
    refresh_token: str
