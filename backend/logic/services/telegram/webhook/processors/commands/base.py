from ...models import TelegramMessage


__all__ = [
    'Command',
]


class Command:
    code: str

    def execute(self, update: TelegramMessage) -> None: ...
