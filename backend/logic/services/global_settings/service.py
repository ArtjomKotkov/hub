from backend.settings import Settings

from .responses import GlobalSettingsResponse, GlobalSettingsFields


class GlobalSettingsService:
    def get(self) -> GlobalSettingsResponse:
        return GlobalSettingsResponse(
            entity=GlobalSettingsFields(
                refresh_token_cookie_name=Settings.REFRESH_TOKEN_COOKIE_NAME,
                auth_token_cookie_name=Settings.AUTH_TOKEN_COOKIE_NAME,
                auth_token_expires_in=Settings.AUTH_TOKEN_EXPIRES_IN,
                refresh_token_expires_in=Settings.AUTH_TOKEN_EXPIRES_IN,
            )
        )
