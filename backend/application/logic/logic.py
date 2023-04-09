from .services import Services
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject


class Logic(containers.DeclarativeContainer):
    services = providers.Container(Services)