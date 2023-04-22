from pydantic import BaseModel


class EducationModel(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class EducationCreate(BaseModel):
    name: str


class EducationUpdate(BaseModel):
    name: str
