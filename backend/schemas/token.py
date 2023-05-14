from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    id: int
    is_doctor: bool
    token_type: str


class TokenData(BaseModel):
    username: Optional[str]
