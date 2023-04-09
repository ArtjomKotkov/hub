from ...models import TelegramCallbackQuery

from ....shared import ButtonAction


__all__ = [
    'ActionHandler',
]


class ActionHandler:
    action: ButtonAction

    def execute(self, update: TelegramCallbackQuery) -> None: ...
