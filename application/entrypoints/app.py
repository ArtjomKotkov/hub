from errors import Error

from .api import ApiApp
from .shared import RestApp
from .error_handlers import errors_handler


class Entrypoints(RestApp):
    sub_apps = [
        ('/api', ApiApp),
    ]
    exception_handlers = [
        (Error, errors_handler),
    ]
    propagate_exception_handlers = True
