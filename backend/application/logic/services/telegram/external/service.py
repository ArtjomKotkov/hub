from typing import Optional, Any
import requests

from .requests import (
    TelegramApproveRequest,
    TelegramGetUserDataRequest, TelegramMessageRequest,
)
from .responses import (
    TelegramGetUserDataResponse,
)

from ..shared import TelegramInlineKeyboard, TelegramCallbackIKButton
from ..webhook import ButtonActionApproveSession


__all__ = [
    'TelegramExternalService',
]


class TelegramExternalService:
    _api_url = 'https://api.telegram.org/bot'
    _webhook_updates = [
        'message',
        'callback_query',
    ]

    def __init__(
        self,
        bot_token: str,
        callback_url: str,
        webhook_secret: str,
        ip_address: Optional[str] = None,
    ) -> None:
        self._bot_token = bot_token
        self._callback_url = callback_url
        self._webhook_secret = webhook_secret
        self._ip_address = ip_address

    def get_user_data(self, request: TelegramGetUserDataRequest) -> TelegramGetUserDataResponse:
        return TelegramGetUserDataResponse(name='test')

    def set_webhook(self) -> None:
        data = {
            'url': self._callback_url,
            'allowed_updates': self._webhook_updates,
            'secret_token': self._webhook_secret,
        }

        if self._ip_address:
            data['ip_address'] = self._ip_address

        self._make_request(
            method='setWebhook',
            data=data
        )

    def drop_webhook(self) -> None:
        self._make_request(method='deleteWebhook')

    def send_message(self, message: TelegramMessageRequest) -> None:
        data = message.dict(exclude_none=True)

        self._make_request(method='sendMessage', data=data)

    def _make_request(self, method: str, data: Optional[dict[str, Any]] = None) -> Any:
        url = self._get_url(method)

        return requests.post(url=url, json=data)

    def _get_url(self, method: str) -> str:
        return f'{self._api_url}{self._bot_token}/{method}'
