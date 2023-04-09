from backend.entrypoints.shared import RestApp

from .user import user_router
from .settings import user_settings_router


class UserApp(RestApp):
    routers = [
        ('', user_router),
        ('/settings', user_settings_router)
    ]
