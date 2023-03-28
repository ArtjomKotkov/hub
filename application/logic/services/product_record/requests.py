from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, UUID4

__all__ = [
    'AddProductRecordFields',
    'UpdateProductRecordFields',
    'AddProductRecordRequest',
    'UpdateProductRecordRequest',
    'DeleteProductRecordRequest',
    'ListProductRecordRequest',
]


class AddProductRecordFields(BaseModel):
    product: UUID4
    weight: int
    date: date


class UpdateProductRecordFields(BaseModel):
    weight: Optional[int]


class AddProductRecordRequest(BaseModel):
    fields: AddProductRecordFields


class UpdateProductRecordRequest(BaseModel):
    id: int
    fields: UpdateProductRecordFields


class DeleteProductRecordRequest(BaseModel):
    id: int


class ListProductRecordRequest:
    date: date