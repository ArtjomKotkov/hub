from fastapi import Depends

from application.entrypoints.shared import RestApp

from .product import product_router
from .product_record import product_record_router
from .dependencies import check_authentication
from .user import UserApp


class HubApp(RestApp):
    sub_apps = [
        ('/users', UserApp),
    ]

    routers = [
        ('/products', product_router),
        ('/product_records', product_record_router),
    ]

    dependencies = [
        Depends(check_authentication),
    ]
