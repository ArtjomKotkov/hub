from .auth import auth_router
from .global_settings import global_settings_router

from ....shared import RestApp


class ExternalApp(RestApp):
    routers = [
        ('/auth', auth_router),
        ('/global_settings', global_settings_router),
    ]
