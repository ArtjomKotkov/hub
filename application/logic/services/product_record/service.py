from errors import NotFound

from .requests import *
from .responses import *

from ...models import ProductRecord, Product
from ...repositories import Repository


class ProductRecordService:
    def __init__(
        self,
        product_record_repo: Repository[ProductRecord],
        products_repo: Repository[Product],
    ):
        self._product_record_repo = product_record_repo
        self._products_repo = products_repo

    def list(self, request: ListProductRecordRequest) -> ListProductRecordResponse:
        return ListProductRecordResponse(entities=self._product_record_repo.find(ProductRecord.date == request.date))

    def add(self, request: AddProductRecordRequest) -> AddProductRecordResponse:
        product = self._products_repo.find_one(request.fields.product)
        if product is None:
            raise NotFound('product-id-not-found')

        # TODO: переделать, получаем количество, чтобы сформировать id
        count = len(self._product_record_repo.find())

        product_record = ProductRecord(
            id=count+1,
            owner=request.fields.owner,
            product=request.fields.product,
            weight=request.fields.product,
            date=request.fields.date,
        )

        self._product_record_repo.save(product_record)

        return AddProductRecordResponse(entity=product_record)

    def update(self, request: UpdateProductRecordRequest) -> UpdateProductRecordResponse:
        old_product_record = self._product_record_repo.find(ProductRecord.id == request.id)
        if old_product_record is None:
            raise NotFound('product-record-not-found')

        new_model_record = ProductRecord(
            **{
                **old_product_record.dict(),
                **request.fields.dict(),
            }
        )

        self._product_record_repo.save(new_model_record)

        return UpdateProductRecordResponse(entity=new_model_record)

    def delete(self, request: DeleteProductRecordRequest) -> DeleteProductRecordResponse:
        product_record = self._product_record_repo.find(ProductRecord.id == request.id)
        if product_record is None:
            raise NotFound('product-record-not-found')

        self._product_record_repo.delete(product_record)

        return DeleteProductRecordResponse()
