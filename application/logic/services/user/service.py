from typing import List

from errors import NotFound, AlreadyExists
from modeller import Evaluable

from .requests import (
    GetUserRequest, ListUserRequest,
    CreateUserRequest, UpdateUserRequest,
    DeleteUserRequest,
)
from .responses import (
    GetUserResponse, ListUserResponse,
    CreateUserResponse, UpdateUserResponse,
    DeleteUserResponse,
)

from ..user_settings import UserSettingsService

from ...repositories import Repository
from ...models import User

__all__ = [
    'UserService',
]


class UserService:
    def __init__(
        self,
        user_repo: Repository[User],
        user_settings_service: UserSettingsService,
    ):
        self._user_repo = user_repo
        self._user_settings_service = user_settings_service

    def get(self, request: GetUserRequest) -> GetUserResponse:
        model = self._user_repo.find_one(User.id == request.id)
        if not model:
            raise NotFound()

        return GetUserResponse(entity=model)

    def list(self, request: ListUserRequest) -> ListUserResponse:
        models = self._user_repo.find(self._make_search_spec(request))

        return ListUserResponse(entities=models)

    def create(self, request: CreateUserRequest) -> CreateUserResponse:
        user = User(**request.fields.dict())

        model = self._user_repo.find_one(User.id == user.id)
        if model:
            raise AlreadyExists()

        saved_user = self._user_repo.save(user)
        self._user_settings_service.init_user(saved_user)

        return CreateUserResponse(entity=saved_user)

    def update(self, request: UpdateUserRequest) -> UpdateUserResponse:
        updating_model = User(phone=request.phone, **request.fields.dict())

        model = self._user_repo.find_one(User.id == updating_model.id)
        if not model:
            raise NotFound()

        saved_model = self._user_repo.save(updating_model)

        return UpdateUserResponse(entity=saved_model)

    def delete(self, request: DeleteUserRequest) -> DeleteUserResponse:
        model = self._user_repo.find_one(User.id == request.id)
        if not model:
            raise NotFound()

        self._user_repo.delete(model)

        return DeleteUserResponse()

    @staticmethod
    def _make_search_spec(request: ListUserRequest) -> Evaluable:
        result = None

        if request.roles:
            spec = User.role.in_(request.roles)

            result = result & spec if result else spec

        return result
