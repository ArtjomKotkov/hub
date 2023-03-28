from datetime import date

from pydantic import BaseModel, UUID4, Extra


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


class UpdateProductRecordFields(BaseModel, extra=Extra.ignore):
    weight: int


class AddProductRecordRequest(BaseModel):
    fields: AddProductRecordFields


class UpdateProductRecordRequest(BaseModel):
    id: int
    fields: UpdateProductRecordFields


class DeleteProductRecordRequest(BaseModel):
    id: int


class ListProductRecordRequest(BaseModel):
    date: date
