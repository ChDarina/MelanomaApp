from pydantic import BaseModel


class CompanyModel(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class CompanyCreate(BaseModel):
    name: str


class CompanyUpdate(BaseModel):
    name: str
