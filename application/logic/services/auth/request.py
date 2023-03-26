from datetime import datetime
from typing import Optional

from pydantic import BaseModel


__all__ = [
    'AuthRequest',
]


class AuthRequest(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str]
    photo_url: Optional[str]
    username: str
    auth_date: int
    hash: str

