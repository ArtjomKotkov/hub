from typing import Optional

from modeller import SModel


class UserSettings(SModel):
    id: int
    calories_limit: Optional[int]
    height: Optional[int]
    weight: Optional[int]
    age: Optional[int]
