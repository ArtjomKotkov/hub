from .v1 import V1App
from ..shared import RestApp


class ApiApp(RestApp):
    sub_apps = [
        ('/v1', V1App),
    ]
