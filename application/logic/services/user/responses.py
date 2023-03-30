from pydantic import BaseModel

from ...models import User


__all__ = [
    'CreateUserResponse',
    'DeleteUserResponse',
    'UpdateUserResponse',
    'GetUserResponse',
    'ListUserResponse',
]


class CreateUserResponse(BaseModel):
    entity: User


class DeleteUserResponse(BaseModel): ...


class UpdateUserResponse(BaseModel):
    entity: User


class GetUserResponse(BaseModel):
    entity: User


class ListUserResponse(BaseModel):
    entity: list[User]
