from application.logic.repositories import Repository

from .base import ActionHandler
from .exceptions import UnknownAction

from ...models import TelegramCallbackQuery
from ....shared import ButtonAction


__all__ = [
    'ActionProcessor',
]


class ActionProcessor:
    def __init__(
        self,
    ):

        self._handlers: list[ActionHandler] = []
        self._register_action_handlers()

    def _register_action_handlers(self) -> None:
        self._handlers: list[ActionHandler] = [
        ]

    def _action_to_handler(self) -> dict[ButtonAction, ActionHandler]:
        return {handler.action: handler for handler in self._handlers}

    def process(self, update: TelegramCallbackQuery) -> None:
        handlers_map = self._action_to_handler()

        for action, handler in handlers_map.items():
            if action.test(update.data):
                handler.execute(update)
                return
        else:
            raise UnknownAction()

