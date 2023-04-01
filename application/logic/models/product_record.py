from datetime import date

from pydantic import UUID4

from modeller import SModel


class ProductRecord(SModel):
    id: int
    owner_id: int
    product: UUID4
    weight: int
    date: date
