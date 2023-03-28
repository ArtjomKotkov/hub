from fastapi import FastAPI
from pydantic import BaseConfig

from .product import product_router
from .product_record import product_record_router

BaseConfig.arbitrary_types_allowed = True

app_hub = FastAPI()
app_hub.include_router(product_router, prefix='/product')
app_hub.include_router(product_record_router, prefix='/product_record')
