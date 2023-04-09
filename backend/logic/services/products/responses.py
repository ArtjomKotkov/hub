from pydantic import BaseModel

from ...models import Product


__all__ = [
    'CreateProductResponse',
    'UpdateProductResponse',
    'GetProductResponse',
    'GetProductsListResponse',
    'DeleteProductResponse',
]


class CreateProductResponse(BaseModel):
    entity: Product


class UpdateProductResponse(BaseModel):
    entity: Product


class GetProductResponse(BaseModel):
    entity: Product


class GetProductsListResponse(BaseModel):
    entities: list[Product]


class DeleteProductResponse(BaseModel): ...
