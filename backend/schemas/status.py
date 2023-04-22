from pydantic import BaseModel


class StatusModel(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class StatusCreate(BaseModel):
    name: str


class StatusUpdate(BaseModel):
    name: str
