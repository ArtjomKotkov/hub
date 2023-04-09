from typing import Any, Optional

from errors import NotFound

from backend.access_tree import access_tree

from .exceptions import UnsupportedRequestorError

from ..shared import NotAllowed

from ...models import Requestor, User
from ...repositories import Repository


class AccessControlService:
    def __init__(
        self,
        user_repo: Repository[User],
    ):
        self._user_repo = user_repo

    def can(self, requestor: Requestor, target: Any, action: str, context: Optional[Any] = None) -> bool:
        subject = self._parse_subject(requestor)

        execute_context = {
            'provided': context,
            'default': access_tree,
        }

        return access_tree.execute(subject, target, action, execute_context)

    def check(self, requestor: Requestor, target: Any, action: str, context: Optional[Any] = None) -> None:
        if not self.can(requestor, target, action, context):
            target_name = target.__class__.__name__.lower() if not isinstance(target, type) else target.__name__.lower()
            raise NotAllowed(f'{action}-{target_name}-not_allowed')

    def _parse_subject(self, requestor: Requestor) -> User:
        if requestor.type == 'user':
            user = self._user_repo.find_one(User.id == requestor.id)
            if user is None:
                raise NotFound('user-not_found')
            return user
        else:
            raise UnsupportedRequestorError('requestor_type-not_found')

    def _make_default_context(self) -> dict[str, Any]:
        return {}
