from typing import Optional

from pydantic import BaseModel


class Requestor(BaseModel):
    id: Optional[int]
    type: str
    role: str
