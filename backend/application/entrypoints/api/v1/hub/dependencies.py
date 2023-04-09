from datetime import datetime

from fastapi import Request
from jwt import decode, DecodeError

from errors import Error

from backend.settings import Settings

from backend.logic import AuthTokenPayload, Requestor


__all__ = [
    'check_authentication',
]


class Unauthorized(Error):
    code = 403


class TokenDecodeError(Error):
    code = 400


def check_authentication(
    request: Request,
):
    auth_token = request.cookies.get(Settings.AUTH_TOKEN_COOKIE_NAME)
    if auth_token is None:
        raise Unauthorized('auth_token-not_provided')

    try:
        payload = AuthTokenPayload(**decode(auth_token, key=Settings.APP_SECRET))
    except DecodeError:
        raise TokenDecodeError('auth_token-decode_error')

    if payload.expires_in < datetime.now():
        raise Unauthorized('auth-token-expired')

    request.state.requestor = Requestor(id=payload.id, type='user', role=payload.role)
