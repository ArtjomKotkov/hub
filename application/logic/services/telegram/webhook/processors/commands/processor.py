from application.logic.repositories import Repository

from .base import Command
from .exceptions import UnknownCommand

from ...models import TelegramMessage


__all__ = [
    'CommandProcessor',
]


class CommandProcessor:
    def __init__(
        self,
    ):
        self._commands: list[Command] = []
        self._register_commands()

    def _register_commands(self) -> None:
        self._commands: list[Command] = [
        ]

    def _get_code_to_command_map(self) -> dict[str, Command]:
        return {command.code: command for command in self._commands}

    def process(self, update: TelegramMessage) -> None:
        handler = self._get_code_to_command_map().get(update.text)
        if handler is None:
            raise UnknownCommand(update.text)

        handler.execute(update)


