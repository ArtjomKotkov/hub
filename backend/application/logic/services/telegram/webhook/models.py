from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Extra, Field


__all__ = [
    'TelegramUpdate',
    'TelegramUser',
    'TelegramMessage',
    'TelegramChat',
    'TelegramChatType',
    'TelegramChatMemberUpdated',
    'TelegramCallbackQuery',
]


class TelegramUser(BaseModel, extra=Extra.ignore):
    id: int
    first_name: str
    last_name: Optional[str]
    username: str


class TelegramMessage(BaseModel, extra=Extra.ignore):
    message_id: int
    from_: TelegramUser = Field(alias='from')
    date: datetime
    text: str


class TelegramChatType(str, Enum):
    private = 'private'
    group = 'group'
    supergroup = 'supergroup'
    channel = 'channel'


class TelegramChat(BaseModel, extra=Extra.ignore):
    id: int
    type: list[TelegramChatType]


class TelegramChatMemberUpdated(BaseModel, extra=Extra.ignore):
    chat: TelegramChat
    from_: TelegramUser = Field(alias='from')
    date: datetime


class TelegramCallbackQuery(BaseModel, extra=Extra.ignore):
    id: str
    from_: TelegramUser = Field(alias='from')
    message: Optional[TelegramMessage]
    data: str


class TelegramUpdate(BaseModel, extra=Extra.ignore):
    update_id: int
    message: Optional[TelegramMessage]
    chat_member: Optional[TelegramChatMemberUpdated]
    callback_query: Optional[TelegramCallbackQuery]
