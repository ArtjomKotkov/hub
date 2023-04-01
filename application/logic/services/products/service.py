from errors import NotFound

from .requests import (
    CreateProductRequest, UpdateProductRequest,
    GetProductRequest, GetProductsListRequest,
    DeleteProductRequest,
)
from .responses import (
    CreateProductResponse, UpdateProductResponse,
    GetProductResponse, GetProductsListResponse,
    DeleteProductResponse,
)

from ..access_control import AccessControlService
from ..shared import NotAllowed

from ...repositories import Repository
from ...models import Product, Feature, UserSettings, Requestor


class ProductsService:
    feature = Feature(name='products')

    def __init__(
        self,
        access_control_service: AccessControlService,
        products_repo: Repository[Product],
        user_settings_repo: Repository[UserSettings],
    ):
        self._products_repo = products_repo
        self._access_control_service = access_control_service
        self._user_settings_repo = user_settings_repo

    def get(self, request: GetProductRequest) -> GetProductResponse:
        self._access_control_service.check(request.requestor, self.feature, 'access')

        product = self._products_repo.find_one(Product.id == request.id)
        if product is None:
            raise NotFound()

        self._access_control_service.check(
            request.requestor,
            product,
            'read',
            self._get_product_context(request.requestor, product),
        )

        return product

    def _get_product_context(self, requestor: Requestor, product: Product) -> dict:
        if requestor.id == product.owner_id:
            return {}

        product_owner_settings = self._user_settings_repo.find_one(
            UserSettings.owner_id == product.owner_id
        )

        return {
            'target_owner_settings': {
                'share_products': product_owner_settings.share_products,
            }
        }

    def list(self, request: GetProductsListRequest) -> GetProductsListResponse:
        self._access_control_service.check(request.requestor, self.feature, 'access')
        self._access_control_service.check(request.requestor, Product, 'read')

        return GetProductsListResponse(
            entities=self._products_repo.find(self._get_list_spec(request))
        )

    def _get_list_spec(self, request: GetProductsListRequest):
        owner_id = request.filters.owner_id

        if request.filters.owner_id is None:
            users_with_shared_products = self._user_settings_repo.find(UserSettings.share_products == True)
            return Product.owner_id in [settings.owner_id for settings in users_with_shared_products]
        elif request.requestor.id != owner_id:
            product_owner_settings = self._user_settings_repo.find_one(
                UserSettings.owner_id == owner_id
            )

            if not product_owner_settings.share_products:
                raise NotAllowed()
            else:
                return Product.owner_id == owner_id
        else:
            return Product.owner_id == owner_id

    def add(self, request: CreateProductRequest) -> CreateProductResponse:
        self._access_control_service.check(request.requestor, self.feature, 'access')
        self._access_control_service.check(request.requestor, Product, 'write')

        product = Product(**request.fields.dict(), owner_id=request.requestor.id)

        product = self._products_repo.save(product)

        return CreateProductResponse(entity=product)

    def update(self, request: UpdateProductRequest) -> UpdateProductResponse:
        self._access_control_service.check(request.requestor, self.feature, 'access')

        product = self._products_repo.find_one(Product.id == request.id)
        if product is None:
            raise NotFound()

        self._access_control_service.check(request.requestor, product, 'update')

        new_product = Product(
            **{
                'id': product.id,
                **request.fields.dict(),
            }
        )

        new_product = self._products_repo.save(new_product)

        return UpdateProductResponse(entiry=new_product)

    def delete(self, request: DeleteProductRequest) -> DeleteProductResponse:
        self._access_control_service.check(request.requestor, self.feature, 'access')

        product = self._products_repo.find_one(Product.id == request.id)
        if product is None:
            raise NotFound()

        self._access_control_service.check(request.requestor, product, 'delete')

        self._products_repo.delete(product)

        return DeleteProductResponse()
