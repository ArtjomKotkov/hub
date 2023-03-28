from pydantic import BaseModel


from ...models import ProductRecord


__all__ = [
    'AddProductRecordResponse',
    'UpdateProductRecordResponse',
    'DeleteProductRecordResponse',
    'ListProductRecordResponse',
]


class AddProductRecordResponse(BaseModel):
    entity: ProductRecord


class UpdateProductRecordResponse(BaseModel):
    entity: ProductRecord


class DeleteProductRecordResponse(BaseModel): ...


class ListProductRecordResponse(BaseModel):
    entities: list[ProductRecord]
