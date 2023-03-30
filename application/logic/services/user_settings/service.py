from errors import NotFound

from .requests import *
from .responses import *

from ...models import UserSettings, User
from ...repositories import Repository


class UserSettingsService:
    def __init__(
        self,
        user_settings_repo: Repository[UserSettings],
    ):
        self._user_settings_repo = user_settings_repo

    def get(self, request: GetUserSettingsRequest) -> GetUserSettingsResponse:
        settings = self._user_settings_repo.find(UserSettings.id == request.id)
        if settings is None:
            raise NotFound('user_settings-not_found')

        return GetUserSettingsResponse(entity=settings)

    def update(self, request: UpdateUserSettingsRequest) -> UpdateUserSettingsResponse:
        settings = self._user_settings_repo.find(UserSettings.id == request.id)
        if settings is None:
            raise NotFound('user_settings-not_found')

        new_settings = UserSettings(
            id=settings.id,
            **request.fields.dict(),
        )

        saved_settings = self._user_settings_repo.save(new_settings)
        return UpdateUserSettingsResponse(entity=saved_settings)

    def delete(self, user: User) -> None:
        settings = self._user_settings_repo.find(UserSettings.id == user.id)
        self._user_settings_repo.delete(settings)

    def init_user(self, user: User) -> None:
        self._user_settings_repo.save(
            UserSettings(
                id=user.id,
            )
        )
