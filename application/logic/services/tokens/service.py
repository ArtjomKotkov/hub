from datetime import datetime, timedelta

from errors import NotFound

from jwt import encode

from ...repositories import Repository
from ...models import AuthToken, RefreshToken, User

from .requests import CreateTokensRequest, DeleteTokensRequest, RefreshTokenRequest
from .responses import CreateTokensResponse, RefreshTokenResponse
from .exceptions import TokenExpired


__all__ = [
    'TokensService',
]


SECRET = 'some_secret_phrase'
AUTH_TOKEN_EXPIRES_IN = 60*60
REFRESH_TOKEN_EXPIRES_IN = 60*60*24*30


class TokensService:
    _encode_algorithm = 'HS256'

    def __init__(
        self,
        auth_token_repo: Repository[AuthToken],
        refresh_token_repo: Repository[RefreshToken],
        user_repo: Repository[User],
    ):
        self._auth_token_repo = auth_token_repo
        self._refresh_token_repo = refresh_token_repo
        self._user_repo = user_repo

    def create(self, request: CreateTokensRequest) -> CreateTokensResponse:
        user = self._user_repo.find_one(User.id == request.id)
        if not user:
            raise NotFound()

        auth_token, refresh_token = self._generate_tokens(user.id)

        return CreateTokensResponse(
            auth_token=auth_token,
            refresh_token=refresh_token,
        )

    def delete(self, request: DeleteTokensRequest) -> None:
        auth_token = self._auth_token_repo.find_one(AuthToken.token == request.auth_token)
        if not auth_token:
            raise NotFound()

        if datetime.fromtimestamp(auth_token.expires_in) > datetime.now():
            raise TokenExpired(description='Auth token expired.')

        self._auth_token_repo.delete(auth_token)

        refresh_token = self._refresh_token_repo.find_one(RefreshToken.auth_token == request.auth_token)
        if refresh_token:
            self._refresh_token_repo.delete(auth_token)

        return None

    def refresh_token(self, request: RefreshTokenRequest) -> RefreshTokenResponse:
        refresh_token = self._refresh_token_repo.find_one(RefreshToken.refresh_token == request.refresh_token)
        if not refresh_token:
            raise NotFound('Refresh token not found.')

        if datetime.fromtimestamp(refresh_token.expires_in) > datetime.now():
            raise TokenExpired(description='Refresh token expired.')

        auth_token = self._auth_token_repo.find_one(AuthToken.token == request.auth_token)
        if not auth_token:
            raise NotFound('Auth token not found.')

        self._auth_token_repo.delete(auth_token)
        self._refresh_token_repo.delete(refresh_token)

        new_auth_token, new_refresh_token = self._generate_tokens(auth_token.phone)

        return RefreshTokenResponse(
            auth_token=new_auth_token,
            refresh_token=new_refresh_token,
        )

    def _generate_tokens(self, id: int) -> tuple[str, str]:
        current_datetime = datetime.now()

        auth_token_expiration = current_datetime + timedelta(seconds=AUTH_TOKEN_EXPIRES_IN)
        refresh_token_expiration = current_datetime + timedelta(seconds=REFRESH_TOKEN_EXPIRES_IN)

        auth_token_payload = {
            'expires_in': auth_token_expiration.timestamp()
        }

        refresh_token_payload = {
            'expires_in': refresh_token_expiration.timestamp()
        }

        auth_token = encode(auth_token_payload, SECRET, algorithm=self._encode_algorithm)
        refresh_token = encode(refresh_token_payload, SECRET, algorithm=self._encode_algorithm)

        auth_token_model = AuthToken(
            id=id,
            token=auth_token,
            expires_in=auth_token_expiration,
        )

        refresh_token_model = RefreshToken(
            id=id,
            refresh_token=refresh_token,
            auth_token=auth_token,
            expires_in=refresh_token_expiration,
        )

        self._auth_token_repo.save(auth_token_model)
        self._refresh_token_repo.save(refresh_token_model)

        return auth_token, refresh_token
