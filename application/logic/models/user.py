from typing import Optional

from modeller import SModel


class User(SModel):
    id: int
    username: str
    first_name: str
    last_name: Optional[str]
    photo_url: Optional[str]
    role: str = 'default'


