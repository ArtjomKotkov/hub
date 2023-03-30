from datetime import datetime

from pydantic import BaseModel

from modeller import SModel


class AuthToken(SModel):
    id: int
    token: str
    expires_in: datetime


class RefreshToken(SModel):
    id: int
    refresh_token: str
    auth_token: str
    expires_in: datetime


class BaseTokenPayload(BaseModel):
    class Config:
        json_encoders = {
            datetime: lambda v: v.timestamp(),
        }


class AuthTokenPayload(BaseTokenPayload):
    expires_in: datetime
    id: int
    role: str


class RefreshTokenPayload(BaseTokenPayload):
    expires_in: datetime
