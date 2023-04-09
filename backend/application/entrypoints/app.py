from errors import Error
from pydantic import BaseConfig

from .api import ApiApp
from .shared import RestApp
from .error_handlers import errors_handler


BaseConfig.arbitrary_types_allowed = True


class Entrypoints(RestApp):
    sub_apps = [
        ('/api', ApiApp),
    ]
    exception_handlers = [
        (Error, errors_handler),
    ]
    propagate_exception_handlers = True
