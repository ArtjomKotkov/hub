from pydantic import BaseModel


class Requestor(BaseModel):
    id: int
    role: str