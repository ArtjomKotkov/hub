from pydantic import BaseModel

from ...models import Requestor


class RequestorRequest(BaseModel):
    requestor: Requestor
