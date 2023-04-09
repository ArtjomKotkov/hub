from uuid import uuid4

from pydantic.types import UUID4
from pydantic import Field

from modeller import SModel


class Product(SModel):
    id: UUID4 = Field(default=uuid4(), const=True)
    name: str
    calories: float
    protein: float
    carbohydrate: float
    fat: float

    owner_id: int
