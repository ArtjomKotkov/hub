from typing import Optional, List

from pydantic import BaseModel


__all__ = [
    'GetUserRequest',
    'ListUserRequest',
    'CreateUserRequest',
    'UpdateUserRequest',
    'DeleteUserRequest',
    'UserCreateFields',
    'UserUpdateFields',
]


class UserCommonFields(BaseModel):
    username: str
    first_name: str
    last_name: Optional[str]
    photo_url: Optional[str]
    role: str


class UserCreateFields(UserCommonFields):
    id: int


class UserUpdateFields(UserCommonFields):
    role: str


class GetUserRequest(BaseModel):
    id: int


class ListUserRequest(BaseModel):
    roles: Optional[List[str]]


class CreateUserRequest(BaseModel):
    fields: UserCreateFields


class UpdateUserRequest(BaseModel):
    phone: int
    fields: UserUpdateFields


class DeleteUserRequest(BaseModel):
    id: int

