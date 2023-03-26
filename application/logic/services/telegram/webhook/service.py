from typing import Any

from .requests import TelegramUpdateRequest
from .models import TelegramMessage, TelegramCallbackQuery
from .processors import CommandProcessor, ActionProcessor

from application.logic.repositories import Repository


__all__ = [
    'TelegramWebhookService',
]


class TelegramWebhookService:
    def __init__(
        self,
    ):
        self._command_processor = CommandProcessor()

        self._action_processor = ActionProcessor()

    def process_update(self, request: TelegramUpdateRequest) -> Any:
        if request.message:
            self._process_message(request.message)

        elif request.callback_query:
            self._process_callback_query(request.callback_query)

    def _process_message(self, update: TelegramMessage) -> None:
        if update.text.startswith(r'/'):
            self._process_command(update)

    def _process_command(self, update: TelegramMessage) -> None:
        self._command_processor.process(update)

    def _process_callback_query(self, update: TelegramCallbackQuery) -> None:
        self._action_processor.process(update)
