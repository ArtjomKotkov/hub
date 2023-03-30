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

from ..tokens import TokensService
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
        tokens_service: TokensService,
    ):
        self._user_repo = user_repo
        self._user_settings_service = user_settings_service
        self._tokens_service = tokens_service

    def get(self, request: GetUserRequest) -> GetUserResponse:
        model = self._user_repo.find_one(User.id == request.id)
        if not model:
            raise NotFound('user-not_found')

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
        model = User(id=request.id, **request.fields.dict())

        old_user = self._user_repo.find_one(User.id == model.id)
        if not old_user:
            raise NotFound()

        new_user = self._user_repo.save(model)

        self._update_hook(old_user, new_user)

        return UpdateUserResponse(entity=new_user)

    def _update_hook(self, old_user: User, new_user: User) -> None:
        if old_user.role != new_user.role:
            self._tokens_service.delete_user_tokens(new_user)

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
