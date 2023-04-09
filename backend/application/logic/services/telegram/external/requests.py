from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel
from pydantic.types import UUID4

from ..shared import TelegramInlineKeyboard


__all__ = [
    'TelegramApproveRequest',
    'TelegramGetUserDataRequest',
    'TelegramMessageRequest',
]


class TelegramApproveRequest(BaseModel):
    session_guid: UUID4


class TelegramGetUserDataRequest(BaseModel):
    phone: int


class TelegramMessageRequest(BaseModel):
    chat_id: int | str
    text: str
    reply_markup: Optional[TelegramInlineKeyboard]
