from fastapi import Depends
from pydantic import BaseConfig

from application.entrypoints.shared import RestApp
from .product import product_router
from .product_record import product_record_router
from .dependencies import check_authentication


BaseConfig.arbitrary_types_allowed = True


class HubApp(RestApp):
    routers = [
        ('/product', product_router),
        ('/product_record', product_record_router),
    ]

    dependencies = [
        Depends(check_authentication),
    ]
