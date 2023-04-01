from datetime import date

from pydantic import BaseModel, UUID4, Extra

from ..shared import RequestorRequest


__all__ = [
    'AddProductRecordFields',
    'UpdateProductRecordFields',
    'AddProductRecordRequest',
    'UpdateProductRecordRequest',
    'DeleteProductRecordRequest',
    'ListProductRecordRequest',
    'ListProductRecordFilters',
]


class AddProductRecordFields(BaseModel):
    product: UUID4
    weight: int
    date: date
    owner: int


class UpdateProductRecordFields(BaseModel, extra=Extra.ignore):
    weight: int


class AddProductRecordRequest(RequestorRequest):
    fields: AddProductRecordFields


class UpdateProductRecordRequest(RequestorRequest):
    id: int
    fields: UpdateProductRecordFields


class DeleteProductRecordRequest(RequestorRequest):
    id: int


class ListProductRecordFilters(BaseModel):
    date: date


class ListProductRecordRequest(RequestorRequest):
    filters: ListProductRecordFilters
