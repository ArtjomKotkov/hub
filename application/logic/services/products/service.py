from errors import NotFound

from ...repositories import Repository
from ...models import Product

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


class ProductsService:
    def __init__(
        self,
        products_repo: Repository[Product],
    ):
        self._products_repo = products_repo

    def get(self, request: GetProductRequest) -> GetProductResponse:
        product = self._products_repo.find_one(Product.id == request.id)
        if product is None:
            raise NotFound()

        return product

    def list(self, request: GetProductsListRequest) -> GetProductsListResponse:
        return GetProductsListResponse(entities=self._products_repo.find())

    def add(self, request: CreateProductRequest) -> CreateProductResponse:
        product = Product(**request.fields.dict())

        product = self._products_repo.save(product)

        return CreateProductResponse(entity=product)

    def update(self, request: UpdateProductRequest) -> UpdateProductResponse:
        product = self._products_repo.find_one(Product.id == request.id)
        if product is None:
            raise NotFound()

        new_product = Product(
            **{
                'id': product.id,
                **request.fields.dict(),
            }
        )

        new_product = self._products_repo.save(new_product)

        return UpdateProductResponse(entiry=new_product)

    def delete(self, request: DeleteProductRequest) -> DeleteProductResponse:
        product = self._products_repo.find_one(Product.id == request.id)
        if product is None:
            raise NotFound()

        self._products_repo.delete(product)

        return DeleteProductResponse()
