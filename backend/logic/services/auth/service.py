import hashlib
import hmac

from errors import NotFound

from .request import AuthRequest
from .responses import AuthResponse
from .exceptions import InvalidHash

from ..user import UserService, CreateUserRequest, GetUserRequest, UserCreateFields
from ..telegram import TelegramExternalService, TelegramGetUserDataRequest
from ..tokens import TokensService, CreateTokensRequest

from ...models import User




__all__ = [
    'AuthService',
]


class AuthService:
    def __init__(
        self,
        tokens_service: TokensService,
        telegram_service: TelegramExternalService,
        user_service: UserService,
        auth_bot_token: str,
    ):
        self._tokens_service = tokens_service
        self._telegram_service = telegram_service
        self._user_service = user_service
        self._auth_bot_token = auth_bot_token

    def auth(self, request: AuthRequest) -> AuthResponse:
        if not self._validate_is_true_request(request):
            raise InvalidHash()

        try:
            user = self._user_service.get(GetUserRequest(id=request.id)).entity
        except NotFound:
            user = self._create_new_user(request)

        auth_token, refresh_token = self._create_auth_tokens(user)

        return AuthResponse(auth_token=auth_token, refresh_token=refresh_token)

    def _create_new_user(self, request: AuthRequest) -> User:
        new_user_request = CreateUserRequest(fields=UserCreateFields(
            id=request.id,
            username=request.username,
            first_name=request.first_name,
            last_name=request.last_name if request.last_name else None,
            photo_url=request.photo_url if request.photo_url else None,
            role='default',
        ))

        response = self._user_service.create(new_user_request)

        return response.entity

    def _create_auth_tokens(self, user: User) -> tuple[str, str]:
        new_tokens_request = CreateTokensRequest(
            id=user.id,
        )

        tokens = self._tokens_service.create(new_tokens_request)

        return tokens.auth_token, tokens.refresh_token

    def _validate_is_true_request(self, request: AuthRequest) -> bool:
        msg = f'{chr(0x0A)}'.join(
            map(
                lambda x: '='.join(map(str, x)),
                sorted(
                    list(request.dict(exclude_none=True, exclude={'hash'}).items()),
                    key=lambda x: x[0]
                )
            )
        )

        key = hashlib.sha256(self._auth_bot_token.encode('utf-8')).digest()

        signature = hmac.new(
            key=key,
            msg=msg.encode('utf-8'),
            digestmod=hashlib.sha256,
        ).hexdigest()

        return signature == request.hash
