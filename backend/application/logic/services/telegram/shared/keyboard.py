from pydantic import BaseModel, validator


__all__ = [
    'TELEGRAM_KEYBOARD_BUTTON_TYPE',
    'TelegramIKButton',
    'TelegramCallbackIKButton',
    'TelegramInlineKeyboard',
]


class TelegramIKButton(BaseModel):
    text: str


class TelegramCallbackIKButton(TelegramIKButton):
    callback_data: str

    @validator('callback_data')
    def must_be_64_bytes_long(cls, value: str):
        if len(value.encode()) > 64:
            raise ValueError

        return value

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True


TELEGRAM_KEYBOARD_BUTTON_TYPE = TelegramIKButton | TelegramCallbackIKButton


class TelegramInlineKeyboard(BaseModel):
    inline_keyboard: list[list[TELEGRAM_KEYBOARD_BUTTON_TYPE]]

    @validator('inline_keyboard')
    def keyboard_size_validation(cls, value: str):
        if len(value) > 12:
            raise ValueError('Keyboard support only 12 rows')

        if any(len(row) > 8 for row in value):
            raise ValueError('Keyboard support only 8 buttons per row')

        return value

