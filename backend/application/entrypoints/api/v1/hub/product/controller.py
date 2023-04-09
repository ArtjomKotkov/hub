from typing import Optional

from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject
from pydantic import UUID4

from backend.logic import (
    Logic, ProductsService,
    GetProductResponse, GetProductsListRequest,
    GetProductsListResponse, DeleteProductRequest,
    DeleteProductResponse, CreateProductRequest,
    CreateProductFields, CreateProductResponse,
    UpdateProductRequest, UpdateProductFields,
    UpdateProductResponse, GetProductRequest,
    GetProductListFilters,
)


product_router = APIRouter()


@product_router.get('/{product_id}')
@inject
def get(
    product_id: UUID4,
    product_service: ProductsService = Depends(Provide[Logic.services.products_service]),
) -> GetProductResponse:
    response = product_service.get(GetProductRequest(id=product_id))

    return response


@product_router.get('/')
@inject
def list_(
    owner_id: Optional[int] = None,
    product_service: ProductsService = Depends(Provide[Logic.services.products_service]),
) -> GetProductsListResponse:
    response = product_service.list(
        GetProductsListRequest(
            filters=GetProductListFilters(owner_id=owner_id)
        )
    )

    return response


@product_router.post('/')
@inject
def create(
    data: CreateProductFields,
    product_service: ProductsService = Depends(Provide[Logic.services.products_service]),
) -> CreateProductResponse:
    response = product_service.add(CreateProductRequest(fields=data))

    return response


@product_router.post('/{product_id}')
@inject
def update(
    product_id: UUID4,
    data: UpdateProductFields,
    product_service: ProductsService = Depends(Provide[Logic.services.products_service]),
) -> UpdateProductResponse:
    response = product_service.update(UpdateProductRequest(id=product_id, fields=data))

    return response


@product_router.delete('/{product_id}')
@inject
def delete(
    product_id: UUID4,
    product_service: ProductsService = Depends(Provide[Logic.services.products_service]),
) -> DeleteProductResponse:
    response = product_service.delete(DeleteProductRequest(id=product_id))

    return response
