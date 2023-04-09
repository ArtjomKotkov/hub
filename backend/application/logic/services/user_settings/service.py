from errors import NotFound

from .requests import *
from .responses import *

from ..access_control import AccessControlService

from ...models import UserSettings, User, Feature
from ...repositories import Repository


class UserSettingsService:
    feature = Feature(name='products')

    def __init__(
        self,
        user_settings_repo: Repository[UserSettings],
        access_control_service: AccessControlService,
    ):
        self._user_settings_repo = user_settings_repo
        self._access_control_service = access_control_service

    def get(self, request: GetUserSettingsRequest) -> GetUserSettingsResponse:
        self._access_control_service.check(request.requestor, self.feature, 'access')

        settings = self._user_settings_repo.find(UserSettings.owner_id == request.id)
        if settings is None:
            raise NotFound('user_settings-not_found')

        self._access_control_service.check(request.requestor, UserSettings, 'read')

        return GetUserSettingsResponse(entity=settings)

    def update(self, request: UpdateUserSettingsRequest) -> UpdateUserSettingsResponse:
        self._access_control_service.check(request.requestor, self.feature, 'access')

        settings = self._user_settings_repo.find(UserSettings.owner_id == request.id)
        if settings is None:
            raise NotFound('user_settings-not_found')

        self._access_control_service.check(request.requestor, settings, 'update')

        new_settings = UserSettings(
            id=settings.owner_id,
            **request.fields.dict(),
        )

        saved_settings = self._user_settings_repo.save(new_settings)
        return UpdateUserSettingsResponse(entity=saved_settings)

    def delete(self, user: User) -> None:
        settings = self._user_settings_repo.find(UserSettings.owner_id == user.id)
        self._user_settings_repo.delete(settings)

    def init_user(self, user: User) -> None:
        self._user_settings_repo.save(
            UserSettings(
                owner_id=user.id,
            )
        )
