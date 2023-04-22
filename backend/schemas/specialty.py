from pydantic import BaseModel


class SpecialtyModel(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class SpecialtyCreate(BaseModel):
    name: str


class SpecialtyUpdate(BaseModel):
    name: str
