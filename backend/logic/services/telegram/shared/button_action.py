from typing import Self

from .exceptions import InvalidAction


__all__ = [
    'ButtonAction',
]


class ButtonAction:
    action: str

    def serialize(self) -> str:
        values = '|'.join(str(value) for value in self.__dict__.values())

        return f'{self.action}:{values}'

    @classmethod
    def parse(cls, data: str) -> Self:
        action, values = data.split(':', maxsplit=1)

        if action != cls.action:
            raise InvalidAction()

        values = values.split('|')

        return cls(*values)

    @classmethod
    def test(cls, data: str) -> bool:
        try:
            cls.parse(data)
        except InvalidAction:
            return False

        return True
