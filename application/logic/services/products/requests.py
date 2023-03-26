from typing import Optional

from pydantic import BaseModel, UUID4

__all__ = [
    'CreateProductRequest',
    'CreateProductFields',
    'UpdateProductFields',
    'UpdateProductRequest',
    'GetProductsListRequest',
    'GetProductRequest',
    'DeleteProductRequest',
]


class GetProductRequest(BaseModel):
    id: UUID4


class GetProductsListRequest(BaseModel): ...


class CreateProductFields(BaseModel):
    name: str
    calories: float
    protein: float
    carbohydrate: float
    fat: float


class UpdateProductFields(BaseModel):
    name: Optional[str]
    calories: Optional[float]
    protein: Optional[float]
    carbohydrate: Optional[float]
    fat: Optional[float]


class CreateProductRequest(BaseModel):
    fields: CreateProductFields


class UpdateProductRequest(BaseModel):
    id: UUID4
    fields: UpdateProductFields


class DeleteProductRequest(BaseModel):
    id: UUID4
