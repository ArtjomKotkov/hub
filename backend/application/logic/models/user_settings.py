from typing import Optional

from modeller import SModel


class UserSettings(SModel):
    calories_limit: Optional[int] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    age: Optional[int] = None

    share_products: bool = False

    owner_id: int
