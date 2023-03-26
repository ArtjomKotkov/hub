from .button_types import *

from ....shared import ButtonAction


__all__ = [
    'ButtonActionApproveSession',
]


class ButtonActionApproveSession(ButtonAction):
    action = CallbackButtonTypes.APPROVE_SESSION

    def __init__(self, session_id: str) -> None:
        self.session_id = session_id
