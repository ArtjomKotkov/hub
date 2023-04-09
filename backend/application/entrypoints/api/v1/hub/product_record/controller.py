from fastapi import APIRouter, Depends, Request
from dependency_injector.wiring import Provide, inject

from backend.logic import (
    Logic, ProductRecordService,
    ListProductRecordRequest, ListProductRecordResponse,
    AddProductRecordFields, AddProductRecordRequest,
    AddProductRecordResponse, UpdateProductRecordFields,
    UpdateProductRecordRequest, UpdateProductRecordResponse,
    DeleteProductRecordResponse, DeleteProductRecordRequest,
    ListProductRecordFilters,
)


product_record_router = APIRouter()


@product_record_router.get('/')
@inject
def list_(
    request: Request,
    data: ListProductRecordFilters,
    product_record_service: ProductRecordService = Depends(Provide[Logic.services.prodict_record_service]),
) -> ListProductRecordResponse:
    requestor = request.state.requestor
    response = product_record_service.list(ListProductRecordRequest(requestor=requestor, filters=data))

    return response


@product_record_router.post('/')
@inject
def create(
    request: Request,
    data: AddProductRecordFields,
    product_record_service: ProductRecordService = Depends(Provide[Logic.services.prodict_record_service]),
) -> AddProductRecordResponse:
    requestor = request.state.requestor
    response = product_record_service.add(AddProductRecordRequest(requestor=requestor, fields=data))

    return response


@product_record_router.post('/{product_record_id}')
@inject
def update(
    request: Request,
    product_record_id: int,
    data: UpdateProductRecordFields,
    product_record_service: ProductRecordService = Depends(Provide[Logic.services.prodict_record_service]),
) -> UpdateProductRecordResponse:
    requestor = request.state.requestor
    response = product_record_service.update(
        UpdateProductRecordRequest(requestor=requestor, id=product_record_id, fields=data)
    )

    return response


@product_record_router.delete('/{product_record_id}')
@inject
def update(
    request: Request,
    product_record_id: int,
    product_record_service: ProductRecordService = Depends(Provide[Logic.services.prodict_record_service]),
) -> DeleteProductRecordResponse:
    requestor = request.state.requestor
    response = product_record_service.delete(DeleteProductRecordRequest(requestor=requestor, id=product_record_id))

    return response
