from datetime import datetime

from fastapi import Request
from jwt import decode

from errors import Error

from settings import Settings


__all__ = [
    'check_authentication',
]


class Unauthorized(Error):
    code = 403


def check_authentication(
    request: Request,
):
    auth_token = request.cookies.get(Settings.AUTH_TOKEN_COOKIE_NAME)
    if auth_token is None:
        raise Unauthorized('auth-token-not-provided')

    payload = decode(auth_token, key=Settings.APP_SECRET)

    expiration_datetime = datetime.fromtimestamp(payload['expires_in'])
    if expiration_datetime < datetime.now():
        raise Unauthorized('auth-token-expired')
