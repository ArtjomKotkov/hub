from typing import Optional

from modeller import SModel


class UserSettings(SModel):
    calories_limit: Optional[int]
    height: Optional[int]
    weight: Optional[int]
    age: Optional[int]

    share_products: bool = False

    owner_id: int
