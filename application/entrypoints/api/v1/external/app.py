from .auth import auth_router

from ....shared import RestApp


class ExternalApp(RestApp):
    routers = [
        ('', auth_router),
    ]
