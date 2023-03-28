from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from application.logic import (
    Logic, ProductRecordService,
    ListProductRecordRequest, ListProductRecordResponse,
    AddProductRecordFields, AddProductRecordRequest,
    AddProductRecordResponse, UpdateProductRecordFields,
    UpdateProductRecordRequest, UpdateProductRecordResponse,
    DeleteProductRecordResponse, DeleteProductRecordRequest,
)


product_record_router = APIRouter()


@product_record_router.get('/')
@inject
def list_(
    data: ListProductRecordRequest,
    product_record_service: ProductRecordService = Depends(Provide[Logic.services.prodict_record_service]),
) -> ListProductRecordResponse:
    response = product_record_service.list(data)

    return response


@product_record_router.post('/')
@inject
def create(
    data: AddProductRecordFields,
    product_record_service: ProductRecordService = Depends(Provide[Logic.services.prodict_record_service]),
) -> AddProductRecordResponse:
    response = product_record_service.add(AddProductRecordRequest(fields=data))

    return response


@product_record_router.post('/{product_record_id}')
@inject
def update(
    product_record_id: int,
    data: UpdateProductRecordFields,
    product_record_service: ProductRecordService = Depends(Provide[Logic.services.prodict_record_service]),
) -> UpdateProductRecordResponse:
    response = product_record_service.update(UpdateProductRecordRequest(id=product_record_id, fields=data))

    return response


@product_record_router.delete('/{product_record_id}')
@inject
def update(
    product_record_id: int,
    product_record_service: ProductRecordService = Depends(Provide[Logic.services.prodict_record_service]),
) -> DeleteProductRecordResponse:
    response = product_record_service.delete(DeleteProductRecordRequest(id=product_record_id))

    return response
