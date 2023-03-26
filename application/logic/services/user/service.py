from typing import List

from errors import NotFound, AlreadyExists
from modeller import Evaluable

from .requests import (
    GetUserRequest, ListUserRequest,
    CreateUserRequest, UpdateUserRequest,
    DeleteUserRequest,
)

from ...repositories import Repository
from ...models import User

__all__ = [
    'UserService',
]


class UserService:
    def __init__(
        self,
        user_repo: Repository[User]
    ):
        self._user_repo = user_repo

    def get(self, request: GetUserRequest) -> User:
        model = self._user_repo.find_one(User.id == request.id)
        if not model:
            raise NotFound()

        return model

    def list(self, request: ListUserRequest) -> List[User]:
        models = self._user_repo.find(self._make_search_spec(request))

        return models

    def create(self, request: CreateUserRequest) -> User:
        new_model = User(**request.fields.dict())

        model = self._user_repo.find_one(User.id == new_model.id)
        if model:
            raise AlreadyExists()

        saved_model = self._user_repo.save(new_model)

        return saved_model

    def update(self, request: UpdateUserRequest) -> User:
        updating_model = User(phone=request.phone, **request.fields.dict())

        model = self._user_repo.find_one(User.id == updating_model.id)
        if not model:
            raise NotFound()

        saved_model = self._user_repo.save(updating_model)

        return saved_model

    def delete(self, request: DeleteUserRequest) -> None:
        model = self._user_repo.find_one(User.phone == request.phone)
        if not model:
            raise NotFound()

        self._user_repo.delete(model)

    @staticmethod
    def _make_search_spec(request: ListUserRequest) -> Evaluable:
        result = None

        if request.roles:
            spec = User.role.in_(request.roles)

            result = result & spec if result else spec

        return result
