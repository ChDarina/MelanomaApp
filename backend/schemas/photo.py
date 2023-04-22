from pydantic import BaseModel


class PhotoModel(BaseModel):
    id: int
    path: str

    class Config:
        orm_mode = True


class PhotoCreate(BaseModel):
    path: str


class PhotoUpdate(BaseModel):
    path: str
