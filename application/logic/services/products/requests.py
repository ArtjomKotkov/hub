from typing import Optional

from pydantic import BaseModel, UUID4

from ..shared import RequestorRequest


__all__ = [
    'CreateProductRequest',
    'CreateProductFields',
    'UpdateProductFields',
    'UpdateProductRequest',
    'GetProductsListRequest',
    'GetProductRequest',
    'DeleteProductRequest',
    'GetProductListFilters',
]


class GetProductRequest(RequestorRequest):
    id: UUID4


class GetProductListFilters(BaseModel):
    owner_id: Optional[int]


class GetProductsListRequest(RequestorRequest):
    filters: GetProductListFilters


class CreateProductFields(BaseModel):
    name: str
    calories: float
    protein: float
    carbohydrate: float
    fat: float


class UpdateProductFields(CreateProductFields): ...


class CreateProductRequest(RequestorRequest):
    fields: CreateProductFields


class UpdateProductRequest(RequestorRequest):
    id: UUID4
    fields: UpdateProductFields


class DeleteProductRequest(RequestorRequest):
    id: UUID4
