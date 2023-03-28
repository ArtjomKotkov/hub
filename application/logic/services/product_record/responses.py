from pydantic import BaseModel


from ...models import ProductRecord


__all__ = [
    'AddProductRecordResponse',
    'UpdateProductRecordResponse',
    'DeleteProductRecordResponse',
    'ListProductRecordResponse',
]


class BaseResponse(BaseModel):
    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True


class AddProductRecordResponse(BaseResponse):
    entity: ProductRecord


class UpdateProductRecordResponse(BaseResponse):
    entity: ProductRecord


class DeleteProductRecordResponse(BaseModel): ...


class ListProductRecordResponse(BaseResponse):
    entities: list[ProductRecord]
