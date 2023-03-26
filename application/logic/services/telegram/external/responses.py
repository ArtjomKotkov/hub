from pydantic import BaseModel, Extra

from ..webhook import TelegramUpdate

__all__ = [
    'TelegramGetUserDataResponse',
    'TelegramGetUpdatesResponse'
]


class TelegramGetUserDataResponse(BaseModel, extra=Extra.ignore):
    name: str
    id: str


class TelegramGetUpdatesResponse(BaseModel, extra=Extra.ignore):
    updates: list[TelegramUpdate]
