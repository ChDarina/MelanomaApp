from pydantic import BaseModel


class UserModel(BaseModel):
    id: int
    name: str
    age: int
    email: str
    password: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: str
    age: int
    email: str
    password: str


class UserUpdate(BaseModel):
    name: str
    age: int
    email: str
    password: str
