from datetime import datetime
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
