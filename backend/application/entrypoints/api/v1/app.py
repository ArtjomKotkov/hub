from .hub import HubApp
from .external import ExternalApp

from ...shared import RestApp


class V1App(RestApp):
    sub_apps = [
        ('/hub', HubApp),
        ('/external', ExternalApp),
    ]
