from datetime import datetime, timedelta
import json

from errors import NotFound

from jwt import encode

from settings import Settings

from ...repositories import Repository
from ...models import AuthToken, RefreshToken, User, AuthTokenPayload, RefreshTokenPayload

from .requests import CreateTokensRequest, DeleteTokensRequest, RefreshTokenRequest
from .responses import CreateTokensResponse, RefreshTokenResponse
from .exceptions import TokenExpired


__all__ = [
    'TokensService',
]


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

        auth_token, refresh_token = self._generate_tokens(user)

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
            self._refresh_token_repo.delete(refresh_token)
            raise TokenExpired(description='Refresh token expired.')

        auth_token = self._auth_token_repo.find_one(AuthToken.token == request.auth_token)
        if not auth_token:
            raise NotFound('Auth token not found.')

        self._auth_token_repo.delete(auth_token)
        self._refresh_token_repo.delete(refresh_token)

        user = self._user_repo.find_one(User.id == auth_token)
        if user is None:
            raise NotFound('user-not_found')

        new_auth_token, new_refresh_token = self._generate_tokens(user)

        return RefreshTokenResponse(
            auth_token=new_auth_token,
            refresh_token=new_refresh_token,
        )

    def _generate_tokens(self, user: User) -> tuple[str, str]:
        current_datetime = datetime.now()

        auth_token_expiration = current_datetime + timedelta(seconds=Settings.AUTH_TOKEN_EXPIRES_IN)
        refresh_token_expiration = current_datetime + timedelta(seconds=Settings.REFRESH_TOKEN_EXPIRES_IN)

        auth_token_payload = AuthTokenPayload(
            id=user.id,
            role=user.role,
            expires_in=auth_token_expiration,
        )

        refresh_token_payload = RefreshTokenPayload(
            expires_in=refresh_token_expiration,
        )

        auth_token = encode(json.dumps(auth_token_payload.json()), Settings.APP_SECRET, algorithm=self._encode_algorithm)
        refresh_token = encode(json.dumps(refresh_token_payload.json()), Settings.APP_SECRET, algorithm=self._encode_algorithm)

        auth_token_model = AuthToken(
            id=user.id,
            token=auth_token,
            expires_in=auth_token_expiration,
        )

        refresh_token_model = RefreshToken(
            id=user.id,
            refresh_token=refresh_token,
            auth_token=auth_token,
            expires_in=refresh_token_expiration,
        )

        self._auth_token_repo.save(auth_token_model)
        self._refresh_token_repo.save(refresh_token_model)

        return auth_token, refresh_token

    def delete_user_tokens(self, user: User) -> None:
        auth_tokens = self._auth_token_repo.find(AuthToken.id == user.id)
        for token in auth_tokens:
            self._auth_token_repo.delete(token)

        refresh_tokens = self._refresh_token_repo.find(RefreshToken.id == user.id)
        for token in refresh_tokens:
            self._refresh_token_repo.delete(token)
