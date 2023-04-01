from errors import NotFound

from .requests import *
from .responses import *

from ..access_control import AccessControlService

from ...models import ProductRecord, Product, Feature
from ...repositories import Repository


class ProductRecordService:
    feature = Feature(name='product_record')

    def __init__(
        self,
        access_control_service: AccessControlService,
        product_record_repo: Repository[ProductRecord],
        products_repo: Repository[Product],
    ):
        self._access_control_service = access_control_service
        self._product_record_repo = product_record_repo
        self._products_repo = products_repo

    def list(self, request: ListProductRecordRequest) -> ListProductRecordResponse:
        self._access_control_service.check(request.requestor, self.feature, 'access')
        self._access_control_service.check(request.requestor, Product, 'read')

        return ListProductRecordResponse(
            entities=self._product_record_repo.find(ProductRecord.date == request.filters.date)
        )

    def add(self, request: AddProductRecordRequest) -> AddProductRecordResponse:
        self._access_control_service.check(request.requestor, self.feature, 'access')
        self._access_control_service.check(request.requestor, Product, 'create')

        product = self._products_repo.find_one(Product.id == request.fields.product)
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
        self._access_control_service.check(request.requestor, self.feature, 'access')

        old_product_record = self._product_record_repo.find(ProductRecord.id == request.id)
        if old_product_record is None:
            raise NotFound('product-record-not-found')

        self._access_control_service.check(request.requestor, old_product_record, 'update')

        new_model_record = ProductRecord(
            **{
                **old_product_record.dict(),
                **request.fields.dict(),
            }
        )

        self._product_record_repo.save(new_model_record)

        return UpdateProductRecordResponse(entity=new_model_record)

    def delete(self, request: DeleteProductRecordRequest) -> DeleteProductRecordResponse:
        self._access_control_service.check(request.requestor, self.feature, 'access')

        product_record = self._product_record_repo.find(ProductRecord.id == request.id)

        self._access_control_service.check(request.requestor, product_record, 'delete')

        if product_record is None:
            raise NotFound('product-record-not-found')

        self._product_record_repo.delete(product_record)

        return DeleteProductRecordResponse()
